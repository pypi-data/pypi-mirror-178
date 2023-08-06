from __future__ import annotations

from typing import Callable
from functools import wraps

import typer
import anyio

from .repl import RePL

def run_async(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        async def coro_wrapper():
            return await func(*args, **kwargs)

        return anyio.run(coro_wrapper)

    return wrapper

@run_async
async def main(dsn: str):
    typer.echo("Connecting to %s" % dsn)
    repl = RePL(dsn)
    await repl.start()

def run():
    typer.run(main) 
