from abc import ABC, abstractmethod
from typing import Any, Optional, Union

from pydantic import BaseModel

from telefone.api import ABCAPI, API
from telefone.bot.states import StateRepr


class BaseBotUpdate(ABC, BaseModel):
    state_repr: Optional[StateRepr] = None
    unprepared_ctx_api: Optional[Any] = None

    @property
    def ctx_api(self) -> Optional[Union["ABCAPI", "API"]]:
        return getattr(self, "unprepared_ctx_api")

    @abstractmethod
    def get_state_key(self) -> Optional[int]:
        pass
