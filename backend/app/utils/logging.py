import logging.config
import structlog
from pathlib import Path


def setup_logging():
    config_path = Path(__file__).resolve().parents[2] / "logging.ini"
    logging.config.fileConfig(config_path, disable_existing_loggers=False)

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
