from library.instruction import Instruction


class Bic(Instruction):
    def __init__(self):
        opcode = "bic"
        suffixes = ["", "s"]
        registerPrefixes = ["x", "w"]
        numberOfOperators = 3
        shift = ["", "lsl #1"]
        immediates = [""]
        bothAllowed = False
        super().__init__(opcode, suffixes, registerPrefixes, numberOfOperators, shift, immediates, bothAllowed)