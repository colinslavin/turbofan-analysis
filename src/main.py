from src.load_data import load_train_data
from src.preprocess import add_health_flag, zscore_relative_to_healthy
from src.analysis import (
    rank_early_warning_sensors,
    compute_composite_health_score,
    add_rolling_health_score,
    sensor_alarm_summary,
)
from src.visualize import plot_sensor_with_threshold, plot_health_score
from src.config import (
    DRIFT_SENSORS, HEALTHY_CUTOFF, Z_THRESHOLD,
    ROLL_WINDOW, SUSTAIN_COUNT
)

def main():
    df = load_train_data('data/train_FD001.txt')

    df = add_health_flag(df, HEALTHY_CUTOFF)
    df = zscore_relative_to_healthy(df, DRIFT_SENSORS)

    ranking = rank_early_warning_sensors(
        df, DRIFT_SENSORS, Z_THRESHOLD,
        roll_window=ROLL_WINDOW,
        sustain_count=SUSTAIN_COUNT
    )
    print(ranking.head(10).to_string(index=False))

    summary = sensor_alarm_summary(
        df,
        DRIFT_SENSORS,
        Z_THRESHOLD,
        roll_window=ROLL_WINDOW,
        sustain_count=SUSTAIN_COUNT
    )

    print("\nSensor alarm summary (sustained alarms):")
    print(summary.head(10).to_string(index=False))

    df = compute_composite_health_score(df, DRIFT_SENSORS)
    df = add_rolling_health_score(df, ROLL_WINDOW)

    # Quick visuals (same as before)
    plot_sensor_with_threshold(df, engine_id=1, sensor='sensor_13', z_threshold=Z_THRESHOLD)
    plot_health_score(df, engine_id=1)

if __name__ == "__main__":
    main()
