# Script to execute all throughput benchmarks

import os
from library.generator import Generator

# Reset CSV File
file = 'ThroughputResults.csv'
if(os.path.exists(file) and os.path.isfile(file)):
  os.remove(file)

# Create the list of all instructions to be tested and get their names
blocks = []
blocks.extend(Generator.generate())
name = [tup[0] for tup in blocks]

# Loop over the instructions to run the C-Files
for instruction in name:
    os.system("taskset 8  ./{0}_throughput_1".format(instruction))
    os.system("taskset 8  ./{0}_throughput_2".format(instruction))
    os.system("taskset 8  ./{0}_throughput_4".format(instruction))
    os.system("taskset 8  ./{0}_throughput_6".format(instruction))
    os.system("taskset 8  ./{0}_throughput_8".format(instruction))

print("Success. Data written to ThroughputResults.csv!")