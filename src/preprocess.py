import pandas as pd
from typing import List

def add_health_flag(df: pd.DataFrame, healthy_cutoff: int) -> pd.DataFrame:
    """
    Adds is_healthy based on cycles_to_failure.
    """
    out = df.copy()
    out['is_healthy'] = out['cycles_to_failure'] > healthy_cutoff
    return out

def zscore_relative_to_healthy(
    df: pd.DataFrame,
    sensors: List[str],
    healthy_col: str = 'is_healthy'
) -> pd.DataFrame:
    """
    Per-engine normalization:
      z = (x - mean_healthy_engine) / std_healthy_engine

    Uses only rows where df[healthy_col] is True to compute mean/std per engine.
    Falls back to per-engine overall mean/std if healthy window is missing or std=0.
    """
    out = df.copy()

    # Precompute per-engine fallback stats over ALL rows
    all_mu = out.groupby('engine_id')[sensors].mean()
    all_sigma = out.groupby('engine_id')[sensors].std()

    # Compute per-engine stats over HEALTHY rows
    healthy = out[out[healthy_col]].copy()
    healthy_mu = healthy.groupby('engine_id')[sensors].mean()
    healthy_sigma = healthy.groupby('engine_id')[sensors].std()

    for s in sensors:
        # Map healthy stats onto each row by engine_id
        mu = out['engine_id'].map(healthy_mu[s])
        sigma = out['engine_id'].map(healthy_sigma[s])

        # Where healthy stats are missing/invalid, use fallback (all rows)
        mu_fallback = out['engine_id'].map(all_mu[s])
        sigma_fallback = out['engine_id'].map(all_sigma[s])

        mu = mu.fillna(mu_fallback)

        # sigma: fill NaNs, then avoid divide-by-zero
        sigma = sigma.fillna(sigma_fallback)

        # If sigma is still 0 or NaN (totally flat), set z-score to 0
        denom = sigma.replace(0, pd.NA)

        z = (out[s] - mu) / denom
        out[s] = z.fillna(0.0)

    return out
