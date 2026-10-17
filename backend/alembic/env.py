import os

from sqlalchemy import engine_from_config, pool

from alembic import context
from app import models  # noqa: F401
from app.db import Base

config = context.config
url = config.get_main_option("sqlalchemy.url") or os.environ["DATABASE_URL"]
# URL is supplied directly, avoiding ConfigParser interpolation of password percent signs.
target_metadata = Base.metadata

if context.is_offline_mode():
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    engine = engine_from_config(
        {"sqlalchemy.url": url}, prefix="sqlalchemy.", poolclass=pool.NullPool
    )
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()
