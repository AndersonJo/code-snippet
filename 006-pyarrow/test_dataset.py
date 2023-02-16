from datetime import datetime, timedelta
from pathlib import Path
from plistlib import Data

import pandas as pd
import pyarrow as pa
from torch.utils.data import DataLoader

from pyarrow_torch import PyArrowDataset


def test_dataset():
    create_data()

    dataset = CustomDataset("./data")
    assert dataset[50000] == 50000
    assert dataset.read_cnt == 1

    assert dataset[0] == 0
    assert dataset.read_cnt == 2

    assert dataset[500000] == 500000
    assert dataset.read_cnt == 3

    assert dataset[100] == 100
    assert dataset.read_cnt == 4

    assert dataset[32768] == 32768
    assert dataset.read_cnt == 5

    assert dataset[32767] == 32767
    assert dataset.read_cnt == 6

    assert dataset[32769] == 32769
    assert dataset.read_cnt == 7

    assert dataset[32770] == 32770
    assert dataset.read_cnt == 7

    assert dataset[32771] == 32771
    assert dataset.read_cnt == 7

    assert dataset[8000000] == 8000000
    assert dataset.read_cnt == 8

    assert dataset[8000001] == 8000001
    assert dataset.read_cnt == 8


def test_dataloader_batch():
    dataset = CustomDataset("./data")
    loader = DataLoader(dataset, batch_size=2)
    for i, row in enumerate(loader):
        assert [i * 2, i * 2 + 1] == row.tolist()
        # assert i == row.item()

    i = 0
    for i, row in enumerate(loader):
        assert [i * 2, i * 2 + 1] == row.tolist()
    assert (i + 1) == len(loader)


def test_dataloader_workers():
    dataset = CustomDataset("./data")
    loader = DataLoader(dataset, batch_size=2, num_workers=8)
    for i, row in enumerate(loader):
        assert [i * 2, i * 2 + 1] == row.tolist()


def test_dataloader_random():
    dataset = CustomDataset("./data")
    loader = DataLoader(dataset, batch_size=10, shuffle=True, num_workers=2, pin_memory=True)
    total = set()
    for i, row in enumerate(loader):
        total |= set(row.tolist())
    assert len(total) == len(loader) * 10

    total = set()
    for i, row in enumerate(loader):
        total |= set(row.tolist())
    assert len(total) == len(loader) * 10


class CustomDataset(PyArrowDataset):

    def __getitem__(self, idx):
        row = super().__getitem__(idx)
        return row['idx']


def create_data():
    if not Path('./data').exists():
        df = pd.DataFrame({"idx": range(50000000)})
        dt = datetime(2023, 1, 1)
        df["dt"] = df["idx"].apply(
            lambda x: (dt + timedelta(milliseconds=x * 10)).date()
        )
        pa.parquet.write_to_dataset(
            pa.Table.from_pandas(df),
            root_path="data",
            partition_cols=["dt"],
            use_legacy_dataset=False,
        )
