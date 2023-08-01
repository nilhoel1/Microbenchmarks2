# Script to execute all latency benchmarks

import os
import csv
from library.generator import Generator

# Reset CSV Files
file = 'PortUsageResults.csv'
if(os.path.exists(file) and os.path.isfile(file)):
  os.remove(file)
file = 'LatencyResults.csv'
if(os.path.exists(file) and os.path.isfile(file)):
  os.remove(file)
file = 'ThroughputResults.csv'
if(os.path.exists(file) and os.path.isfile(file)):
  os.remove(file)

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

subblocks = [tup for tup in blocks if 'x' in tup[0] or 'nop' in tup[0] or 'adr' in tup[0]]
subnames = [tup[0] for tup in subblocks]

# Loop over the instructions to run the C-Files
for instruction in subnames:
    for instruction2 in subnames:
        if(os.path.exists("./{0}_with_{1}_port_usage".format(instruction, instruction2))):
            os.system("taskset 8  ./{0}_with_{1}_port_usage".format(instruction, instruction2))

# Dictionary, to save the data
matrix_data = {}

# Open CSV and read its data
with open('PortUsageResults.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Save Data in the dictionary
    for row in csvreader:
        first_name = row[0].strip()
        second_name = row[1].strip()
        value = float(row[2])
        
        if first_name not in matrix_data:
            matrix_data[first_name] = {}
        
        matrix_data[first_name][second_name] = int(value)

# Create list of all first names for showing of the names in the end results
name_list = list(matrix_data.keys())

print(str(len(name_list)) + " should be 69!")

# Create matrix and make comparisions
matrix = []
first_names = list(matrix_data.keys())
for i, first_name in enumerate(first_names):
    row_values = []
    compare = matrix_data[first_name][first_name]
    for j, second_name in enumerate(first_names):
        if i == j:
            # Main diagonal
            row_values.append(1)
        elif matrix_data[first_name][second_name] > compare:
            row_values.append(0)
        else:
            row_values.append(1)
    matrix.append(row_values)

# Loop over the matrix and delete duplicate rows and columns
finished = False
while finished == False:

    # Remove duplicate rows while keeping one instance of each
    filtered_matrix = []
    seen_rows = set()
    deleted_index = []
    counter = 0
    similar = []

    for row in matrix:
        row_tuple = tuple(row)  # Convert the row to a tuple for hashing
        
        # Only keep duplicated rows once
        if row_tuple not in seen_rows:
            filtered_matrix.append(row)
            seen_rows.add(row_tuple)
        else:
            similar.append(filtered_matrix.index(row))
            deleted_index.append(counter)
        counter += 1

    # Delete corresponding columns to deleted rows
    for row in filtered_matrix:
        for index in reversed(deleted_index):
            row.pop(index)

    # Delete corresponding names to deleted rows/columns
    for index in reversed(deleted_index):
        name_list[similar[-1]] += (", " + first_names[index])
        similar.pop
        name_list.pop(index)

    if len(deleted_index) == 0:
        finished = True
        break
    else:
        matrix = filtered_matrix

newFile = 'InterferenceMatrix.csv'

if(os.path.exists(newFile) and os.path.isfile(newFile)):
  os.remove(newFile)

# Write results to csv
with open(newFile, mode='w', newline='') as newFile:
    writer = csv.writer(newFile)

    # Write Matrix to csv
    for row in filtered_matrix:
        writer.writerow(row)

    # Write names to csv
    i = 1
    for name in name_list:
        writer.writerow([str(i), name])
        i += 1

print("Results for Throughput (Port Usage) were saved in PortUsageResults.csv.")
print("Results for Interference were saved in InterferenceMatrix.csv.")
print("Success. Data written to LatencyResults.csv and ThroughputResults.csv!")