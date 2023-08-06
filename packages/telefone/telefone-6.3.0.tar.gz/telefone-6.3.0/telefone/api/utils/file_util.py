from io import BytesIO
from pathlib import Path
from typing import Optional, Union

Bytes = Union[bytes, BytesIO]
FilePath = Union[str, Path]

try:
    from aiofiles import open
except ImportError:
    open = None


class File:
    def __init__(
        self, name: Optional[str] = None, content: Optional["Bytes"] = None
    ) -> None:
        if open is None:
            raise SystemExit(
                "Reinstall `telefone` package with file-uploading extra "
                "before using File utility"
            )

        self.name = name or "Unnamed"
        self.content = content.getvalue() if isinstance(content, BytesIO) else content

    @classmethod
    def from_bytes(cls, file_source: Bytes, name: Optional[str] = None) -> "File":
        return cls(name=name, content=file_source)

    @classmethod
    async def from_path(
        cls, file_source: FilePath, name: Optional[str] = None
    ) -> "File":
        path = Path(file_source) if isinstance(file_source, str) else path

        async with open(path, "rb") as f:
            return cls(name=name or path.name, content=await f.read())

    def __repr__(self) -> str:
        return f"File(name={self.name!r})"
