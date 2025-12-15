# Turbofan Engine Degradation Monitoring

Early Failure Detection with Sustained Alarms and Composite Health Scoring

## Overview
This project builds a decision-grade monitoring pipeline to detect early-stage degradation in complex systems using multi-sensor time-series data. Instead of relying on single threshold crossings, the system emphasizes sustained deviation, per-engine normalization, and composite risk scoring to balance early detection against false positives.

The output is an interpretable monitoring approach with explicit warning-time distributions and false-positive guarantees.

## Dataset
NASA C-MAPSS Turbofan Engine Dataset (FD001).

Each engine is run to failure.  
Each row represents one operating cycle.  
The dataset includes operational settings and 21 sensor channels.

Failure timing is known for the training data. Remaining useful life is computed as the difference between an engine’s final cycle and the current cycle.

## Problem Framing
The goal is not prediction for its own sake, but early and reliable warning.

Key questions:
- Which sensors provide early signals of degradation?
- How early can failure be detected consistently?
- How can false positives during healthy operation be avoided?
- Can a single composite metric outperform individual sensors?

## Approach

Healthy baseline normalization:
Sensor values vary significantly across engines. A healthy operating window is defined as cycles far from failure. Each sensor is normalized per engine using z-scores relative to its healthy behavior. This ensures deviations represent degradation rather than unit differences.

Sustained sensor alarms:
Single threshold crossings are noisy and unrealistic. A sustained alarm is defined as N out of M recent cycles exceeding a z-score threshold. This removes spurious triggers and produces interpretable alarms.

Sensor-level evaluation:
For each sensor, the first sustained alarm time is recorded per engine. Warning-time distributions are summarized using the 25th percentile, median, and 75th percentile. Sensors are ranked by median warning time and consistency.

Composite health score:
A composite health score is defined as the mean absolute normalized deviation across drifting sensors. The score is smoothed using a rolling window and monitored with sustained alarm logic. This acts as the primary system-level alarm.

False-positive control:
False positives are explicitly measured by evaluating alarm rates during healthy operation. Thresholds are chosen to keep healthy false positives below two percent.

## Key Results

Sensor-level alarms:
The earliest sensors provide roughly 95 cycles of median warning time. Some sensors alarm early but inconsistently, while others alarm later but across nearly all engines.

Composite alarm:
The composite alarm provides a median warning time of approximately 81 cycles before failure. The interquartile range is roughly 71 to 92 cycles. All engines are detected. The healthy false-positive rate is zero percent.

The composite alarm is more reliable than any individual sensor while remaining early enough for intervention.

## How to Run
From the project root, run:

python -m src.main

This loads the data, computes sensor-level and composite alarms, prints summary tables, and produces representative plots.

## Repository Structure
src/load_data.py handles data loading and RUL labeling.  
src/preprocess.py handles healthy baseline normalization.  
src/analysis.py implements sustained alarms and summaries.  
src/visualize.py contains plotting utilities.  
src/config.py defines thresholds and design choices.  
src/main.py runs the end-to-end pipeline.

## Design Philosophy
This project prioritizes interpretability over black-box prediction, sustained evidence over single-point triggers, and explicit tradeoffs between sensitivity and false alarms. Outputs are designed to support real monitoring decisions rather than retrospective analysis.

## Next Steps
Possible extensions include applying the framework to test data, comparing composite alarms to individual sensors, and evaluating robustness across operating regimes.
