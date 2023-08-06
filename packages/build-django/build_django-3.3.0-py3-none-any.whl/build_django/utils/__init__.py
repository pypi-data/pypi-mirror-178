import secrets
import asyncio
from shlex import quote
from typing import Iterable, Union

import aiofiles

from .process import run_cmd, Process
from .files import write_file
from build_django import const


def generate_env(debug: bool = False, hosts: str = '*') -> str:
    items = [
        f'SECRET_KEY={secrets.token_hex(128)}',
        f'ALLOWED_HOSTS={hosts}'
    ]

    if debug:
        items.append('DEBUG=True')

    return '\n\n'.join(items)


async def edit_settings(file) -> list[str]:
    result = []

    async for line in file:
        if line.startswith('BASE_DIR'):
            result.append('\nfrom environ import Env\n')

            result.append(f'\n{line}\n')

            result.append(f'\nenv = Env({const.DEFAULT_ENV})\n')

            result.append('\nEnv.read_env(BASE_DIR / \'.env\')\n')

        elif line.startswith('SECRET_KEY'):
            result.append('SECRET_KEY = env(\'SECRET_KEY\')\n')
        elif line.startswith('ALLOWED_HOSTS'):
            result.append('ALLOWED_HOSTS = env.tuple(\'ALLOWED_HOSTS\')')
        elif line.startswith('DEBUG'):
            result.append('DEBUG = env(\'DEBUG\')\n')
        else:
            result.append(line)

    result.extend((
        '\n# Custom settings\n'
        "\nif env('USE_SSL'):\n",
        ' ' * 4 + "SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')"
    ))

    return result


async def write_settings(path: str):
    async with aiofiles.open(path, 'r+') as file:
        result = await edit_settings(file)

        await file.seek(0)

        await file.writelines(result)


async def write_requirements(path: str, pip_path: str):
    async with aiofiles.open(path, 'w') as file:
        await run_cmd((pip_path, 'freeze'), stdout=file)


async def install_package(pip_path: str, package: str, *args: str) -> Process:
    return await run_cmd((
        pip_path,
        'install',
        '--require-virtualenv',
        '-v',
        '--disable-pip-version-check',
        *args,
        quote(package)
    ))


async def install_packages(
    pip_path: str,
    packages: Iterable[str],
    output: Union[None, str],
    *args: str
) -> list[Process]:
    added = set()

    tasks = []

    for package in packages:
        if package in added:
            continue

        added.add(package)

        tasks.append(install_package(pip_path, package, *args))

    result = await asyncio.gather(*tasks)

    if output:
        await write_requirements(output, pip_path)

    return result
