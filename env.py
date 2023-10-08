from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import your SQLAlchemy Base instance and other necessary database components
from app.db import Base, DATABASE_URL

config = context.config
fileConfig(config.config_file_name)

# This should be correctly getting the metadata of your models.
target_metadata = Base.metadata

# Ensure your DATABASE_URL is correctly defined
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # The target_metadata is set here again to doubly ensure it's passed
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    raise NotImplementedError("Offline mode not supported")
else:
    run_migrations_online()
