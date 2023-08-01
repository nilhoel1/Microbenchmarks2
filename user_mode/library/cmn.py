from library.instruction import Instruction


class Cmn(Instruction):
    def __init__(self):
        opcode = "cmn"
        suffixes = [""]
        registerPrefixes = ["x", "w"]
        numberOfOperators = 2
        shift = ["", "lsl #12"]
        immediates = ["", "#5"]
        bothAllowed = True
        super().__init__(opcode, suffixes, registerPrefixes, numberOfOperators, shift, immediates, bothAllowed)