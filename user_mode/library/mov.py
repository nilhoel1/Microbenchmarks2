import random
from library.instruction import Instruction


class Mov(Instruction):
    def __init__(self):
        opcode = "mov"
        suffixes = ["", "z", "k", "n"]
        registerPrefixes = ["x", "w"]
        numberOfOperators = 1
        shift = [""]
        immediates = [""]
        bothAllowed = False
        super().__init__(opcode, suffixes, registerPrefixes, numberOfOperators, shift, immediates, bothAllowed)