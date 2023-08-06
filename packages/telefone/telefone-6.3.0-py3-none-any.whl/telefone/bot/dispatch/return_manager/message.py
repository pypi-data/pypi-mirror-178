from typing import TYPE_CHECKING, Union

from telegram_text.styles import Style
from telegram_text.elements import Element

from telefone.bot.dispatch.return_manager import ABCReturnManager

if TYPE_CHECKING:
    from telefone.bot.updates import MessageUpdate


class MessageReturnManager(ABCReturnManager):
    @ABCReturnManager.instance_of((str, Element))
    async def str_handler(
        self, value: Union[str, Element], message: "MessageUpdate", _: dict
    ):
        await message.answer(value)

    @ABCReturnManager.instance_of((tuple, list))
    async def iter_handler(
        self, value: Union[tuple, list], message: "MessageUpdate", _: dict
    ):
        [await message.answer(str(e)) for e in value]

    @ABCReturnManager.instance_of(dict)
    async def dict_handler(self, value: dict, message: "MessageUpdate", _: dict):
        await message.answer(**value)
