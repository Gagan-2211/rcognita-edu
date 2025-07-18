import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import glob

# Define Cost Matrices Q and R for Testing 
cost_sets = [
    {"Q": [50.0, 55.0, 80.0], "R": [10.0, 10.0]},
    {"Q": [15.0, 15.0, 8.0], "R": [1.0, 1.0]},
    {"Q": [2.0, 3.0, 1.0], "R": [0.1, 0.1]}
]

# Folder Setup
log_folder = "/home/gagan/Desktop/Adv Controll Engineering /rcognita-edu-main/simdata/lqr/Init_angle_1.57_seed_1_Nactor_10"
os.makedirs(log_folder, exist_ok=True)

# Run Simulation 
for i, cost in enumerate(cost_sets):
    print(f"\n Running LQR Simulation {i+1} with Q={cost['Q']} and R={cost['R']}")

    os.environ["Q_VALS"] = " ".join(str(x) for x in cost["Q"])
    os.environ["R_VALS"] = " ".join(str(x) for x in cost["R"])
    print("Environment variables set:", os.environ["Q_VALS"], os.environ["R_VALS"])

    subprocess.run([
        "python3", "PRESET_3wrobot_NI.py",
        "--ctrl_mode", "lqr",
        "--Nruns", "1",
        "--t1", "20",
        "--is_visualization", "0",
        "--is_log_data", "1",
        "--Q", *map(str, cost["Q"]),
        "--R", *map(str, cost["R"]),
        "--v_max", "1.0",
        "--omega_max", "1.0"
    ])

def find_latest_lqr_csvs(folder, prefix="3wrobotNI_lqr_", run_suffix="__run01.csv", count=3):
    pattern = os.path.join(folder, f"{prefix}*{run_suffix}")
    all_files = glob.glob(pattern)
    all_files.sort(key=os.path.getmtime, reverse=True)
    return all_files[:count]

print("\n Plotting Results")

def smart_read_csv(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    header_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith("t"): 
            header_index = i
            break
    if header_index is None:
        raise ValueError(f"Header row not found in {file_path}")
    return pd.read_csv(file_path, skiprows=header_index)

csvs = find_latest_lqr_csvs(log_folder)
if not csvs:
    print("No CSV files found for plotting.")
    exit()

dfs = []
for f in csvs:
    df = smart_read_csv(f)
    df.columns = [col.strip() for col in df.columns]  
    dfs.append(df)

print(f"Found {len(dfs)} CSV files for plotting.")

# Define colors
colors = ['black', 'Pink', 'green']

# PLOT 1: x vs y
plt.figure(figsize=(10, 10))
for i, df in enumerate(dfs):
    plt.plot(df['x [m]'], df['y [m]'], label=f"Run {i+1} - Q={cost_sets[i]['Q']}, R={cost_sets[i]['R']}", color=colors[i])
plt.title("LQR: Trajectory (x vs y)")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(log_folder, "Trajectory_Plot.png"))
plt.close()

# PLOT 2: Tracking error VS Time
plt.figure(figsize=(10, 10))
for i, df in enumerate(dfs):
    error = np.sqrt(df['x [m]']**2 + df['y [m]']**2)
    plt.plot(df['t [s]'], error, label=f"Run {i+1}", color=colors[i])

    if error.iloc[-1] > 0.5:
        print(f" Run {i+1} may not converge properly: final error = {error.iloc[-1]:.2f} m")

plt.title("LQR: Tracking Error vs Time")
plt.xlabel("Time [s]")
plt.ylabel("Position Error [m]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(log_folder, "Tracking_Error_Plot.png"))
plt.close()

# PLOT 3: v and omega vs time
plt.figure(figsize=(10, 10))
for i, df in enumerate(dfs):
    plt.plot(df['t [s]'], df['v [m/s]'], label=f"v - Run {i+1}", color=colors[i])
    plt.plot(df['t [s]'], df['omega [rad/s]'], '--', label=f"ω - Run {i+1}", color=colors[i])
plt.title("LQR: Control Inputs Over Time")
plt.xlabel("Time [s]")
plt.ylabel("Input Values")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(log_folder, "Control_Inputs_Plot.png"))
plt.close()

print(" Plots Saved:")

