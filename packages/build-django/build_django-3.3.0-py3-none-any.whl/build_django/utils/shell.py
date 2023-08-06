from pathlib import Path
from dataclasses import dataclass
from typing import Union, Iterable
from asyncio.subprocess import Process

from .process import run_cmd


@dataclass
class Shell:
    _pwd: Union[str, Path, None]
    
    @property
    def pwd(self) -> Path:
        return Path('./' if self._pwd is None else self._pwd).absolute()

    def _kwargs_to_params(self, **kwargs: dict[str, str]) -> list[str]:
        result = []

        for key in kwargs:
            param = key.replace('_', '-')

            value = kwargs[key]

            if isinstance(value, bool):
                result.append(param)
            else:
                result.extend((param, kwargs[key]))

        return result

    def cd(self, path: Union[str, Path]):
        path = Path(path)

        if path.is_file():
            raise ValueError(f'{path} is a file')

        self._pwd = path

        return self

    async def run(self, args: Iterable[str], **kwargs) -> Process:
        return await run_cmd(args, self.pwd, **kwargs)
