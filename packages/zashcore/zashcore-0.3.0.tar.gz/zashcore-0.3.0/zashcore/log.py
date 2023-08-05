import os
import structlog
import logging
import sys
from operator import attrgetter


def get_logger() -> structlog.stdlib.BoundLogger:
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M.%S"),
        structlog.processors.StackInfoRenderer(),
    ]
    level = attrgetter(os.getenv("LOG_LEVEL", "INFO"))(logging)
    if sys.stderr.isatty():
        # Pretty printing when we run in a terminal session / in local development env.
        # Automatically prints pretty tracebacks when "rich" is installed
        processors = shared_processors + [structlog.dev.ConsoleRenderer()]
        structlog.configure(
            processors=processors,
            context_class=dict,
            cache_logger_on_first_use=True,
            wrapper_class=structlog.make_filtering_bound_logger(level),
        )
    else:
        # Print JSON when we run, e.g., in a Docker container.
        # Also print structured tracebacks.
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]
        structlog.configure(
            processors,
            wrapper_class=structlog.make_filtering_bound_logger(level),
            cache_logger_on_first_use=True,
        )
    return structlog.get_logger()
