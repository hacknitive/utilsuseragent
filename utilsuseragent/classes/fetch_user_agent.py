from typing import Any
from collections.abc import Sequence
from sqlite3 import connect

from aiosqlite import connect as async_connect


class FetchUserAgent:

    def __init__(
            self,
            database_connection_string: str = 'user_agent.sqlite',
    ) -> None:
        self.database_connection_string = database_connection_string

    def perform(
            self,
            **kwargs,
    ) -> tuple[str]:
        filter_ = self._create_filter(inputs=kwargs)
        query = self._create_query(filter_=filter_)
        return self._fetch(query=query)

    async def async_perform(
            self,
            **kwargs,
    ) -> tuple[str]:
        filter_ = self._create_filter(inputs=kwargs)
        query = self._create_query(filter_=filter_)
        return await self._async_fetch(query=query)

    @staticmethod
    def _create_filter(inputs: dict[str, Any]) -> str:
        filter_ = list()
        for key, value in inputs.items():
            if value is None:
                filter_.append(f"{key} IN ('null')")

            elif isinstance(value, str):
                filter_.append(f"{key} IN ('{value}')")

            elif isinstance(value, Sequence):
                prepared_value = [f"'{i}'" for i in value]
                filter_.append(f"{key} IN ({', '.join(prepared_value)})")

        return ' AND '.join(filter_)

    @staticmethod
    def _create_query(filter_: str) -> str:
        return f"""
        SELECT * 
        FROM user_agent 
        WHERE {filter_}
        ORDER BY RANDOM() LIMIT 1;
        """

    def _fetch(
            self,
            query: str,
    ) -> tuple[str]:
        with connect(self.database_connection_string) as connection:
            cursor = connection.cursor()
            cursor.execute(query)

            return cursor.fetchone()

    async def _async_fetch(
            self,
            query: str,
    ) -> tuple[str]:
        async with async_connect(self.database_connection_string) as connection:
            cursor = await connection.cursor()
            await cursor.execute(query)

            return await cursor.fetchone()
