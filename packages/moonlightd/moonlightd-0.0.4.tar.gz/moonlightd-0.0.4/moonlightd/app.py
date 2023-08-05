#!/usr/bin/env python
# -----------------------------------------------------------------------------
# moonlightd [moonlightd]
# (C) 2022 A. Shavykin <0.delameter@gmail.com>
# -----------------------------------------------------------------------------
import logging
import os
import sys
import time
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler

from telegram.ext import Application

from .handler import HANDLERS

log_level = os.getenv("LOG_LEVEL", "INFO")
stdout_log_level = "INFO"

formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)-5.5s] [%(name)s] %(message)s"
)
handler_file = TimedRotatingFileHandler(
    os.getenv("LOGS_PATH", "/tmp/moonlightd.log"),
    "d",
    interval=1,
    backupCount=1,
)
handler_file.setFormatter(formatter)
handler_file.setLevel(log_level)
handler_stdout = StreamHandler(sys.stdout)
handler_stdout.setFormatter(formatter)
handler_stdout.setLevel(stdout_log_level)

logger = logging.getLogger()
logger.addHandler(handler_file)
logger.addHandler(handler_stdout)
logger.setLevel(log_level)

app_start_time = time.time()
logging.info(f"Initialized logging system, level {log_level}")


def main() -> None:
    application = Application.builder().token(os.getenv("TELEGRAM_API_KEY")).build()
    for handler in HANDLERS:
        application.add_handler(handler)

    application.run_polling()


if __name__ == "__main__":
    main()
