import os
import csv
from library.generator import Generator

# Template for the generated C-Code
code_template = """
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>

void write_to_csv(const char* instruction, double cycles_per_instruction) {{
    FILE* file = fopen("LatencyResults.csv", "a");
    fprintf(file, "%s, %f\\n", instruction, cycles_per_instruction);
    fclose(file);
}}

int main() {{

    // Loop for warmup runs
    for (int i = 0; i < 2; i++) {{
        // Clear the registers and write the pmu counter in x20
        __asm__ __volatile__("mov x19, 1");
        __asm__ __volatile__("mov x20, 0");
        __asm__ __volatile__("mov x21, 0");
        __asm__ volatile("isb");
        __asm__ __volatile__(" mrs x20, pmccntr_el0");

        // Add the instructions to be tested in the loop
        {instruction_block}
    }}

    // Get the final value of the pmu counter and write it in x21
    __asm__ __volatile__("mrs x21, pmccntr_el0");
    __asm__ volatile("isb");

    // Calculate the resulting number of cycles and write it to the CSV file
    uint64_t start_cycles = 0;
    __asm__ __volatile__("mov %0, x20" : "=r" (start_cycles));
    uint64_t end_cycles = 0;
    __asm__ __volatile__("mov %0, x21" : "=r" (end_cycles));
    uint64_t cycles_over_all = end_cycles - start_cycles;
    double cycles_per_instruction = (double)(cycles_over_all / {iterations});

    write_to_csv("{instruction}", cycles_per_instruction);

    return 0;
}}
"""

# Number of Iteration for the following instruction block
num_iterations = 9800

# Generate a list with all instructions to be benchmarked and then split it up in their names and the actual assembler instruction
blocks = []
blocks.extend(Generator.generate())
name = [tup[0] for tup in blocks]
string = [tup[1] for tup in blocks]

counter = 0

# Loop over the instructions and create the C-Files
for instruction in string:
    mode = ""
    instruction_block = ""
    for i in range(num_iterations):
        if (i + 1) % 2 == 0:
            modified_instruction = instruction.replace("9", "11").replace("10", "9").replace("11", "10")
            instruction_block += ''.join(modified_instruction)
        else:
            instruction_block += ''.join(instruction)

    c_code = code_template.format(instruction=name[counter], instruction_block=instruction_block, iterations=num_iterations * 1.0, mode=mode)
    c_file_name = name[counter] + "_latency.c"
    with open(c_file_name, "w") as f:
        f.write(c_code)
    os.system("gcc -O0 -o {0} {1}".format(name[counter] + "_latency", c_file_name))
    counter += 1
    print(str(counter) + " out of " + str(len(string)) + " benchmarks created!")

print("Benchmarks were created successfully!")