# Class to generate the list of instructions which you want to benchmark

from library.add import Add
from library.sub import Sub
from library.adc import Adc
from library.adr import Adr
from library.ands import And
from library.bic import Bic
from library.cmn import Cmn
from library.cmp import Cmp
from library.eor import Eor
from library.orn import Orn
from library.orr import Orr
from library.sbc import Sbc
from library.asr import Asr
from library.mov import Mov
from library.mvn import Mvn
from library.lsl import Lsl
from library.lsr import Lsr
from library.ror import Ror
from library.nop import Nop

class Generator():
    def __init__():
        blocks = []
    
    def generate():
        blocks = []
        blocks.extend(Add().generate_instruction_block())
        blocks.extend(Adc().generate_instruction_block())
        blocks.extend(Adr().generate_instruction_block())
        blocks.extend(And().generate_instruction_block())
        blocks.extend(Asr().generate_instruction_block())
        blocks.extend(Bic().generate_instruction_block())
        blocks.extend(Cmn().generate_instruction_block())
        blocks.extend(Cmp().generate_instruction_block())
        blocks.extend(Eor().generate_instruction_block())
        blocks.extend(Lsl().generate_instruction_block())
        blocks.extend(Lsr().generate_instruction_block())
        blocks.extend(Mov().generate_instruction_block())
        blocks.extend(Mvn().generate_instruction_block())
        blocks.extend(Nop().generate_instruction_block())
        blocks.extend(Orn().generate_instruction_block())
        blocks.extend(Orr().generate_instruction_block())
        blocks.extend(Ror().generate_instruction_block())
        blocks.extend(Sbc().generate_instruction_block())
        blocks.extend(Sub().generate_instruction_block())

        return blocks