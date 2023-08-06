import asyncio
from shlex import quote
from subprocess import SubprocessError
from dataclasses import dataclass
from asyncio.subprocess import Process
from typing import Iterable, Any, cast

from .shell import Shell


class GitShell(Shell):
    async def cmd(self, args, **kwargs) -> Process:
        params = self._kwargs_to_params(**kwargs)

        return await self.run(('git', *args, *params))


@dataclass
class ConfigSection(GitShell):
    section: str
    
    async def value(self, name: str) -> str:
        try:
            process = await self.cmd(('config', '--get', f'{self.section}.{name}'))
        except SubprocessError:
            return ''

        return cast(str, process.stdout)

    async def set(self, name: str, value: Any) -> Any:
        await self.cmd(('config', f'{self.section}.{name}', quote(value)))

        return self


class Config(GitShell):
    def section(self, name: str) -> ConfigSection:
        return ConfigSection(self.pwd, name)


class Repo(GitShell):
    @property
    def initialized(self) -> bool:
        return (self.pwd / '.git').exists()

    @property
    def config(self) -> Config:
        return Config(self.pwd)

    async def setup(self, email: str = '', name: str = ''):
        tasks = []

        section = self.config.section('user')

        cur_name = await section.value('name')

        if not cur_name:
            tasks.append(section.set('name', name))

        cur_email = await section.value('email')

        if not cur_email:
            tasks.append(section.set('email', email))

        await asyncio.gather(*tasks)

        return self


    async def init(self) -> Process:
        if self.initialized:
            raise ValueError(
                f'There is already a git repository at {self.pwd}'
            )

        return await self.cmd(('init',))

    async def add(self, files: Iterable[str], **kwargs) -> Process:
        args = ('add', *map(quote, files))

        return await self.cmd(args, **kwargs)

    async def commit(self, message: str, **kwargs) -> Process:
        args = ('commit', '-m', quote(message))

        return await self.cmd(args, **kwargs)
