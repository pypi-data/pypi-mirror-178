"""Module to setup logging."""
import logging
from copy import deepcopy
from typing import Optional, TypedDict, cast


# pylint: disable=missing-class-docstring
class LoggingConfigDict(TypedDict):
    name: Optional[str]
    level: int
    console_output: bool
    console_level: int
    console_formatter: logging.Formatter
    file_name: Optional[str]
    file_mode: str
    file_level: int
    file_formatter: logging.Formatter


def get_logging_formatter(*tags) -> logging.Formatter:
    """Get a logging formatter string."""
    logging_tags = {
        "time": "%(asctime)s",
        "module": "%(name)-12s",
        "file": "%(filename)s",
        "function": "%(funcName)-12s",
        "level": "%(levelname)-12s",
    }

    if not tags:
        _tags: tuple[str, ...] = ("time", "module", "file", "function", "level")
    else:
        _tags = tags

    tag_strings: list[str] = []

    for tag in _tags:
        tag_strings.append(logging_tags[tag])

    formatter_str = " : ".join(tag_strings) + " :: %(message)s"

    formatter = logging.Formatter(formatter_str)

    return formatter


DEFAULT_CONFIG: LoggingConfigDict = {
    "name": None,
    "level": logging.DEBUG,
    "console_output": True,
    "console_level": logging.INFO,
    "console_formatter": get_logging_formatter("time", "level"),
    "file_name": None,
    "file_mode": "a",
    "file_level": logging.INFO,
    "file_formatter": get_logging_formatter(),
}


def get_logging_config(input_config: Optional[dict] = None) -> LoggingConfigDict:
    """Get logging configuration.

    The logging configuration is the default config given at this
    module level, but each option can be overriden by the input
    configuration parameter.
    """
    # Cover case where no input configuration is given.
    if input_config is None:
        return deepcopy(DEFAULT_CONFIG)

    # Initialize result configuration.
    result_config = {}

    # Get given/default result_config for each parameter.
    for key, default_config_val in DEFAULT_CONFIG.items():
        if key in input_config:
            result_config[key] = input_config[key]
        else:
            result_config[key] = default_config_val

    return cast(LoggingConfigDict, result_config)


def get_logger(config: Optional[dict] = None) -> logging.Logger:
    """Get a python logger."""
    if config is None:
        _config = {}
    else:
        _config = config

    # Parse configuration.
    parsed_config: LoggingConfigDict = get_logging_config(_config)

    # Get logger by name (if it doesn't exists, it is created).
    logger = logging.getLogger(parsed_config["name"])

    # Set logger level.
    logger.setLevel(parsed_config["level"])

    # Setup console logging if enabled.
    if parsed_config["console_output"]:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(parsed_config["console_level"])
        console_formatter = parsed_config["console_formatter"]
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # Setup file logging as well, but only if there is a filename.
    if parsed_config["file_name"]:
        file_handler = logging.FileHandler(
            parsed_config["file_name"],
            mode=parsed_config["file_mode"],
        )
        file_handler.setLevel(parsed_config["file_level"])
        formatter = parsed_config["file_formatter"]
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
