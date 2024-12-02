#!/bin/bash

# Output file for logging
OUTPUT_FILE="CreatingProjectsData.txt"

# Interval between samples (in seconds)
INTERVAL=1

# Python script to run
PYTHON_SCRIPT="CPU_Memory_Usage_Creating_Projects.py"

# Print headers to log file
echo "Timestamp, CPU(%), Memory(GB)" > $OUTPUT_FILE

# Start the Python script and capture its PID
python3 $PYTHON_SCRIPT &
PID2=$!
#process Id of the thingifier app (java code)
PID=84321

echo "Monitoring PID $PID for script $PYTHON_SCRIPT"

# Monitor the app in a loop until it exits
while kill -0 $PID2 2>/dev/null; do
  # Check CPU and memory usage
  CPU=$(ps -p $PID -o %cpu | tail -n 1 | tr -d " ")
  MEM=$(ps -p $PID -o rss | tail -n 1 | awk '{print $1/1024/1024}')
  
  # Log the data
  echo "$(date '+%Y-%m-%d %H:%M:%S'), $CPU, $MEM" >> $OUTPUT_FILE
  
  # Wait for the interval before the next sample
  sleep $INTERVAL
done

echo "Python script $PYTHON_SCRIPT has completed. Logging ended."

# Output file for logging
OUTPUT_FILE="DeletingProjectsData.txt"

# Interval between samples (in seconds)
INTERVAL=1

# Python script to run
PYTHON_SCRIPT="CPU_Memory_Usage_Deleting_Projects.py"

# Print headers to log file
echo "Timestamp, CPU(%), Memory(GB)" > $OUTPUT_FILE

# Start the Python script and capture its PID
python3 $PYTHON_SCRIPT &
PID2=$!
#process Id of the thingifier app (java code)
PID=84321

echo "Monitoring PID $PID for script $PYTHON_SCRIPT"

# Monitor the app in a loop until it exits
while kill -0 $PID2 2>/dev/null; do
  # Check CPU and memory usage
  CPU=$(ps -p $PID -o %cpu | tail -n 1 | tr -d " ")
  MEM=$(ps -p $PID -o rss | tail -n 1 | awk '{print $1/1024/1024}')
  
  # Log the data
  echo "$(date '+%Y-%m-%d %H:%M:%S'), $CPU, $MEM" >> $OUTPUT_FILE
  
  # Wait for the interval before the next sample
  sleep $INTERVAL
done

echo "Python script $PYTHON_SCRIPT has completed. Logging ended."

# Output file for logging
OUTPUT_FILE="ChangingProjectsData.txt"

# Interval between samples (in seconds)
INTERVAL=1

# Python script to run
PYTHON_SCRIPT="CPU_Memory_Usage_Changing_Projects.py"

# Print headers to log file
echo "Timestamp, CPU(%), Memory(GB)" > $OUTPUT_FILE

# Start the Python script and capture its PID
python3 $PYTHON_SCRIPT &
PID2=$!
#process Id of the thingifier app (java code)
PID=84321

echo "Monitoring PID $PID for script $PYTHON_SCRIPT"

# Monitor the app in a loop until it exits
while kill -0 $PID2 2>/dev/null; do
  # Check CPU and memory usage
  CPU=$(ps -p $PID -o %cpu | tail -n 1 | tr -d " ")
  MEM=$(ps -p $PID -o rss | tail -n 1 | awk '{print $1/1024/1024}')
  
  # Log the data
  echo "$(date '+%Y-%m-%d %H:%M:%S'), $CPU, $MEM" >> $OUTPUT_FILE
  
  # Wait for the interval before the next sample
  sleep $INTERVAL
done

echo "Python script $PYTHON_SCRIPT has completed. Logging ended."
