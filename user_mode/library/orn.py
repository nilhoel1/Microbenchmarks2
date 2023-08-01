from library.instruction import Instruction


class Orn(Instruction):
    def __init__(self):
        opcode = "orn"
        suffixes = [""]
        registerPrefixes = ["x", "w"]
        numberOfOperators = 3
        shift = ["", "lsl #12"]
        immediates = [""]
        bothAllowed = False
        super().__init__(opcode, suffixes, registerPrefixes, numberOfOperators, shift, immediates, bothAllowed)