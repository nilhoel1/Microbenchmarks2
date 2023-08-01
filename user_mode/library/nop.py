from library.instruction import Instruction


class Nop(Instruction):
    def __init__(self):
        opcode = "nop"
        suffixes = [""]
        registerPrefixes = [""]
        numberOfOperators = 0
        shift = [""]
        immediates = [""]
        bothAllowed = False
        super().__init__(opcode, suffixes, registerPrefixes, numberOfOperators, shift, immediates, bothAllowed)



    def generate_instruction_block(self):
        blocks = []
        
        instruction_block = f"__asm__ __volatile__(\"{self.opcode}\");\n"
        blocks.append(["nop_basic", instruction_block])

        return blocks