from library.instruction import Instruction


class Adc(Instruction):
    def __init__(self):
        opcode = "adc"
        suffixes = ["", "s"]
        registerPrefixes = ["x", "w"]
        numberOfOperators = 3
        shift = [""]
        immediates = [""]
        bothAllowed = False
        super().__init__(opcode, suffixes, registerPrefixes, numberOfOperators, shift, immediates, bothAllowed)