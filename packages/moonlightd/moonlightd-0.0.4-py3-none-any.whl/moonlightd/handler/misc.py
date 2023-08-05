import html
import logging
import re
import typing
from abc import ABC, abstractmethod

import requests
from telegram import Update
from telegram.constants import MessageLimit

from ..common import fmt_bold, fmt_code, fmt_italic
from ._base import (
    _GenericCommandHandler,
    CTX_DEFAULT,
    ApiError,
    NEWLINE_REPLACER,
    EmptyResponseError,
)


class _WeatherGenericCommandHandler(_GenericCommandHandler, ABC):
    HIDDEN_RESPONSE_HTTP_STATUSES = [
        404,
    ]
    PAD = 2 * " "

    _URL_TEMPLATE = "http://v2.wttr.in/%s?FTM"
    _USER_AGENT = "curl"
    _WTTR_TIMEOUT_SEC = 10
    _DEFAULT_LOCATION = "Moscow"

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(__name__)

    def _handle(self, upd: Update, ctx: CTX_DEFAULT) -> tuple[str | None, ...]:
        location = self._get_location(upd)
        try:
            raw_data = self._fetch_wttrin_data(location)
        except ApiError as e:
            return e.msg,

        extract_data_gen = self._extract_data(raw_data)
        result = self._process_data(extract_data_gen)
        if not result or result.isspace():
            limit = MessageLimit.TEXT_LENGTH
            result = raw_data[: min(max(1, len(raw_data)), limit)]

        return result,

    def _get_location(self, upd: Update) -> str:
        if len(argv := re.split(r"\s", upd.message.text)) >= 2:
            return " ".join(argv[1:])
        return self._DEFAULT_LOCATION

    def _fetch_wttrin_data(self, location: str) -> str:
        try:
            url = self._URL_TEMPLATE % location
            headers = {"User-Agent": self._USER_AGENT}
            response = requests.get(url, headers, timeout=self._WTTR_TIMEOUT_SEC)

            if response.ok and len(response.text) == 0:
                raise EmptyResponseError()

        except Exception as e:
            eqn = e.__class__.__qualname__
            self._logger.error(f"Failed to retrieve weather: {e})")
            raise ApiError(f"Failed to retrieve weather: {eqn}") from e

        self._logger.debug("Response: " + NEWLINE_REPLACER.apply(response.text))
        if response.ok:
            return response.text

        msg = "Remote service failure: "
        msg += f"HTTP {response.status_code} ({response.reason})."
        if response.status_code not in self.HIDDEN_RESPONSE_HTTP_STATUSES:
            response_lines = response.text.lstrip().splitlines()
            if len(response_lines) and len(response_lines[0]):
                msg += "\nResponse: " + response_lines[0]
                if len(response_lines) > 1:
                    msg += " [...]"
        self._logger.error(msg)
        raise ApiError(msg)

    @abstractmethod
    def _get_field_index(self) -> dict[str, int]:
        raise NotImplementedError

    @abstractmethod
    def _get_field_icon(self, label: str) -> str:
        raise NotImplementedError

    def _extract_data(self, raw_data: str) -> typing.Iterable[tuple[str, str]]:
        field_keys = self._get_field_index().keys()
        field_keys_str = "|".join(field_keys)
        regex = rf"\s*({field_keys_str}):\s*(.+)$"

        split_data = raw_data.replace(" | ", "\n").strip().splitlines()
        filtered_data = {
            match.group(1): match.group(2)
            for match in [re.search(regex, line) for line in split_data]
            if match
        }

        for field in field_keys:
            if field in filtered_data.keys():
                yield field, filtered_data[field]

    def _process_data(self, extract_data_gen: typing.Iterable[tuple[str, str]]) -> str:
        field_index = self._get_field_index()
        line_index: list[str] = [""] * (1 + max(field_index.values()))

        for (field, value) in extract_data_gen:
            value = html.escape(value)
            primary = fmt_bold(r"\1")
            match field:
                case "Location":
                    coords_repl = fmt_code("[") + fmt_code(r"\1") + fmt_code("]")
                    result = re.sub(r"^(.+?)(?=$|,|\[)", primary, value)
                    result = re.sub(r"\[([\d,.-]+)]", coords_repl, result)
                case "Weather":
                    result = re.sub(r"\s+", " ", value).replace(",", 3 * " ")
                    result = re.sub(r"(\S+°C)", primary, result)
                case "Now":
                    pattern: re.Pattern = re.compile(r"^(.+?)([+-]\d{4})")
                    repl = primary + self.PAD + fmt_italic(r"(\2,")
                    result = pattern.sub(repl, value)
                case "Timezone":
                    result = fmt_italic(" " + value + ")")
                case "Dawn" | "Sunrise" | "Sunset" | "Dusk":
                    icon = self._get_field_icon(field) + " "
                    label_str = fmt_bold(field) + ":"
                    result = icon + label_str + self.PAD + fmt_code(value)
                case _:
                    continue
            line_index[field_index[field]] += result

        return "\n".join(line_index)


class WeatherCommandHandler(_WeatherGenericCommandHandler):
    _COMMAND_NAME = "weather"
    _COMMAND_SHORT_HELP = "show current weather in specified location"
    _COMMAND_HELP = (
        f"/{_COMMAND_NAME} [LOCATION]\n"
        'Show current weather in LOCATION [default: "Moscow"]. '
        'Accepts various location formats, e.g. "MSK", "Москва".',
    )

    def _get_field_index(self) -> dict[str, int]:
        """ "label" -> "target line no" map"""
        return {
            "Location": 0,
            "Now": 1,
            "Timezone": 1,
            "Weather": 3,
        }

    def _get_field_icon(self, label: str) -> str:
        return ""


class SunCommandHandler(_WeatherGenericCommandHandler):
    _COMMAND_NAME = "sun"
    _COMMAND_SHORT_HELP = "show sunrise/sunset times in specified location"
    _COMMAND_HELP = (
        f"/{_COMMAND_NAME} [LOCATION]\n"
        'Show current sun times in LOCATION [default: "Moscow"]. '
        'Accepts various location formats, e.g. "MSK", "Москва".'
    )

    _LABEL_ICONS_MAP = {
        "Dawn": "🌃",
        "Sunrise": "🌅",
        "Sunset": "🌇",
        "Dusk": "🌉",
    }

    def _get_field_index(self) -> dict[str, int]:
        """ "label" -> "target line no" map"""
        return {
            "Location": 0,
            "Now": 1,
            "Timezone": 1,
            "Dawn": 3,
            "Sunrise": 4,
            "Sunset": 5,
            "Dusk": 6,
        }

    def _get_field_icon(self, label: str) -> str:
        return self._LABEL_ICONS_MAP.get(label, "?")
