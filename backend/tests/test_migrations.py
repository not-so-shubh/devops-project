from alembic.config import Config
from sqlalchemy import create_engine, inspect

from alembic import command


def test_migration_round_trip_and_metadata(tmp_path):
    config = Config("alembic.ini")
    url = f"sqlite:///{tmp_path}/migration_test.db"
    config.set_main_option("sqlalchemy.url", url)
    command.upgrade(config, "head")
    engine = create_engine(url)
    assert {"products", "stock_movements"} <= set(inspect(engine).get_table_names())
    command.check(config)
    command.downgrade(config, "base")
    assert "products" not in inspect(engine).get_table_names()
    command.upgrade(config, "head")
    assert "stock_movements" in inspect(engine).get_table_names()
    engine.dispose()
