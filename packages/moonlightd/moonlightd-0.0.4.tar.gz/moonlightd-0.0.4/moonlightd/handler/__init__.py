from ._base import (
    LoggingMessageHandler,
    InvalidCommandMessageHandler,
    HelpCommandHandler,
    StartCommandHandler, _GenericCommandHandler,
)
from .codepages import HolmesCommandHandler, WatsonCommandHandler
from .misc import SunCommandHandler, WeatherCommandHandler
from .private import IdCommandHandler

HANDLERS = [
    HelpCommandHandler(),
    StartCommandHandler(),
    HolmesCommandHandler(),
    WatsonCommandHandler(),
    IdCommandHandler(),
    SunCommandHandler(),
    WeatherCommandHandler(),
    LoggingMessageHandler(),
    InvalidCommandMessageHandler(),
]
HANDLER_MAP = {h.get_name(): h for h in HANDLERS if isinstance(h, _GenericCommandHandler)}

PUBLIC_COMMAND_GROUPS_MAP = {
    "codepages": [
        HolmesCommandHandler,
        WatsonCommandHandler,
    ],
    "misc": [
        SunCommandHandler,
        WeatherCommandHandler,
    ],
}
