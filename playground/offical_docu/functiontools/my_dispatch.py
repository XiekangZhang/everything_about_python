from enum import Enum
from functools import singledispatch


# define your sql dialect types
class BaseDialect:
    """Base class for all SQL dialects"""


class PostgresDialect(BaseDialect):
    pass


class BigQueryDialect(BaseDialect):
    pass


class SnowflakeDialect(BaseDialect):
    pass


# create the generic sql generation function
# singledispatch only dispatches on the type of the first argument
@singledispatch
def generate_sql_statement(
    dialect: BaseDialect, table_name: str, columns: list[str]
) -> str:
    raise NotImplementedError(
        f"SQL generation not implemented for dialect type: {type(dialect).__name__}"
    )


# register implementations for specific dialects
@generate_sql_statement.register(PostgresDialect)
def _(dialect: PostgresDialect, table_name: str, columns: list[str]) -> str:
    cols_str = ", ".join(f'"{col}"' for col in columns)
    return f'SELECT {cols_str} FROM "{table_name}"'


@generate_sql_statement.register(BaseDialect)
def _(dialect: BaseDialect, table_name: str, columns: list[str]) -> str:
    cols_str = ", ".join(columns)
    return f"SELECT {cols_str} FROM {table_name}"


if __name__ == "__main__":
    postgres_dialect = PostgresDialect()
    print(generate_sql_statement(postgres_dialect, "users", ["id", "name", "email"]))
