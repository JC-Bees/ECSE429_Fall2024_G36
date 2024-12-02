import numpy as np
import matplotlib.pyplot as plt

# Load time data
delete_times = np.loadtxt("DeleteTimes_Categories.csv", delimiter = ",")
post_times = np.loadtxt("PostTimes_Categories.csv", delimiter = ",")
put_times = np.loadtxt("PutTimes_Categories.csv", delimiter = ",")

num_objects = range(1, len(delete_times) + 1)

# Load perfmon data
cpu_mem_data = np.genfromtxt("CPU_Memory_Categories.csv", delimiter=",", skip_header=1, dtype=None, encoding=None)
time = cpu_mem_data[:, 0]
memory = cpu_mem_data[:, 1]
memory = np.array([float(m.strip('"')) for m in memory]) # convert from string to float
cpu = (cpu_mem_data[:, 4])[1:len(cpu_mem_data)]
cpu = np.array([float(c.strip('"')) for c in cpu]) # convert from string to float

# Plot the delete data
plt.figure(figsize=(10, 6))
plt.scatter(num_objects, delete_times, label="Delete Times")

plt.title("Delete Time per Object", fontsize=16)
plt.xlabel("Number of Objects", fontsize=12)
plt.ylabel("Time Taken (seconds)", fontsize=12)

plt.grid(True, linestyle='--', alpha=0.7)
#plt.legend(fontsize=12)

plt.show()

# Plot the post data
plt.figure(figsize=(10, 6))
plt.scatter(num_objects, post_times, label="Post Times")

plt.title("Post Time per Object", fontsize=16)
plt.xlabel("Number of Objects", fontsize=12)
plt.ylabel("Time Taken (seconds)", fontsize=12)

plt.grid(True, linestyle='--', alpha=0.7)

plt.show()

# Plot the put data
plt.figure(figsize=(10, 6))
plt.scatter(num_objects, put_times, label="Put Times")

plt.title("Put Time per Object", fontsize=16)
plt.xlabel("Number of Objects", fontsize=12)
plt.ylabel("Time Taken (seconds)", fontsize=12)

plt.grid(True, linestyle='--', alpha=0.7)

plt.show()

# Plot the CPU data
plt.figure(figsize=(10, 6))
plt.plot(time[1:len(cpu_mem_data)], cpu, label="CPU Usage")
plt.xticks(rotation=90)

plt.ylabel("CPU Usage", fontsize=12)
plt.xlabel("Time ", fontsize=12)

plt.grid(True, linestyle='--', alpha=0.7)

plt.show()

# Plot the Memory data
plt.figure(figsize=(10, 6))
plt.plot(time, memory, label="Available Memory")

plt.ylabel("Available Memory", fontsize=12)
plt.xlabel("Time ", fontsize=12)
plt.xticks(rotation=90)

plt.grid(True, linestyle='--', alpha=0.7)

plt.show()