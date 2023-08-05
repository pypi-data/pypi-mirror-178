import html
import re
import unicodedata

from telegram import Update
from os.path import join, dirname, abspath

from telegram.constants import MessageLimit

from ..common import fmt_code, fmt_bold
from ..common import fmt_pre_block
from ._base import _GenericCommandHandler, CTX_DEFAULT


class HolmesCommandHandler(_GenericCommandHandler):
    _COMMAND_NAME = "holmes"
    _COMMAND_SHORT_HELP = "inspect Unicode character(s)"
    _COMMAND_SYNTAX = f"/{fmt_bold(_COMMAND_NAME)} [STRING]..."
    _COMMAND_HELP = (
        _COMMAND_SYNTAX + "\n"
        "Break input STRINGs down to separate characters "
        "and show Unicode details for each."
    )

    _DEMO_INPUT = "moоnlightd🌚"
    _CHAR_LIMIT = 50

    def _handle(self, upd: Update, ctx: CTX_DEFAULT) -> tuple[str | None, ...]:
        inp = self._DEMO_INPUT
        using_demo = True
        if len(argv := re.split(r"\s", upd.message.text, 1)) > 1:
            inp = " ".join(argv[1:])
            using_demo = False
        msg = ""

        for idx, char in enumerate(inp):
            if idx >= self._CHAR_LIMIT:
                break

            ucid = f"{ord(char):02X}"
            # utf8 = char.encode().hex()
            char = html.escape(char.replace("\n", " "))

            line = (
                fmt_code("U+" + ucid.rjust(5))
                + " │ "
                + fmt_code(char)
                + " │ "
                + f"{unicodedata.category(char)}: "
                + f"{unicodedata.name(char, f'(unnamed code point)')}"
                + "\n"
            )
            msg += line
            if len(msg) >= MessageLimit.TEXT_LENGTH - 2 * len(line):
                if idx < len(inp) - 1:
                    msg += "...[TRUNCATED]\n"
                break

        syntax_hint: str | None = None
        if using_demo:
            demo_str = fmt_code(self._DEMO_INPUT)
            syntax_hint = f'No args -- using demo input string "{demo_str}".\n'
            syntax_hint += "Custom input string can be provided as follows:\n"
            syntax_hint += self._COMMAND_SYNTAX
        return syntax_hint, msg


class WatsonCommandHandler(_GenericCommandHandler):
    _COMMAND_NAME = "watson"
    _COMMAND_SHORT_HELP = "display ASCII-7 codepage"
    _COMMAND_HELP = (
        f"/{_COMMAND_NAME}\n"
        "Print all 7-bit ASCII characters along with "
        "corresponding hexadecimal codes.",
    )

    _DATA_FILENAME = "codepage.ascii"

    def _handle(self, upd: Update, ctx: CTX_DEFAULT) -> tuple[str | None, ...]:
        with open(join(abspath(dirname(__file__)), self._DATA_FILENAME)) as f:
            data = f.read()
        return fmt_pre_block(html.escape(data)),
