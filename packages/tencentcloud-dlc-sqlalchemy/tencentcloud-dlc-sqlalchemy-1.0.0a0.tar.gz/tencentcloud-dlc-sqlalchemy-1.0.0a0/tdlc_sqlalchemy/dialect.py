import re
from collections import defaultdict
from urllib.parse import unquote_plus
from tdlc_connector import constants

import sqlalchemy.types as sqltypes
from sqlalchemy import event as sa_vnt
from sqlalchemy import exc as sa_exc
from sqlalchemy import util as sa_util
from sqlalchemy.engine import default, reflection
from sqlalchemy.schema import Table
from sqlalchemy.sql import text
from sqlalchemy.sql.elements import quoted_name
from sqlalchemy.sql.sqltypes import String


from .base import (
    DlcCompiler,
    DlcDDLCompiler,
    DlcExecutionContext,
    DlcIdentifierPreparer,
    DlcTypeCompiler,
)
from . import types


COMPATIBLE_TYPES = {
    "TINYINT"           :types.TINYINT,
    "SMALLINT"          :types.SMALLINT,
    "BIGINT"            :types.BIGINT,
    "INT"               :types.INT,
    "INTEGER"           :types.INTEGER,
    "FLOAT"             :types.FLOAT,
    "DOUBLE"            :types.DOUBLE,
    "DECIMAL"           :types.DECIMAL,

    "BOOLEAN"           :types.BOOLEAN,
    "CHAR"              :types.CHAR,
    "VARCHAR"           :types.VARCHAR,
    "STRING"            :types.String,
    "TEXT"              :types.TEXT,
    "TINYTEXT"          :types.TEXT,
    "MEDIUMTEXT"        :types.TEXT,
    "LONGTEXT"          :types.TEXT,



    "DATE"              :types.DATE,
    "TIME"              :types.TIME,
    "TIMESTAMP"         :types.TIMESTAMP,
    "DATETIME"          :types.DATETIME,

    "JSON"              :types.JSON,
    "ARRAY"             :types.ARRAY,
    "STRUCT"            :types.STRUCT,
    "MAP"               :types.JSON,

    "BOOL"              :types.BOOLEAN,
    "BOOLEAN"           :types.BOOLEAN,
}

TYPE_REGEXP = r'(\w+)(\((\d+)(.+(\d+))?\))?'
def get_column_type(_type):

    m = re.match(TYPE_REGEXP, _type)

    name = m.group(1).upper()
    arg1 = m.group(3)
    arg2 = m.group(5)

    col_type = COMPATIBLE_TYPES.get(name, sqltypes.NullType)
    col_type_kw = {}

    if name in ('CHAR', 'STRING', 'VARCHAR') and arg1 is not None:
        col_type_kw['length'] = int(arg1)
    
    elif name in ('DECIMAL',) and arg1 is not None and arg2 is None:
        col_type_kw['precision'] = int(arg1)
        col_type_kw['scale'] = int(arg2)
    
    return col_type(**col_type_kw)



class DlcDialect(default.DefaultDialect):

    name = "dlc"

    driver = "dlc"

    max_identifier_length = 255

    cte_follows_insert = True

    supports_statement_cache = False

    encoding = 'UTF8'

    default_paramstyle = "pyformat"

    convert_unicode = True

    supports_unicode_statements = True
    
    supports_unicode_binds = True

    returns_unicode_strings = String.RETURNS_UNICODE

    description_encoding = None

    postfetch_lastrowid = False

    supports_sane_rowcount = True

    # Indicate whether the dialect properly implements rowcount for
    # ``UPDATE`` and ``DELETE`` statements when executed via
    # executemany.
    supports_sane_multi_rowcount = True

    # NUMERIC type returns decimal.Decimal
    supports_native_decimal = True

    # The dialect supports a native boolean construct.
    # This will prevent types.Boolean from generating a CHECK
    # constraint when that type is used.
    supports_native_boolean = True

    # The dialect supports ``ALTER TABLE``.
    supports_alter = True

    # The dialect supports CREATE SEQUENCE or similar.
    supports_sequences = False
 
    # The dialect supports inserting multiple rows at once.
    supports_multivalues_insert = True

    supports_comments = True

    preparer = DlcIdentifierPreparer

    ddl_compiler = DlcDDLCompiler

    type_compiler = DlcTypeCompiler

    statement_compiler = DlcCompiler

    execution_ctx_cls = DlcExecutionContext

    catalog = None

    schema = None

    def _get_default_schema_name(self, connection):
        return self.schema

    @classmethod
    def dbapi(cls):
        import tdlc_connector
        return  tdlc_connector

    def create_connect_args(self, url):
        '''
        RFC1738: https://www.ietf.org/rfc/rfc1738.txt
        dialect+driver://username:password@host:port/database

        支持两种配置方式:

        1. dlc://ak:sk(:token)@region/database?engine=engineName&engine-type&arg1=value1
        2. dlc:///?secretId=1&secretKey=2&token

        {'host': 'ap-shanghai', 'database': 'public-engine:spark', 'username': 'ak', 'password': 'sk:token'}

        '''
        opts = url.translate_connect_args()
        query = dict(url.query)

        region = opts.get('host')
        secret_id = opts.get('username') 
        secret_key = opts.get('password')
        token = query.pop('token', None)

        if secret_key and secret_key.find(':') > 0:
            secrets = secret_key.split(':')
            secret_key = secrets[0]
            token = secrets[-1]

        self.schema = opts.get('database')

        self.catalog = opts.get('catalog', constants.Catalog.DATALAKECATALOG)


        # engine_type =  constants.EngineType.PRESTO
        # if engine and engine.find(':') > 0:
        #     parts = engine.split(':')
        #     engine = parts[0]
        #     engine_type = parts[-1]
        
        kwargs = {
            'region': region or query.pop('region', None),
            'secret_id': secret_id or query.pop('secretId', None),
            'secret_key': secret_key or query.pop('secretKey', None),
            'token': token or query.pop('token', None),
            'endpoint': query.pop('endpoint', None),
            'engine': query.pop('engine', None),
            'engine_type': query.pop('engineType', constants.EngineType.PRESTO),
            'download': query.pop('download', False),
            'mode': query.pop('mode', constants.Mode.LASY)
        }

        return[[], kwargs]
    
    @reflection.cache
    def get_schema_names(self, connection, **kw):
        """
        Gets all schema names.
        """
        cursor = connection.execute(
            text("SHOW /* tdlc:sqlalchemy:get_schema_names */ SCHEMAS")
        )

        return [self.normalize_name(row[0]) for row in cursor]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        """
        Gets all table names.
        """
        schema = schema or self.default_schema_name
        current_schema = schema
        ret = []
        if schema:
            cursor = connection.execute(
                text(
                    f"SHOW /* tdlc:sqlalchemy:get_table_names */ TABLES IN {schema}"
                )
            )

            ret = [self.normalize_name(row[0]) for row in cursor]

        return ret
    
    @reflection.cache
    def get_view_names(self, connection, schema=None, **kw):
        """
        Gets all view names
        """
        ret = []
        schema = schema or self.default_schema_name
        if schema:
            cursor = connection.execute(
                text(
                    f"SHOW /* tdlc:sqlalchemy:get_view_names */ VIEWS IN {schema}"
                )
            )
            ret = [self.normalize_name(row[0]) for row in cursor]
        return ret
    
    def get_table_comment(self, connection, table_name, schema, **kw):

        schema = schema or self.default_schema_name

        ret = ""
        if schema:
            cursor = connection.execute(
                text(f"SHOW /* tdlc:sqlalchemy:get_table_comment*/ TBLPROPERTIES {schema}.{table_name}")
            )
            ret = {row[0]: row[1] for row in cursor}
        return {
            "text": ret.get("comment", None)
        }

    @reflection.cache
    def get_columns(self, connection, table_name, schema, **kw):

        schema = schema or self.default_schema_name
        ret = []
        if schema:
            cursor = connection.execute(
                text(f"SHOW /* tdlc:sqlalchemy:get_columns*/ COLUMNS IN {schema}.{table_name}")
            )

            for row in cursor:

                column = {
                    'name': row[0],
                    'type': get_column_type(row[1])
                }
                ret.append(column)

        return ret

    def get_indexes(self, connection, table_name, schema, **kw):
        ''' 不支持 '''
        return []
    
    def get_pk_constraint(self, connection, table_name, schema, **kw):
        ''' 不支持 '''
        return []
    
    def get_foreign_keys(self, connection, table_name, schema, **kw):
        ''' 不支持 '''
        return []
    
    def has_table(self, connection, table_name, schema, **kw) -> None:

        schema = schema or self.default_schema_name

        try:
            r = connection.execute(
                text(f"DESC /* tdlc:sqlalchemy:has_table */ {schema}.{table_name}")
            )
            row = r.fetchone()
            return row is not None
        except Exception as e:
            # TODO 异常分类
            return False
    
    def has_index(self, connection, table_name, index_name, schema, **kw):
        return False
    
    def has_sequence(self, connection, sequence_name, schema, **kw) -> None:
        return False



dialect = DlcDialect
