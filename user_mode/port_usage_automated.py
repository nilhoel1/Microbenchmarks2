import os
from library.generator import Generator

# Template for the generated C-Code
code_template = """
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>

void write_to_csv(const char* instruction, const char* instruction2, double throughput) {{
    FILE* file = fopen("PortUsageResults.csv", "a");
    fprintf(file, "%s, %s, %f\\n", instruction, instruction2, throughput);
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
    write_to_csv("{instruction}", "{instruction2}", throughput);

    return 0;
}}
"""

# Number of Iterations for the following instruction block
num_iterations = 6000

# Generate a list with all instructions to be benchmarked and then split it up into their names and the actual assembler instruction
blocks = []
blocks.extend(Generator.generate())
name = [tup[0] for tup in blocks]
string = [tup[1] for tup in blocks]

subblocks = [tup for tup in blocks if 'x' in tup[0] or 'nop' in tup[0] or 'adr' in tup[0]]
subnames = [tup[0] for tup in subblocks]
substring = [tup[1] for tup in subblocks]


counter = 0
progress = 1
# Loop over the instructions and create the C-Files
for instruction in substring:
    mode = ""
    counter2 = 0
    for instruction2 in substring:
    # Generate registers and memory locations for each instance to avoid read-after-write dependencies
        instruction_block = ""
        instruction = instruction.replace("9", "10").replace("10", "9", 1)
        instruction2 = instruction2.replace("9", "10").replace("10", "9", 1)
        for i in range(int(num_iterations/3)):
            for j in range(2):
                next_register = j + 10
                modified_instruction = instruction.replace("10", str(next_register))
                instruction_block += modified_instruction
            modified_instruction = instruction2.replace("10", "12")
            instruction_block += modified_instruction

        c_code = code_template.format(
            instruction=subnames[counter],
            instruction2=subnames[counter2],
            instruction_block=instruction_block,
            iterations=num_iterations * 1.0,
            mode=mode
        )

        c_file_name = subnames[counter] + f"_with_" + subnames[counter2] + f"_port_usage.c"
        with open(c_file_name, "w") as f:
            f.write(c_code)
        os.system(f"gcc -O0 -o {subnames[counter]}_with_{subnames[counter2]}_port_usage {c_file_name}")
        print(str(progress) + " out of " + str(len(substring) * len(substring)) + " benchmarks created!")
        progress += 1
        counter2 += 1

    counter += 1

print("Benchmarks were created successfully!")