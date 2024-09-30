#!/bin/zsh

# Bash script to run Python command with arguments from 1 to 50
# use this script to change the format of ground truth json to standardized format

for i in {1..50}
do
  # Replace `your_python_script.py` with your actual Python script or command
  python to_std_format2.py "$i"
done
