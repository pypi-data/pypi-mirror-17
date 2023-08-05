import re

import sqlalchemy
from sqlalchemy.schema import CreateTable
from sqlalchemy_views import CreateView

from shiftmanager import queries
from shiftmanager.memoized_property import memoized_property
from shiftmanager.privileges import grants_from_privileges

# Redshift distribution styles
DISTSTYLES_BY_INDEX = {
    0: 'EVEN',
    1: 'KEY',
    8: 'ALL',
}


# Regex for SQL identifiers (valid table and column names)
SQL_IDENTIFIER_RE = re.compile(r"""
   [_a-zA-Z][\w$]*  # SQL standard identifier
   |                # or
   (?:"[^"]+")+     # SQL delimited (quoted) identifier
""", re.VERBOSE)


def _get_relation_key(name, schema):
    if schema is None:
        return name
    else:
        return schema + "." + name


def _get_schema_and_relation(key):
    if '.' not in key:
        return (None, key)
    identifiers = SQL_IDENTIFIER_RE.findall(key)
    if len(identifiers) == 1:
        return (None, key)
    elif len(identifiers) == 2:
        return identifiers
    raise ValueError("%s does not look like a valid relation identifier")


class ReflectionMixin(object):
    """The database reflection base class for `Redshift`."""

    @memoized_property
    def engine(self):
        """A `sqlalchemy.engine` which wraps `connection`.
        """
        return sqlalchemy.create_engine("redshift+psycopg2://",
                                        poolclass=sqlalchemy.pool.StaticPool,
                                        creator=lambda: self.connection)

    @memoized_property
    def meta(self):
        """A `sqlalchemy.schema.MetaData` instance used for reflection calls.
        """
        meta = sqlalchemy.MetaData()
        meta.bind = self.engine
        return meta

    @property
    def preparer(self):
        """A Redshift-aware identifier preparer."""
        return self.engine.dialect.identifier_preparer

    def get_table_names(self, schema=None, **kwargs):
        """Return a list naming all tables and views defined in *schema*.
        """
        return self.engine.dialect.get_table_names(self.engine, schema,
                                                   **kwargs)

    def reflected_table(self, name, *args, **kwargs):
        """Return a `sqlalchemy.schema.Table` reflected from the database.

        This is simply a convenience method which passes arguments to the
        `sqlalchemy.schema.Table` constructor, so you may override various
        properties of the existing table.
        In particular, Redshift-specific attributes like
        distkey and sorkey can be set through ``redshift_*`` keyword arguments
        (``redshift_distkey='col1'``,
        ``redshift_interleaved_sortkey=('col1', 'col2')``, etc.)

        The return value is suitable input for the `table_definition`
        or `deep_copy` methods, useful for changing the structure of an
        existing table.

        *extend_existing* is set to True by default.

        Notes
        -----
        See SQLAlchemy's dcoumentation on `Overriding Reflected Columns
        <http://docs.sqlalchemy.org/en/rel_1_0/core/reflection.html#overriding-reflected-columns>`_
        and ``sqlalchemy-redshift``'s `DDLCompiler docs
        <http://redshift-sqlalchemy.readthedocs.org/en/latest/ddl-compiler.html>`_
        """
        kw = kwargs.copy()
        analyze_compression = kwargs.pop('analyze_compression', None)
        kw['autoload'] = True
        kw['extend_existing'] = kw.get('extend_existing', True)
        table = sqlalchemy.Table(name, self.meta, *args, **kw)
        if analyze_compression:
            for col in table.columns:
                # Initialize this field
                col.info['encode'] = 'raw'
        return table

    def reflected_privileges(self, relation, schema=None, use_cache=True):
        """Return a SQL str which recreates all privileges for *relation*.

        Parameters

        relation : `str` or `sqlalchemy.schema.Table`
            The table or view to reflect
        schema : `str`
            The database schema in which to look for *relation*
            (only used if *relation* is str)
        use_cache : `bool`
            Use cached results for the privilege query, if available
        """
        return ';\n'.join(self._privilege_statements(relation, use_cache))

    def table_definition(self, table, schema=None,
                         copy_privileges=True, use_cache=True,
                         analyze_compression=False):
        """
        Return a str containing the necessary SQL statements
        to recreate *table*.

        Parameters
        ----------
        table : `str` or `sqlalchemy.schema.Table`
            The table to reflect
        schema : `str`
            The database schema in which to look for *table*
            (only used if *table* is str)
        copy_privileges : `bool`
            Reflect ownership and grants on the existing table
            and include them in the return value
        use_cache : `bool`
            Use cached results for the privilege query, if available
        """
        table = self._pass_or_reflect(table, schema=schema)
        table_name = self.preparer.format_table(table)
        if analyze_compression:
            result = self.engine.execute("ANALYZE COMPRESSION %s" % table_name)
            encodings = dict((r.Column, r.Encoding) for r in result)
            for col in table.columns:
                col.info['encode'] = encodings[col.key]
        statements = [str(CreateTable(table).compile(self.engine))]
        if copy_privileges:
            statements += self._privilege_statements(table, use_cache)
        return ';\n'.join(statements)

    def view_definition(self, view, schema=None,
                        copy_privileges=True, use_cache=True,
                        execute=False,
                        **kwargs):
        """Return a SQL str defining *view*.

        Parameters
        ----------
        view : `str` or `sqlalchemy.schema.Table`
            The view to reflect
        schema : `str`
            The database schema in which to look for *view*
            (only used if *view* is str)
        copy_privileges : `bool`
            Reflect ownership and grants on the existing view
            and include them in the return value
        use_cache : `bool`
            Use cached results for the privilege query, if available
        execute : `bool`
            Execute the command in addition to returning it.
        kwargs :
            Additional keyword arguments will be passed unchanged to the
            `reflected_table` method.
        """
        view = self._pass_or_reflect(view, schema)
        definition = self.engine.dialect.get_view_definition(
            self.engine, name=view.name, schema=view.schema, **kwargs)
        create_statement = str(CreateView(view, definition)
                               .compile(self.engine))
        statements = []
        if copy_privileges:
            statements += self._privilege_statements(view, use_cache)
        batch = create_statement + ';\n'.join(statements)
        return self.mogrify(batch, None, execute)

    def deep_copy(self, table, schema=None,
                  copy_privileges=True, use_cache=True,
                  cascade=False, distinct=False,
                  analyze_compression=False,
                  execute=False,
                  **kwargs):
        """Return a SQL str defining a deep copy of *table*.

        This method can be used to simply sort and clean
        an unvacuumable table, or it can be used to migrate
        to a revised table structure. You can use the
        `reflected_table` method with overrides to generate a new
        table structure, then pass that revised object in as *table*.

        Parameters
        ----------
        table : `str` or `sqlalchemy.schema.Table`
            The table to reflect
        schema : `str`
            The database schema in which to look for *table*
            (only used if *table* is str)
        copy_privileges : `bool`
            Reflect ownership and grants on the existing table
            and include them in the return value
        use_cache : `bool`
            Use cached results for the privilege query, if available
        cascade : `bool`
            Drop any dependent views when dropping the source table
        distinct : `bool`
            Deduplicate the table by adding DISTINCT to the SELECT statement
        analyze_compression : `bool`
            Update the column compression encodings based on results of an
            ANALYZE COMPRESSION statement on the table.
        execute : `bool`
            Execute the command in addition to returning it.
        kwargs :
            Additional keyword arguments will be passed unchanged to the
            `reflected_table` method.
        """
        table = self._pass_or_reflect(table, schema=schema, **kwargs)
        table_name = self.preparer.format_table(table)
        outgoing_name = table_name + '$outgoing'
        outgoing_name_simple = table.name + '$outgoing'
        table_definition = self.table_definition(table, None,
                                                 copy_privileges, use_cache,
                                                 analyze_compression)
        insert_statement = "\nINSERT INTO {table_name} SELECT "
        if distinct:
            insert_statement += "DISTINCT "
        insert_statement += "* from {outgoing_name}"
        drop_statement = "DROP TABLE {outgoing_name}"
        if cascade:
            drop_statement += " CASCADE"
        statements = (
            "LOCK TABLE {table_name}",
            "ALTER TABLE {table_name} RENAME TO {outgoing_name_simple}",
            table_definition,
            insert_statement,
            drop_statement,
        )
        batch = ';\n'.join(statements).format(
            table_name=table_name, outgoing_name=outgoing_name,
            outgoing_name_simple=outgoing_name_simple,
        )
        return self.mogrify(batch, None, execute)

    def _cache_privileges(self):
        result = self.engine.execute(queries.all_privileges)
        self._all_privileges = {}
        for r in result:
            key = _get_relation_key(r.relname, r.schema)
            self._all_privileges[key] = r

    def _privilege_statements(self, relation, use_cache):
        if not use_cache or not self._all_privileges:
            self._cache_privileges()
        priv_info = self._all_privileges[relation.key]
        relation_name = self.preparer.format_table(relation)
        statements = [("ALTER {type} {relation_name} OWNER TO {owner}"
                       .format(type=priv_info.type.upper(),
                               relation_name=relation_name,
                               owner=priv_info.owner_name))]
        statements += grants_from_privileges(priv_info.privileges,
                                             relation.key)
        return statements

    def _pass_or_reflect(self, table, schema, **kwargs):
        try:
            # This is already a sqlalchemy.Table object; return it unchanged.
            CreateTable(table)
        except AttributeError:
            table = self.reflected_table(table, schema=schema, **kwargs)
        return table
