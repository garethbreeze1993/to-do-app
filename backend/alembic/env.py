import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

try:
    from app.config import settings

except Exception:
    database_username = os.getenv('DATABASE_USERNAME', 'POSTGRES')
    database_password = os.getenv('DATABASE_PASSWORD', '<PASSWORD>')
    database_hostname = os.getenv('DATABASE_HOSTNAME', 'localhost')
    database_port = os.getenv('DATABASE_PORT', '5432')
    database_name = os.getenv('DATABASE_NAME', 'postgres')

else:
    database_username = settings.database_username
    database_password = settings.database_password
    database_hostname = settings.database_hostname
    database_port = settings.database_port
    database_name = settings.database_name

from app.models import Base  # Need to import from here so alembic can read from the models file

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override sqlalchemyurl from alembic.ini file so can use env variables not hardcoded when env is set up
config.set_main_option("sqlalchemy.url",
                       f"postgresql://{database_username}:{database_password}"
                       f"@{database_hostname}:{database_port}/{database_name}")


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
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


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
