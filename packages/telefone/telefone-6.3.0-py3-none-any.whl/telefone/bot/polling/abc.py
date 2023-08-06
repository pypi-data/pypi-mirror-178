from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Generator, Optional

from telefone.api.abc import ABCAPI
from telefone.errors import ABCErrorHandler


class ABCPolling(ABC):
    api: "ABCAPI"
    error_handler: "ABCErrorHandler"

    @abstractmethod
    async def listen(self) -> AsyncIterator:
        """
        Receives and yields update objects
        """
        pass
