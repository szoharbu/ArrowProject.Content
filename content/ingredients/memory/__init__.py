import random

from Utils.configuration_management import Configuration
from Tool.frontend.AR_API import AR
from Tool.frontend.sources_API import Sources

'''
load - store actions of a same memory.  
'''
@AR.ingredient_decorator(random=True, priority=Configuration.Priority.HIGH, tags=[Configuration.Tag.MEMORY])
class MemoryPairing_ing(AR.Ingredient):
    def __init__(self):
        self.mem = Sources.Memory(name="MemoryPairing_memory", init_value=random.randint(0, 0x1000))

    def init(self):
        AR.generate(src=self.mem)

    def body(self):
        for i in range(random.randint(2,5)):
            action = AR.choice(values=["load","store"])
            if action == "load":
                if Configuration.Architecture.x86:
                    AR.generate(src=self.mem, comment="load instruction")
                else:
                    AR.generate(query=(AR.Instruction.group == "load"), src=self.mem, comment="load instruction")
            else: # action == "store":
                AR.generate(dest=self.mem, comment="store instruction")
            yield

    def final(self):
        pass

''' 
B2B bursts of memory stores , using a shared memory
'''
@AR.ingredient_decorator(random=True, priority=Configuration.Priority.HIGH, tags=[Configuration.Tag.MEMORY])
class B2BMemoryStress_ing(AR.Ingredient):

    def __init__(self):
        self.mem = Sources.Memory(shared=True)

    def init(self):
        pass

    def body(self):
        for i in range(random.randint(2, 4)):
            burst_count = AR.rangeWithPeak(start=1,end=6,peak=2, peak_width="narrow")
            AR.generate(instruction_count=burst_count, dest=self.mem)
            yield

    def final(self):
        pass

'''
stressing multiple memory access of the same memory, with different sizes and offsets
'''
@AR.ingredient_decorator(random=True, priority=Configuration.Priority.HIGH, tags=[Configuration.Tag.MEMORY])
class MemoryOverlapping(AR.Ingredient):

    def __init__(self):
        self.mem_block = Sources.MemoryBlock(byte_size=random.randint(8,16), init_value=random.randint(1,0xf00000))

    def init(self):
        pass

    def body(self):
        for i in range(random.randint(2, 6)):
            action = AR.choice(values=["load", "store"])
            size = AR.choice(values=[1, 2, 4, 8])
            offset = random.randint(0, self.mem_block.byte_size - size)
            partial_mem = Sources.Memory(memory_block=self.mem_block, memory_block_offset=offset, byte_size=size)
            if action == "load":
                AR.generate(src=partial_mem, comment=f" partial memory load instruction ")
            else:  # store
                AR.generate(dest=partial_mem, comment=f" partial memory store instruction ")
            yield

    def final(self):
        pass
