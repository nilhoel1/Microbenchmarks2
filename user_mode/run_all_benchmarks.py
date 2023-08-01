# Script to execute all latency benchmarks

import os
from library.generator import Generator

# Create the list of all instructions to be tested and get their names
blocks = []
blocks.extend(Generator.generate())
name = [tup[0] for tup in blocks]

# Loop over the instructions to run the C-Files
for instruction in name:
    os.system("taskset 8  ./{0}_latency".format(instruction))
    os.system("taskset 8  ./{0}_throughput_1".format(instruction))
    os.system("taskset 8  ./{0}_throughput_2".format(instruction))
    os.system("taskset 8  ./{0}_throughput_4".format(instruction))
    os.system("taskset 8  ./{0}_throughput_6".format(instruction))
    os.system("taskset 8  ./{0}_throughput_8".format(instruction))

print("Success. Data written to LatencyResults.csv and ThroughputResults.csv!")