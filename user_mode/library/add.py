from library.instruction import Instruction


class Add(Instruction):
    def __init__(self):
        opcode = "add"
        suffixes = ["", "s"]
        registerPrefixes = ["x", "w"]
        numberOfOperators = 3
        shift = ["", "lsl #12"]
        immediates = ["", "#5"]
        bothAllowed = True
        super().__init__(opcode, suffixes, registerPrefixes, numberOfOperators, shift, immediates, bothAllowed)