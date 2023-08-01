from library.instruction import Instruction


class Lsr(Instruction):
    def __init__(self):
        opcode = "lsr"
        suffixes = [""]
        registerPrefixes = ["x", "w"]
        numberOfOperators = 3
        shift = [""]
        immediates = ["", "#5"]
        bothAllowed = False
        super().__init__(opcode, suffixes, registerPrefixes, numberOfOperators, shift, immediates, bothAllowed)