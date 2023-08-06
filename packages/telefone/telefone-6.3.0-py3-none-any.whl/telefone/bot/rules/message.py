from re import compile
from typing import Iterable, List, Optional, Union

from telefone.bot.rules.abc import ABCRule
from telefone.bot.updates import MessageUpdate


class Command(ABCRule[MessageUpdate]):
    def __init__(
        self, text: str, prefixes: Optional[Union[str, Iterable[str]]] = "/"
    ) -> None:
        if isinstance(prefixes, str):
            prefixes = [prefixes]

        self.text = text
        self.prefixes = prefixes

    async def check(self, msg: MessageUpdate) -> bool:
        if text := msg.text or msg.caption:
            for prefix in self.prefixes:
                if not text.startswith(prefix):
                    continue
                elif text.startswith(prefix + self.text + " "):
                    return {"args": text[len(prefix + self.text) + 1 :].split()}
                elif text == prefix + self.text:
                    return True
        return False


class FromChat(ABCRule[MessageUpdate]):
    """
    A rule which checks if the message was sent from a specified chat.
    If it's not, the rule will return False and the message will be ignored.
    """

    def __init__(self, chats: Union[int, List[int]]) -> None:
        self.chats = chats if isinstance(chats, list) else [chats]

    async def check(self, msg: MessageUpdate) -> bool:
        return msg.chat.id in self.chats


class IsReply(ABCRule[MessageUpdate]):
    """
    A rule that checks if the message is a reply.
    """

    async def check(self, msg: MessageUpdate) -> bool:
        return msg.reply_to_message is not None


class IsForward(ABCRule[MessageUpdate]):
    """
    A rule that checks if the message was forwarded.
    """

    async def check(self, msg: MessageUpdate) -> bool:
        return msg.forward_date is not None


class IsGroup(ABCRule[MessageUpdate]):
    """
    A rule that checks if the message was sent in the chat.
    """

    async def check(self, msg: MessageUpdate) -> bool:
        return msg.chat.type in ["group", "supergroup"]


class IsPrivate(ABCRule[MessageUpdate]):
    """
    A rule that checks if the message is private.
    """

    async def check(self, msg: MessageUpdate) -> bool:
        return msg.chat.type == "private"


class Length(ABCRule[MessageUpdate]):
    """
    A rule that checks if the message is longer than or equal to the given length.
    """

    def __init__(self, minimum_length: int) -> None:
        self.minimum_length = minimum_length

    async def check(self, msg: MessageUpdate) -> bool:
        text = msg.text or msg.caption

        if not text:
            return False
        return self.minimum_length >= len(text)


try:
    from Levenshtein import distance as lev_distance
except ImportError:
    lev_distance = None


class Levenshtein(ABCRule[MessageUpdate]):
    """
    A rule that computes the Levenshtein distance between two strings
    and then compares it to the given maximum distance.
    """

    def __init__(
        self, levenshtein_texts: Union[str, List[str]], max_distance: Optional[int] = 1
    ) -> None:
        if lev_distance is None:
            raise SystemExit(
                "You must install `levenshtein` package to be able "
                "to use Levenshtein rule"
            )

        if isinstance(levenshtein_texts, str):
            levenshtein_texts = [levenshtein_texts]

        self.levenshtein_texts = levenshtein_texts
        self.max_distance = max_distance

    async def check(self, msg: MessageUpdate) -> bool:
        text = msg.text or msg.caption

        if not text:
            return False

        return any(
            lev_distance(text, levenshtein_text) <= self.max_distance
            for levenshtein_text in self.levenshtein_texts
        )


class Regex(ABCRule[MessageUpdate]):
    """
    A rule that checks if the message text matches the given regex.
    """

    def __init__(self, regex: str) -> None:
        self.regex = compile(regex)

    async def check(self, msg: MessageUpdate) -> bool:
        text = msg.text or msg.caption

        if not text:
            return False
        return self.regex.match(text) is not None


class Text(ABCRule[MessageUpdate]):
    """
    A rule that checks if the message text is equal
    to or is in the list of given texts.
    """

    def __init__(
        self, texts: Union[str, List[str]], ignore_case: Optional[bool] = False
    ) -> None:
        if not isinstance(texts, list):
            texts = [texts]

        self.texts = texts
        self.ignore_case = ignore_case

    async def check(self, msg: MessageUpdate) -> bool:
        text = msg.text or msg.caption

        if not text:
            return False

        if self.ignore_case:
            return text.lower() in list(map(str.lower, self.texts))
        return text in self.texts


try:
    import vbml
except ImportError:
    vbml = None


class VBML(ABCRule[MessageUpdate]):
    """
    This rule matches message text against a list of given patterns
    using the VBML library. See more details at https://github.com/tesseradecade/vbml
    """

    PatternLike = Union[str, "vbml.Pattern"]

    def __init__(
        self,
        patterns: Union[PatternLike, Iterable[PatternLike]],
        patcher: Optional["vbml.Patcher"] = None,
    ) -> None:
        if not isinstance(patterns, list):
            patterns = [patterns]

        self.patterns = [
            vbml.Pattern(pattern) if isinstance(pattern, str) else pattern
            for pattern in patterns
        ]
        self.patcher = patcher or vbml.Patcher()

    async def check(self, msg: MessageUpdate) -> bool:
        for pattern in self.patterns:
            result = self.patcher.check(pattern, msg.text)
            if result not in (None, False):
                return result
        return False
