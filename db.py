from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
schema_name = "public"  # schema name is added for foreign key constraints
table_name_prefix = "asmar60093530"  # prefix is added to table name to avoid conflicts during presentation
# not including schema name in foreign key string causes sqlalchemy.exc.NoReferencedTableError
table_name_prefix_with_schema = schema_name + "." + table_name_prefix
