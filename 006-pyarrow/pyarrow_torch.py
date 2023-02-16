import random
import sys
from bisect import bisect_right
from typing import Iterator, Optional, Tuple, List

import pyarrow as pa
import pandas as pd
from pyarrow.dataset import ParquetFileFragment
from pyarrow.lib import RecordBatch
from pyarrow.parquet import ParquetDataset, ParquetFile
from torch.utils.data import Dataset


class PyArrowDataset(Dataset):
    def __init__(self, source: str, shuffle: bool = False, seed: int = 123):
        random.seed(seed)
        self.source = source
        self.seed = seed

        # Pyarrow
        self.dataset = ParquetDataset(source, use_legacy_dataset=False)
        self.parquet_indices: List[Tuple[int, int, int, ParquetFile, int, int]] = []
        self._cur_meta = None
        self._df: Optional[pd.DataFrame] = None

        # Debug (Memory Profiling)
        self.read_cnt = 0

        self.init_parquet_indexing(shuffle)

    def init_parquet_indexing(self, shuffle: bool = False):
        fragments = self.dataset.fragments
        if shuffle:
            random.shuffle(fragments)

        idx = 0
        parquet_indices = []
        for frag in fragments:
            parquet_file = ParquetFile(frag.path)
            for i, row_group in enumerate(frag.row_groups):
                start_idx = idx  # inclusive
                end_idx = idx + row_group.num_rows  # exclusive
                parquet_indices.append((i, start_idx, end_idx, parquet_file, row_group.id, row_group.num_rows))
                idx += row_group.num_rows

        self.parquet_indices.clear()
        self.parquet_indices = parquet_indices

    def __len__(self):
        if not self.parquet_indices:
            return 0
        return self.parquet_indices[-1][-1]

    def __getitem__(self, idx: int):
        meta_idx = self._binary_search(idx)

        if self._cur_meta is not None and meta_idx == self._cur_meta[0]:
            start_idx = self._cur_meta[1]
            # print(f'total: {len(self)} | {idx - start_idx}')
            assert (idx - start_idx) >= 0, f'{idx} - {start_idx} = {idx - start_idx} <- should not be negative.'
            return self._df.iloc[idx - start_idx]

        # Clear memory references
        del self._df
        del self._cur_meta
        self.read_cnt += 1
        # Read a new Parquet File
        self._cur_meta = self.parquet_indices[meta_idx]
        start_idx = self._cur_meta[1]
        parquet_file = self._cur_meta[3]
        row_id = self._cur_meta[4]
        table: pa.Table = parquet_file.read_row_group(row_id)
        self._df = table.to_pandas()

        return self._df.iloc[idx - start_idx]

    def _binary_search(self, target: int):
        arr = self.parquet_indices
        n = len(arr)
        left, right = 0, n

        while left <= right:
            mid = (left + right) // 2
            _, start_idx, end_idx, _, _, _ = arr[mid]
            if target == start_idx:
                return mid
            elif target == end_idx:
                return mid + 1
            elif start_idx <= target < end_idx:
                return mid
            elif target <= end_idx:
                right = mid - 1
            else:
                left = mid + 1
        return left
