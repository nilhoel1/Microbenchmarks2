from library.instruction import Instruction


class Sbc(Instruction):
    def __init__(self):
        opcode = "sbc"
        suffixes = ["", "s"]
        registerPrefixes = ["x", "w"]
        numberOfOperators = 3
        shift = [""]
        immediates = [""]
        bothAllowed = False
        super().__init__(opcode, suffixes, registerPrefixes, numberOfOperators, shift, immediates, bothAllowed)