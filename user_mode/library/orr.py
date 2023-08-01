from library.instruction import Instruction


class Orr(Instruction):
    def __init__(self):
        opcode = "orr"
        suffixes = [""]
        registerPrefixes = ["x", "w"]
        numberOfOperators = 3
        shift = ["", "lsl #12"]
        immediates = ["", "#1"]
        bothAllowed = False
        super().__init__(opcode, suffixes, registerPrefixes, numberOfOperators, shift, immediates, bothAllowed)