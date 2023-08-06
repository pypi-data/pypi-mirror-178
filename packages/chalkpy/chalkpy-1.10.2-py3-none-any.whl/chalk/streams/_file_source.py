from typing import Any

from pydantic import BaseModel

from chalk.streams._types import StreamSource


class FileSource(BaseModel, StreamSource):
    path: str
    key_separator: str = "|"

    def config_to_json(self) -> Any:
        return self.json()
