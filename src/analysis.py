import pandas as pd
from typing import List, Dict, Tuple

def rank_early_warning_sensors(
    df: pd.DataFrame,
    sensors: List[str],
    z_threshold: float
) -> pd.DataFrame:
    """
    Ranks sensors by how early they tend to exceed |z| > threshold.
    Uses median cycles_to_failure at first 'alarm' per engine.
    Lower median cycles_to_failure -> later alarm.
    Higher median cycles_to_failure -> earlier alarm (more warning time).
    """
    rows = []

    for s in sensors:
        first_alarm_ctf = []

        for engine_id, g in df.groupby('engine_id'):
            g_sorted = g.sort_values('cycle')
            alarms = g_sorted[g_sorted[s].abs() > z_threshold]

            if len(alarms) == 0:
                continue

            # first time that engine trips threshold
            first_alarm = alarms.iloc[0]
            first_alarm_ctf.append(first_alarm['cycles_to_failure'])

        if len(first_alarm_ctf) == 0:
            rows.append((s, None, 0))
        else:
            rows.append((s, float(pd.Series(first_alarm_ctf).median()), len(first_alarm_ctf)))

    out = pd.DataFrame(rows, columns=['sensor', 'median_warning_cycles', 'engines_with_alarm'])
    out = out.sort_values('median_warning_cycles', ascending=False)  # bigger warning is better
    return out

def compute_composite_health_score(
    df: pd.DataFrame,
    sensors: List[str]
) -> pd.DataFrame:
    """
    Simple composite risk score: mean absolute z across chosen sensors.
    Higher score => farther from healthy baseline.
    """
    out = df.copy()
    out['health_score'] = out[sensors].abs().mean(axis=1)
    return out
