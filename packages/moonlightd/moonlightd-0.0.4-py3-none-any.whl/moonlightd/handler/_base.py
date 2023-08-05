import logging
import os
import re
import time
from abc import ABC, abstractmethod

import pytermor as pt
from telegram import Update
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler

from ..common import fmt_bold, fmt_code

NO_EDIT = ~filters.UpdateType.EDITED_MESSAGE
CTX_DEFAULT = ContextTypes.DEFAULT_TYPE

NEWLINE_REPLACER = pt.utilstr.StringReplacer("\n", "↵")


class _GenericCommandHandler(CommandHandler, ABC):
    PAD = 2 * " "

    _COMMAND_NAME = None
    _COMMAND_SHORT_HELP = ""
    _COMMAND_HELP = ""

    def __init__(self):
        super().__init__(self.get_name(), self._wrapper, NO_EDIT)
        self._logger = logging.getLogger(__name__)
        self._duration_formatter = pt.utilnum.PrefixedUnitFormatter(
            max_value_len=4,
            truncate_frac=False,
            unit="s",
            unit_separator=" ",
            mcoef=1000.0,
            prefixes=pt.utilnum.PREFIXES_SI,
            prefix_zero_idx=pt.utilnum.PREFIX_ZERO_SI,
        )

    def get_name(self) -> str:
        return self._COMMAND_NAME

    def get_short_help(self) -> str:
        return self._COMMAND_SHORT_HELP

    def get_help(self) -> str:
        return self._COMMAND_HELP

    async def _wrapper(self, upd: Update, ctx: CTX_DEFAULT):
        self.log_start(upd)
        start_time = time.time_ns()

        result = self._handle(upd, ctx)
        end_time = time.time_ns()
        self.log_result(end_time - start_time, result)

        if not isinstance(result, tuple):
            result = (result,)
        if not result or all(r.isspace() for r in result):
            msg = f"Internal server error. Contact the developer"
            if author := os.getenv("AUTHOR"):
                msg += f": {author}"
            result = (msg,)

        for msg in result:
            await upd.message.reply_html(msg)

    @abstractmethod
    def _handle(self, upd: Update, ctx: CTX_DEFAULT) -> tuple[str | None, ...]:
        raise NotImplementedError

    def log_start(self, upd: Update):
        self._logger.info(
            f"Command from {_get_event_source(upd)}: '{upd.message.text}'"
        )

    def log_result(self, duration: int, result: tuple[str, ...]):
        self._logger.info(f"Done in {self._duration_formatter.format(duration*1e-9)}")
        for msg in result:
            self._logger.debug(f"Result: '{NEWLINE_REPLACER.apply(msg)}'")


class HelpCommandHandler(_GenericCommandHandler):
    _COMMAND_NAME = "help"

    def _handle(self, upd: Update, ctx: CTX_DEFAULT) -> tuple[str | None, ...]:
        from . import PUBLIC_COMMAND_GROUPS_MAP, HANDLER_MAP

        command_handler: _GenericCommandHandler | None = None
        if len(argv := re.split(r"\s", upd.message.text)) == 2:
            command_name = argv[1].lstrip("/")
            command_handler = HANDLER_MAP.get(command_name)

        if not command_handler:
            msg = ""
            for group_name, group in PUBLIC_COMMAND_GROUPS_MAP.items():
                msg += fmt_bold(group_name) + "\n"
                for command_handler_type in group:
                    command_handler = command_handler_type()
                    short_help = command_handler.get_short_help()
                    msg += f"  /{command_handler.get_name()} -- {short_help}\n"
                msg += "\n"
            msg += "Use /help COMMAND_NAME for the command details, e.g.: "
            msg += fmt_code("/help weather")
        else:
            msg = command_handler.get_help()

        return (msg,)


class StartCommandHandler(HelpCommandHandler):
    _COMMAND_NAME = "start"


class LoggingMessageHandler(MessageHandler):
    def __init__(self):
        super().__init__(~filters.COMMAND & NO_EDIT, self._wrapper)
        self._logger = logging.getLogger(__name__)

    async def _wrapper(self, upd: Update, ctx: CTX_DEFAULT):
        text = NEWLINE_REPLACER.apply(upd.message.text)
        self._logger.info(f"Message from {_get_event_source(upd)}: {text}")


class InvalidCommandMessageHandler(MessageHandler):
    def __init__(self):
        super().__init__(filters.COMMAND & NO_EDIT, self._wrapper)
        self._logger = logging.getLogger(__name__)

    async def _wrapper(self, upd: Update, ctx: CTX_DEFAULT):
        text = NEWLINE_REPLACER.apply(upd.message.text)
        self._logger.info(f"Bad command from {_get_event_source(upd)}: {text}")

        msg = "Invalid command. Run /help to see the command list."
        await upd.message.reply_html(msg)


class ApiError(Exception):
    def __init__(self, msg: str, *args: object) -> None:
        self.msg = msg
        super().__init__(*args)


class EmptyResponseError(ApiError):
    def __init__(self, *args: object) -> None:
        super().__init__("HTTP 200, but empty response", *args)


def _get_event_source(upd: Update):
    username = upd.effective_user.username
    chatname = upd.effective_chat.username
    username_str = f"@{username}"
    if chatname != username:
        return f":{chatname} {username_str}"
    return username_str
