import os
import csv
from library.generator import Generator

# Template for the generated C-Code
code_template = """
#include <math.h>
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>

void write_to_csv(const char* instruction, const char* sequence_length, int roundedThroughput) {{
    FILE* file = fopen("ThroughputResults.csv", "a");
    fprintf(file, "%s, %s, %d\\n", instruction,  sequence_length, roundedThroughput);
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
    __asm__ __volatile__("mrs x20, pmccntr_el0");

    // Add the instructions to be tested in the loop
    {instruction_block}
}}

    // Get the final value of the pmu counter and write it in x21
    __asm__ __volatile__("mrs x21, pmccntr_el0");
    __asm__ volatile("isb");

    // Calculate the resulting number of cycles and print it out
    uint64_t start_cycles = 0;
    __asm__ __volatile__("mov %0, x20" : "=r" (start_cycles));
    uint64_t end_cycles = 0;
    __asm__ __volatile__("mov %0, x21" : "=r" (end_cycles));
    uint64_t cycles_over_all = end_cycles - start_cycles;
    double cycles_per_instruction = (double)(cycles_over_all / {iterations});
    double throughput = 1.0 / cycles_per_instruction;
    int roundedThroughput = round(throughput);
    write_to_csv("{instruction}", "{sequence_length}", roundedThroughput);

    return 0;
}}
"""

# Number of Iterations for the following instruction block
num_iterations = 9800

# Generate a list with all instructions to be benchmarked and then split it up into their names and the actual assembler instruction
blocks = []
blocks.extend(Generator.generate())
name = [tup[0] for tup in blocks]
string = [tup[1] for tup in blocks]

counter = 0
counter2 = 1
# Loop over the instructions and create the C-Files
for instruction in string:
    mode = ""
    for sequence_length in [1, 2, 4, 6, 8]:
        instruction_block = ""
        if sequence_length > 1:
            instruction = instruction.replace("9", "10").replace("10", "9", 1) 
        # Generate registers and memory locations for each instance to avoid read-after-write dependencies
        for i in range(int(num_iterations / sequence_length)):
            for j in range(sequence_length):
                if sequence_length > 1:
                    # Calculate the current register values based on the sequence length

                    next_register = j + 10

                    # Replace the register values in the instruction
                    modified_instruction = instruction.replace("10", str(next_register))

                    instruction_block += modified_instruction
                else:
                    if (i + 1) % 2 == 0:
                        modified_instruction = instruction.replace("9", "11").replace("10", "9").replace("11", "10")
                        instruction_block += ''.join(modified_instruction)
                    else:
                        instruction_block += ''.join(instruction)

        c_code = code_template.format(
            instruction=name[counter],
            instruction_block=instruction_block,
            iterations=num_iterations * 1.0,
            sequence_length=sequence_length,
            mode=mode
        )

        c_file_name = name[counter] + f"_throughput_{sequence_length}.c"
        with open(c_file_name, "w") as f:
            f.write(c_code)
        os.system(f"gcc -O0 -o {name[counter]}_throughput_{sequence_length} {c_file_name} -lm")
        print(str(counter2) + " out of " + str(len(string) * 5) + " benchmarks created!")
        counter2 += 1

    counter += 1

print("Benchmarks were created successfully!")