from asyncio import iscoroutinefunction
from typing import Callable, List, Optional, Type, Union

from telefone.bot.rules.abc import ABCRule
from telefone.bot.states.types import BaseStateGroup, get_state_repr
from telefone.bot.updates import BaseBotUpdate


class Function(ABCRule[BaseBotUpdate]):
    """
    A rule that calls a function to satisfy a check.
    The function can accept any update objects, but should
    always return a boolean.
    """

    def __init__(self, func: Callable[[BaseBotUpdate], bool]) -> None:
        self.func = func

    async def check(self, update: BaseBotUpdate) -> bool:
        if iscoroutinefunction(self.func):
            return await self.func(update)
        return self.func(update)


class State(ABCRule[BaseBotUpdate]):
    def __init__(
        self,
        state: Optional[Union[BaseStateGroup, List[BaseStateGroup]]] = None,
    ):
        if not isinstance(state, list):
            state = [] if state is None else [state]
        self.state = [get_state_repr(s) for s in state]

    async def check(self, update: BaseBotUpdate) -> bool:
        if update.state_repr is None:
            return not self.state
        return update.state_repr.state in self.state


class StateGroup(ABCRule[BaseBotUpdate]):
    def __init__(
        self,
        state_group: Union[Type[BaseStateGroup], List[Type[BaseStateGroup]]],
    ):
        if not isinstance(state_group, list):
            state_group = [] if state_group is None else [state_group]
        self.state_group = [group.__name__ for group in state_group]

    async def check(self, update: BaseBotUpdate) -> bool:
        if update.state_repr is None:
            return not self.state_group

        group_name = update.state_repr.state.split(":", maxsplit=1)[0]
        return group_name in self.state_group
