import pytest
import yaml

from pathlib import Path
from vertrag.storage import (
    OrdersStore,
    PositionsStore,
    ContractsStore,
    AssetsStore,
)

@pytest.fixture
def test_order():
    return yaml.safe_load("test: [1,2,3]")

def test_yaml_stores(tmp_path, test_order):
    for Store in [OrdersStore, PositionsStore, ContractsStore]:
        store_path = tmp_path / Store.key
    if not store_path.is_dir():
        store_path.mkdir()
    store = Store(Store.key, tmp_path)
    store["test_order"] = test_order
    assert store["test_order"] == test_order
