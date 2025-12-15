from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

def _column_names():
    return (
        ['engine_id', 'cycle'] +
        [f'op_setting_{i}' for i in range(1, 4)] +
        [f'sensor_{i}' for i in range(1, 22)]
    )

def load_train_data(rel_path: str) -> pd.DataFrame:
    path = BASE_DIR / rel_path
    df = pd.read_csv(path, sep=r'\s+', header=None, names=_column_names())

    max_cycles = df.groupby('engine_id')['cycle'].max()
    df['cycles_to_failure'] = df.apply(
        lambda r: int(max_cycles.loc[r.engine_id] - r.cycle),
        axis=1
    )
    return df

def load_test_data(path: str) -> pd.DataFrame:
    """
    Load test data (no failure observed in file).
    RUL labels come from separate file.
    """
    df = pd.read_csv(
        path,
        sep=r'\s+',
        header=None,
        names=_column_names()
    )
    return df

def load_rul_labels(path: str) -> pd.Series:
    """
    Load remaining useful life (RUL) labels for each engine in test set.
    """
    rul = pd.read_csv(path, sep=r'\s+', header=None).iloc[:, 0]
    return rul
