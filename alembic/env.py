import os
from logging.config import fileConfig
from urllib.parse import quote_plus

import dotenv
import sqlalchemy.exc
from sqlalchemy import create_engine, engine_from_config, text, pool, URL
from sqlalchemy_utils import database_exists

from alembic import context
from app.models import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support

target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

dotenv.load_dotenv()
# Load individual environment variables
DATABASE_USER = os.getenv("DATABASE_USER", "")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
DATABASE_HOST = os.getenv("DATABASE_HOST", "")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_NAME = os.getenv("DATABASE_NAME", "")


encoded_password = quote_plus(DATABASE_PASSWORD).replace("%", "%%")

database_url = f"postgresql://{DATABASE_USER}:{encoded_password}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

config.set_main_option("sqlalchemy.url", database_url)


def create_database_if_not_exists():
    specific_url = URL.create(
        "postgresql",
        username=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        database=DATABASE_NAME,
    )

    default_url = URL.create(
        "postgresql",
        username=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        database="postgres",
    )

    engine = create_engine(
        url=specific_url,
        connect_args={
            "sslmode": "require",
        }
    )

    db_name = DATABASE_NAME

    if not database_exists(engine.url):
        print(f"Database {db_name} does not exist, creating...")
        try:
            engine_default = create_engine(
                url=default_url,
                connect_args={
                    "sslmode": "require",
                }
            )
            with engine_default.connect() as conn:
                # Disable autocommit
                conn.execute(text("COMMIT"))
                # Create the database
                conn.execute(text(f'CREATE DATABASE "{db_name}"'))
            print(f"Created database: {db_name}")
        except sqlalchemy.exc.ProgrammingError:
            print(f'Database "{db_name}" already exists')
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Database {db_name} exists")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    create_database_if_not_exists()

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
