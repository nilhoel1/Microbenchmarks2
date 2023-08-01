from library.instruction import Instruction


class Mvn(Instruction):
    def __init__(self):
        opcode = "mvn"
        suffixes = [""]
        registerPrefixes = ["x"]
        numberOfOperators = 2
        shift = [""]
        immediates = [""]
        bothAllowed = False
        super().__init__(opcode, suffixes, registerPrefixes, numberOfOperators, shift, immediates, bothAllowed)