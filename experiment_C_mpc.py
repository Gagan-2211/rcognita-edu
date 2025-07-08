import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob

# Define MPC Configuration
mpc_configs = [
    {"Nactor": 5, "R1_diag": [200, 200, 15, 15, 10], "Qf": [100, 100, 10]},
    {"Nactor": 20, "R1_diag": [10, 10, 1, 1, 0.5], "Qf": [10, 10, 1]},
    {"Nactor": 10, "R1_diag": [400, 400, 40, 50, 10], "Qf": [150, 150, 15]},
]

# Base Path
log_folder = "/home/gagan/Desktop/Adv Controll Engineering /rcognita-edu-main/simdata/MPC"
os.makedirs(log_folder, exist_ok=True)

# RUN SIMULATIONS 
for i, config in enumerate(mpc_configs):
    print(f"\n Running MPC Simulation {i+1} with Nactor={config['Nactor']}, Qf={config['Qf']}")

    os.environ["NACTOR"] = str(config["Nactor"])
    os.environ["R1_DIAG"] = " ".join(str(x) for x in config["R1_diag"])
    os.environ["QF"] = " ".join(str(x) for x in config["Qf"])

    subprocess.run([
        "python3", "PRESET_3wrobot_NI.py",
        "--ctrl_mode", "MPC",
        "--Nruns", "1",
        "--t1", "20",
        "--is_visualization", "0",
        "--is_log_data", "1",
        "--Nactor", str(config["Nactor"]),
        "--R1_diag", *map(str, config["R1_diag"]),
        "--Qf", *map(str, config["Qf"]),
    ])

def get_latest_csv_from_each_subfolder(main_folder, pattern="3wrobotNI_MPC_*__run01.csv"):
    csv_paths = []
    subfolders = [os.path.join(main_folder, d) for d in os.listdir(main_folder)
                  if os.path.isdir(os.path.join(main_folder, d))]
    subfolders.sort()
    subfolders = subfolders[:3]

    for folder in subfolders:
        match = glob.glob(os.path.join(folder, pattern))
        if match:
            match.sort(key=os.path.getmtime, reverse=True)
            csv_paths.append(match[0])
        else:
            print(f"No matching CSV in: {folder}")
    return csv_paths

csvs = get_latest_csv_from_each_subfolder(log_folder)

if not csvs:
    print("No CSV files found for plotting.")
    exit()

def smart_read_csv(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    header_index = None
    for i, line in enumerate(lines):
        if line.strip().startswith("t"):
            header_index = i
            break
    if header_index is None:
        raise ValueError(f"Header not found in {file_path}")
    return pd.read_csv(file_path, skiprows=header_index)

dfs = []
for f in csvs:
    df = smart_read_csv(f)
    df.columns = [col.strip() for col in df.columns]  
    dfs.append(df)

# Define colors
colors = ['black', 'pink', 'green'] 

# PLOT 1: Trajectory (x vs y)
plt.figure(figsize=(8, 6))
for i, df in enumerate(dfs):
    plt.plot(df['x [m]'], df['y [m]'], label=f"Run {i+1} - N={mpc_configs[i]['Nactor']}", color=colors[i])
plt.title("MPC Trajectory (x vs y)")
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(log_folder, "MPC_Trajectory.png"))
plt.close()

# PLOT 2: Tracking Error vs Time 
plt.figure(figsize=(8, 6))
for i, df in enumerate(dfs):
    error = np.sqrt(df['x [m]']**2 + df['y [m]']**2)
    plt.plot(df['t [s]'], error, label=f"Run {i+1}", color=colors[i])
plt.title("MPC Tracking Error vs Time")
plt.xlabel("Time [s]")
plt.ylabel("Position Error [m]")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(log_folder, "MPC_Tracking_Error.png"))
plt.close()

# PLOT 3: Control Inputs vs Time
plt.figure(figsize=(10, 6))
for i, df in enumerate(dfs):
    plt.plot(df['t [s]'], df['v [m/s]'], label=f"v - Run {i+1}", color=colors[i])
    plt.plot(df['t [s]'], df['omega [rad/s]'], '--', label=f"ω - Run {i+1}", color=colors[i])
plt.title("MPC Control Inputs (v and ω) vs Time")
plt.xlabel("Time [s]")
plt.ylabel("Control Inputs")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(log_folder, "MPC_Control_Inputs.png"))
plt.close()

# PLOT 4: Accumulated Cost vs Time
plt.figure(figsize=(8, 6))
for i, df in enumerate(dfs):
    if 'accum_obj' in df.columns:
        plt.plot(df['t [s]'], df['accum_obj'], label=f"Run {i+1}", color=colors[i])
plt.title("MPC Accumulated Cost vs Time")
plt.xlabel("Time [s]")
plt.ylabel("Accumulated Cost")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(log_folder, "MPC_Accumulated_Cost.png"))
plt.close()

# Success Message
print("Plots saved:")

