from typing import Optional

from dictum_core.backends.mixins.datediff import DatediffCompilerMixin
from dictum_core.backends.secret import Secret
from dictum_core.backends.sql_alchemy import SQLAlchemyBackend, SQLAlchemyCompiler
from sqlalchemy import Float, Integer
from sqlalchemy.sql import cast


class PostgresCompiler(DatediffCompilerMixin, SQLAlchemyCompiler):
    def div(self, a, b):
        """Dictum's division is like Python's, e.g. 1/2 == 0.5,
        while in Postgres 1/2 == 0, so we need to cast the first
        arg to float.
        """
        return cast(a, Float) / b

    def datepart(self, part, arg):
        if part in {"dow", "dayofweek"}:
            part = "isodow"
        # cast cause date_part returns double
        return cast(super().datepart(part, arg), Integer)

    def datediff_day(self, start, end):
        return self.todate(end) - self.todate(start)

    def dateadd(self, part, interval, value):
        """DATEADD in Postgres is implemented through interval data type.
        Intervals can be added to the value as just a string. The only unsupported part
        is quarter, so we have to replace it with 3 months.
        """
        if part == "quarter":
            part = "month"
            interval = interval * 3

        return value + f"{interval} {part}"


class PostgresBackend(SQLAlchemyBackend):
    type = "postgres"
    compiler_cls = PostgresCompiler

    def __init__(
        self,
        database: str = "postgres",
        host: str = "localhost",
        port: int = 5432,
        username: str = "postgres",
        password: Secret = None,
        pool_size: Optional[int] = 5,
        default_schema: Optional[str] = None,
    ):
        super().__init__(
            drivername="postgresql",
            database=database,
            host=host,
            port=port,
            username=username,
            password=password,
            pool_size=pool_size,
            default_schema=default_schema,
        )
