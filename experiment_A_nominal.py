# IMPORT REQUIRED LIBRARIES
import pandas as pd                 # For reading and handling CSV files
import matplotlib.pyplot as plt     # For plotting data
import numpy as np                  # For numerical operations

# DEFINE GAIN SETS
gain_sets = [
    {"k_rho": 2.5, "k_alpha": 4.5, "k_beta": -1.5}, # (Controller Law for Control Design)
    {"k_rho": 1.0, "k_alpha": 3.0, "k_beta": -1.0}, # (Controller Law for Control Design)
    {"k_rho": 0.5, "k_alpha": 6.0, "k_beta": -0.5}, # (Controller Law for Control Design)
    ]

# DEFINE FILE PATHS FOR CSV FILES GENERATED FROM SIMULATION
csv_files = [
    '/home/gagan/Desktop/Adv Controll Engineering /rcognita-edu-main/simdata/Nominal/Init_angle_1.57_seed_1_Nactor_10/3wrobotNI_Nominal_2025-06-22_17h17m02s__run02.csv',
    '/home/gagan/Desktop/Adv Controll Engineering /rcognita-edu-main/simdata/Nominal/Init_angle_1.57_seed_1_Nactor_10/3wrobotNI_Nominal_2025-06-22_17h17m02s__run01.csv',
    '/home/gagan/Desktop/Adv Controll Engineering /rcognita-edu-main/simdata/Nominal/Init_angle_1.57_seed_1_Nactor_10/3wrobotNI_Nominal_2025-06-22_17h17m02s__run01.csv'
]


# DEFINE COLORS FOR EACH RUN
colors = ['black', 'purple', 'pink']

# FUNCTION TO READ CSV WHILE SKIPPING METADATA COMMENTS
def smart_read_csv(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # Identify the header line (starts with "t [s],")
    for i, line in enumerate(lines):
        if line.startswith("t [s],"):
            header_index = i
            break
    return pd.read_csv(file_path, skiprows=header_index)

# PLOT 1: ROBOT TRAJECTORY VS REFERENCE (x vs y)
plt.figure(figsize=(10, 10))
for i, (file, color) in enumerate(zip(csv_files, colors), start=1):
    data = smart_read_csv(file)
    data.columns = [col.strip() for col in data.columns]

    # Plot the actual robot trajectory
    plt.plot(data['x [m]'], data['y [m]'], label=f'Run {i}', color=color)

plt.xlabel('x [m]')
plt.ylabel('y [m]')
plt.title('Robot Trajectories (N_controller)')
plt.legend()
plt.grid(True)
plt.axis('equal')  # x-y plot, so equal scaling makes sense
plt.savefig('simdata/Robot_Trajectories_Kinematics.png')
plt.close()

# PLOT 2: LINEAR VELOCITY v(t)
plt.figure(figsize=(10, 10))
for i, (file, color) in enumerate(zip(csv_files, colors), start=1):
    data = smart_read_csv(file)
    data.columns = [col.strip() for col in data.columns]

    # Plot v [m/s] over time
    plt.plot(data['t [s]'], data['v [m/s]'], label=f'Run {i}', color=color)

plt.xlabel('t [s]')
plt.ylabel('v [m/s]')
plt.title('Linear velocity over time')
plt.legend()
plt.grid(True)
plt.savefig('simdata/Linear_Velocity_Kinematics.png')
plt.close()

# PLOT 3: ANGULAR VELOCITY omega(t)
plt.figure(figsize=(10, 10))
for i, (file, color) in enumerate(zip(csv_files, colors), start=1):
    data = smart_read_csv(file)
    data.columns = [col.strip() for col in data.columns]

    # Plot omega [rad/s] over time
    plt.plot(data['t [s]'], data['omega [rad/s]'], label=f'Run {i}', color=color)

plt.xlabel('t [s]')
plt.ylabel('omega [rad/s]')
plt.title('Angular Velocity Over Time')
plt.legend()
plt.grid(True)
plt.savefig('simdata/Angular_Velocity_Kinematics.png')
plt.close()

# PLOT 4: TRACKING ERROR VS TIME (Using fixed goal)
plt.figure(figsize=(10, 10))

# Define your fixed goal location (set your actual goal here)
x_goal, y_goal = 0.0, 0.0

for i, (file, color) in enumerate(zip(csv_files, colors), start=1):
    data = smart_read_csv(file)
    data.columns = [col.strip() for col in data.columns]

    # Compute distance to fixed goal at every time step
    error = np.sqrt((data['x [m]'] - x_goal)**2 + (data['y [m]'] - y_goal)**2)

    # Plot tracking error over time
    plt.plot(data['t [s]'], error, label=f'Run {i}', color=color)

plt.xlabel('t [s]')
plt.ylabel('Tracking Error [m]')
plt.title('Tracking Error Over Time')
plt.legend()
plt.grid(True)
plt.savefig('simdata/Tracking_Error_Over_Time.png')
plt.close()
# PRINT SUCCESS MESSAGE
print("Plot Saved :)")