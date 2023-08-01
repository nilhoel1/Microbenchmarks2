from library.instruction import Instruction


class Adr(Instruction):
    def __init__(self):
        opcode = "adr"
        suffixes = [""]
        registerPrefixes = ["x"]
        numberOfOperators = 2
        shift = [""]
        self.op1 = "x9"
        self.op2 = "x10"
        self.op3 = ".+0"
        immediates = [""]
        bothAllowed = False
        super().__init__(opcode, suffixes, registerPrefixes, numberOfOperators, shift, immediates, bothAllowed)



    def generate_instruction_block(self):
        blocks = []
        
        instruction_block = f"__asm__ __volatile__(\"{self.opcode} {self.op1}, {self.op3}\");\n"
        blocks.append(["adr_basic", instruction_block])

        return blocks