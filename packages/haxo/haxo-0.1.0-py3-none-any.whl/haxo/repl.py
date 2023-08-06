from __future__ import annotations

from typing import Any, Optional, AsyncGenerator, TYPE_CHECKING, Union
from traceback import format_exception

import asyncpg

from yarl import URL
from tabulate import tabulate
from pyfiglet import figlet_format
from rich import print as pprint

from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexers.sql import SqlLexer
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit.patch_stdout import patch_stdout

from .completer import PostgreSQLCompleter

if TYPE_CHECKING:
    from asyncpg import Connection, Record

prompt_style = Style.from_dict({
    'db': '#0000FF bold',
    'bracket': '#C1E1C1',
    "task": "#bfe3b4"
})

style = Style.from_dict({
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})

class RePL:
    """
    PostgreSQL RePL.
    """

    def __init__(self, dsn: str):
        self.uri = URL(dsn)
        self.dsn = dsn
        self.session = PromptSession(lexer=PygmentsLexer(SqlLexer), completer=PostgreSQLCompleter(), style=style, auto_suggest=AutoSuggestFromHistory(), history=InMemoryHistory())
        self.error_count = -1
        self.tasks: dict[int, str] = {}

    async def get_user_input(self) -> AsyncGenerator[tuple[int, str], Any]:
        i = -1
        while True:
            i += 1
            try:
                html = HTML(f"<db>{self.uri.scheme} {self.postgres_version}{self.uri.path} __ {self.uri.user}</db> <bracket>!</bracket><task>{i}</task><bracket>!</bracket> ")
                with patch_stdout():
                    res = await self.session.prompt_async(html, style=prompt_style, complete_in_thread=True)
                yield i, res
            except KeyboardInterrupt:
                continue
            except EOFError:
                break

    async def _raw_execute_query(self, query: str, connection: Connection, *, row: bool = False) -> tuple[int, Any]:

        try:
            response = (await connection.fetch(query)) if not row else (await connection.fetchrow(query))
        except Exception as e:
            return (1, format_exception(type(e), e, e.__traceback__, chain=False))

        if not response:
            return (2, None)

        return (0, response)

    async def execute_query(self, query: str) -> Optional[Union[int, str]]:
        connection = await asyncpg.connect(self.dsn)

        res: tuple[int, Any] = await self._raw_execute_query(query, connection) # type: ignore

        if res[0] == 1:
            self.error_count += 1
            error = "".join(res[1])
            if "PostgresSyntaxError" in error:
                print(f"Syntax error occured. Perhaps check your spelling? ERRs: {self.error_count}")
            else:
                print(error)
            return 5

        elif res[0] == 2:
            return None

        response: list[Record] = res[1]


        table = tabulate.tabulate(
            (dict(item) for item in response), headers="keys", tablefmt="psql"
        )

        return table

    async def start(self) -> None:
        conn: Connection = (await asyncpg.connect(self.dsn)) # type: ignore

        version: tuple[int, Record] = await self._raw_execute_query("SELECT version();", conn, row=True)
        server_version: tuple[int, Record] = await self._raw_execute_query("SHOW server_version;", conn, row=True)

        rec: Record = version[1]
        server_rec: Record = server_version[1]

        self.postgres_version = server_rec["server_version"]

        await conn.close()

        pprint(figlet_format("HAXO", "slant"), end="")
        pprint(f"{'+_' * 20}")
        pprint(rec["version"])
        pprint(f"{'+_' * 20}")

        async for i, query in self.get_user_input():
            self.tasks[i] = query
            if query.startswith("/execute"):
                task_id = int((query.split())[1])
                query = self.tasks.get(task_id) # type: ignore

                if not query:
                    print("Incorrect task id.")
                    continue

            res = await self.execute_query(query)
            if not res:
                is_select = False
                
                if "select" in query.lower():
                    is_select = True

                print(f"Results not found. {'Usually means table is empty.' if is_select else ''}")
            elif res == 5:
                continue
            else:
                print(res)
