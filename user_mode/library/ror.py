from library.instruction import Instruction


class Ror(Instruction):
    def __init__(self):
        opcode = "ror"
        suffixes = [""]
        registerPrefixes = ["x", "w"]
        numberOfOperators = 3
        shift = [""]
        immediates = ["", "#5"]
        bothAllowed = False
        super().__init__(opcode, suffixes, registerPrefixes, numberOfOperators, shift, immediates, bothAllowed)