import logging
import os

logger = logging.getLogger(__name__)


def check_env_variable_defined(key_name: str) -> bool:
    """Check if an environment variable exists and has a non-null value."""
    return bool(os.getenv(key_name))


def check_env_variables() -> None:
    """Check environment variables"""
    keys_to_check = [
        "DATABASE_HOST",
        "DATABASE_PORT",
        "DATABASE_NAME",
        "DATABASE_USER",
        "DATABASE_PASSWORD",
    ]
    missing_keys = [key for key in keys_to_check if not check_env_variable_defined(key)]

    if missing_keys:
        error_msg = f"Missing or empty environment variables: {', '.join(missing_keys)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
