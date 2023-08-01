# Parent class for all instructions

import random


class Instruction():

    def __init__(self, opcode, suffixes, registerPrefixes, numberOfOperators, shift, immediates, bothAllowed):
        self.opcode = opcode                                # String: Name of the Assembler-Instruction
        self.suffixes = suffixes                            # List of Chars: All possible suffixes for the specific Instruction
        self.registerPrefixes = registerPrefixes            # List of Chars: All possible register prefixes (x, w, ...) for the specific Instruction
        self.numberOfOperators = numberOfOperators          # List of Ints: Number of registers needed for the Instruction
        self.shift = shift                                  # List of Strings: Add specific shifts to the instruction
        self.immediates = immediates                        # List of Strings: Add specific immediates to the instruction (One register will automatically be removed)
        self.bothAllowed = bothAllowed                      # Boolean: Specify if the instruction can use shift and an immediate at the same time
    
    # Generate the instruction blocks, with the corresponding name
    def generate_instruction_block(self):
        blocks = []
        
        # Loop for all parameter
        for suffix in self.suffixes:
            for prefix in self.registerPrefixes:
                for shift in self.shift:
                    for immediate in self.immediates:

                        # Filter if the instruction can use shift and an immediate at the same time
                        if self.bothAllowed == True:
                            instruction_block = f"__asm__ __volatile__(\"{self.opcode}{suffix} {prefix}9"
                            if self.numberOfOperators == 1:
                                if immediate == "":
                                    instruction_block += f", {random.randint(1, 20)}"
                                else:
                                    instruction_block += f", {immediate}"
                            elif self.numberOfOperators == 2:
                                if immediate == "":
                                    instruction_block += f", {prefix}10"
                                else:
                                    instruction_block += f", {immediate}"
                            else:
                                if immediate == "":
                                    instruction_block += f", {prefix}10, {prefix}9"
                                else:
                                    instruction_block += f", {prefix}10, {immediate}"
                            
                            if shift == "":
                                instruction_block += f"\");\n"
                                if immediate == "":
                                    blocks.append([self.opcode + suffix + "_" + prefix, instruction_block])
                                else:
                                    blocks.append([self.opcode + suffix + "_" + prefix + "_with_immediate", instruction_block])
                            else:
                                instruction_block += f", {shift} \");\n"
                                if immediate == "":
                                    blocks.append([self.opcode + suffix + "_" + prefix  + "_with_shift", instruction_block])
                                else:
                                    blocks.append([self.opcode + suffix + "_" + prefix + "_with_immediate" + "_with_shift", instruction_block])
                                    
                        # Filter if the instruction can't use shift and an immediate at the same time    
                        else:
                            i = 0
                            while i < 2:
                                if i == 0:
                                    instruction_block = f"__asm__ __volatile__(\"{self.opcode}{suffix} {prefix}9"
                                    if self.numberOfOperators == 1:
                                        if immediate == "":
                                            instruction_block += f", {random.randint(1, 20)}"
                                        else:
                                            instruction_block += f", {immediate}"
                                    elif self.numberOfOperators == 2:
                                        if immediate == "":
                                            instruction_block += f", {prefix}10"
                                        else:
                                            instruction_block += f", {immediate}"
                                    else:
                                        if immediate == "":
                                            instruction_block += f", {prefix}10, {prefix}9"
                                        else:
                                            instruction_block += f", {prefix}10, {immediate}"
                                    
                                    instruction_block += f"\");\n"
                                    if immediate == "" and shift == "":
                                        blocks.append([self.opcode + suffix + "_" + prefix, instruction_block])
                                    elif immediate != "":
                                        blocks.append([self.opcode + suffix + "_" + prefix + "_with_immediate", instruction_block])

                                else:
                                    instruction_block = f"__asm__ __volatile__(\"{self.opcode}{suffix} {prefix}9"
                                    if self.numberOfOperators == 1:
                                        instruction_block += f", {random.randint(1, 20)}"
                                    elif self.numberOfOperators == 2:
                                        instruction_block += f", {prefix}10"
                                    else:
                                        instruction_block += f", {prefix}10, {prefix}9"

                                    if shift != "":
                                        instruction_block += f", {shift} \");\n"
                                        blocks.append([self.opcode + suffix + "_" + prefix  + "_with_shift", instruction_block])

                                i += 1
                        
        return blocks