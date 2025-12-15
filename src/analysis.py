import pandas as pd
from typing import List, Optional

def _first_sustained_alarm_ctf(
    g: pd.DataFrame,
    col: str,
    z_threshold: float,
    roll_window: int,
    sustain_count: int
) -> Optional[float]:
    """
    For a single engine dataframe g:
    sustained alarm = at least `sustain_count` exceedances in the last
    `roll_window` cycles where |z| > z_threshold.

    Returns cycles_to_failure at the first sustained alarm time, or None.
    """
    g = g.sort_values('cycle').reset_index(drop=True)

    exceed = (g[col].abs() > z_threshold).astype(int)
    hits = exceed.rolling(roll_window, min_periods=roll_window).sum()

    alarm_pos = hits[hits >= sustain_count].index
    if len(alarm_pos) == 0:
        return None

    first_pos = int(alarm_pos[0])
    return float(g.loc[first_pos, 'cycles_to_failure'])


def rank_early_warning_sensors(
    df: pd.DataFrame,
    sensors: List[str],
    z_threshold: float,
    roll_window: int = 5,
    sustain_count: int = 3
) -> pd.DataFrame:
    """
    Rank sensors by how EARLY they provide a sustained alarm.
    median_warning_cycles: median cycles_to_failure at first sustained alarm.
      - higher => earlier warning (better)
    engines_with_alarm: how many engines ever triggered sustained alarm.
    """
    rows = []

    for s in sensors:
        alarms = []
        for _, g in df.groupby('engine_id'):
            ctf = _first_sustained_alarm_ctf(g, s, z_threshold, roll_window, sustain_count)
            if ctf is not None:
                alarms.append(ctf)

        rows.append({
            "sensor": s,
            "median_warning_cycles": float(pd.Series(alarms).median()) if alarms else None,
            "engines_with_alarm": int(len(alarms))
        })

    out = pd.DataFrame(rows)
    out = out.sort_values('median_warning_cycles', ascending=False, na_position='last')
    return out


def compute_composite_health_score(
    df: pd.DataFrame,
    sensors: List[str]
) -> pd.DataFrame:
    """
    Composite risk score: mean absolute z across chosen sensors.
    Higher score => farther from healthy baseline.
    """
    out = df.copy()
    out['health_score'] = out[sensors].abs().mean(axis=1)
    return out


def add_rolling_health_score(
    df: pd.DataFrame,
    roll_window: int = 5
) -> pd.DataFrame:
    """
    Rolling mean of composite health score to reduce spiky false alarms.
    """
    out = df.copy()
    out['health_score_roll'] = out.groupby('engine_id')['health_score'].transform(
        lambda s: s.rolling(roll_window, min_periods=roll_window).mean()
    )
    return out

def sensor_alarm_summary(df, sensors, z_threshold, roll_window, sustain_count):
    rows = []
    for s in sensors:
        alarms = []
        for _, g in df.groupby('engine_id'):
            ctf = _first_sustained_alarm_ctf(g, s, z_threshold, roll_window, sustain_count)
            if ctf is not None:
                alarms.append(ctf)
        ser = pd.Series(alarms)
        rows.append({
            "sensor": s,
            "p25_warning": float(ser.quantile(0.25)) if len(ser) else None,
            "median_warning": float(ser.median()) if len(ser) else None,
            "p75_warning": float(ser.quantile(0.75)) if len(ser) else None,
            "engines_with_alarm": len(alarms)
        })
    return pd.DataFrame(rows).sort_values("median_warning", ascending=False, na_position="last")
