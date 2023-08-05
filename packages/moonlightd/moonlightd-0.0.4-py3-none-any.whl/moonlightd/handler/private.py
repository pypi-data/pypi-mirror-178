import html
import os
import re
import time

import pytermor as pt
from telegram import Update

from ._base import _GenericCommandHandler, CTX_DEFAULT


class IdCommandHandler(_GenericCommandHandler):
    _COMMAND_NAME = "_id"

    def _handle(self, upd: Update, ctx: CTX_DEFAULT) -> tuple[str | None, ...]:
        from ..app import app_start_time

        uname = os.uname()
        uptime = time.time() - app_start_time

        msg = ""
        fields = {
            "Uptime": pt.utilnum.format_time_delta(uptime),
            "ID": str(ctx.bot.id),
            "Node": uname.nodename,
            "System": uname.sysname,
            "Release": uname.release,
            "Machine": uname.machine,
            "Version": re.sub(
                r" *\w{3} +\w{3} +\d{1,2} +[\d:]{8} +UTC +[\d]{4}", "", uname.version
            ),
        }
        for k, v in fields.items():
            msg += f"<b>{k}</b>:{self.PAD}<code>{html.escape(v)}</code>\n"

        return (msg,)
