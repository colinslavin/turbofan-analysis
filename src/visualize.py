import pandas as pd
import matplotlib.pyplot as plt
from typing import List

def plot_sensor_engine(df: pd.DataFrame, engine_id: int, sensor: str) -> None:
    g = df[df['engine_id'] == engine_id].sort_values('cycle')
    plt.figure()
    plt.plot(g['cycle'], g[sensor])
    plt.xlabel('Cycle')
    plt.ylabel(sensor)
    plt.title(f'{sensor} vs Cycle (Engine {engine_id})')
    plt.show()

def plot_sensor_with_threshold(df: pd.DataFrame, engine_id: int, sensor: str, z_threshold: float) -> None:
    g = df[df['engine_id'] == engine_id].sort_values('cycle')
    plt.figure()
    plt.plot(g['cycle'], g[sensor])
    plt.axhline(z_threshold, linestyle='--')
    plt.axhline(-z_threshold, linestyle='--')
    plt.xlabel('Cycle')
    plt.ylabel(f'{sensor} (z-score)')
    plt.title(f'{sensor} w/ Threshold (Engine {engine_id})')
    plt.show()

def plot_health_score(df: pd.DataFrame, engine_id: int) -> None:
    g = df[df['engine_id'] == engine_id].sort_values('cycle')
    plt.figure()
    plt.plot(g['cycle'], g['health_score'])
    plt.xlabel('Cycle')
    plt.ylabel('Health Score (mean |z|)')
    plt.title(f'Composite Health Score (Engine {engine_id})')
    plt.show()
