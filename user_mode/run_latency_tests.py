# Script to execute all latency benchmarks

import os
from library.generator import Generator

# Reset CSV File
file = 'LatencyResults.csv'
if(os.path.exists(file) and os.path.isfile(file)):
  os.remove(file)

# Create the list of all instructions to be tested and get their names
blocks = []
blocks.extend(Generator.generate())
name = [tup[0] for tup in blocks]

# Loop over the instructions to run the C-Files
for instruction in name:
    os.system("taskset 8  ./{0}_latency".format(instruction))

print("Success. Data written to LatencyResults.csv!")