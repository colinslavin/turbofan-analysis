# Centralized constants so your assumptions are easy to audit/tune.

DRIFT_SENSORS = [
    'sensor_2','sensor_3','sensor_4','sensor_7','sensor_8','sensor_9',
    'sensor_11','sensor_12','sensor_13','sensor_14','sensor_15',
    'sensor_17','sensor_20','sensor_21'
]

# Define "healthy" as far from failure (in remaining cycles)
HEALTHY_CUTOFF = 150

# Z-score threshold for "significant deviation"
Z_THRESHOLD = 2.0

# How many initial cycles to ignore (optional; sometimes cycle 1 is noisy)
MIN_CYCLE = 1

ROLL_WINDOW = 5        # rolling window length (cycles)
SUSTAIN_COUNT = 3      # require >= this many threshold hits within the window
