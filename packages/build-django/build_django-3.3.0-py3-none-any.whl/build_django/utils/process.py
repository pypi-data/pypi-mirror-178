import asyncio
from pathlib import Path
from subprocess import SubprocessError
from asyncio.subprocess import PIPE, Process
from typing import Union, Iterable

from . import system


async def run_cmd(
    args: Iterable[str],
    cwd: Union[str, None, Path] = None,
    **kwargs
) -> Process:
    if cwd:
        cwd = str(cwd)

    cmd = ' '.join(args)

    kwargs = {
        'stdout': PIPE,
        'stderr': PIPE,
        'cwd': cwd,
        **kwargs
    }

    process = await asyncio.create_subprocess_shell(cmd, **kwargs)

    result = await process.communicate()

    out, err = result

    code = process.returncode

    if code != 0:
        raise SubprocessError(f'{code}: {err}')

    if out:
        if isinstance(out, bytes):
            out = system.decode(out)

        print(out)

    return process
