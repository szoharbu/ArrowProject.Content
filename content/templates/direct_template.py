import random
from Utils.configuration_management import Configuration
from Tool.frontend.AR_API import AR
from Tool.frontend.sources_API import Sources

@AR.scenario_decorator(random=True, priority=Configuration.Priority.MEDIUM, tags=[Configuration.Tag.FEATURE_A, Configuration.Tag.SLOW])
def direct_scenario():
    AR.comment(comment="Direct scenario start here")
    for _ in range(20):
        reg = Sources.RegisterManager.get_and_reserve()
        number = AR.choice(values={7:30, random.randint(2,40):70})
        AR.asm(f"mov {reg}, {number}", comment=f"moving {number} into {reg}")
        Sources.RegisterManager.free(reg)

        AR.generate()
        AR.generate(src=reg)

@AR.scenario_decorator(random=True, priority=Configuration.Priority.MEDIUM, tags=[Configuration.Tag.FEATURE_A, Configuration.Tag.SLOW])
def direct_memory_stress_scenario():
    AR.comment(comment="Direct memory_stress scenario start here")
    for _ in range(20):
        mem = Sources.Memory(shared=True)
        action = AR.choice(values=["src","dest"])
        if action == "src":
            AR.generate(src=mem)
        else:
            AR.generate(dest=mem)

@AR.scenario_decorator(random=True, priority=Configuration.Priority.MEDIUM, tags=[Configuration.Tag.FEATURE_A, Configuration.Tag.SLOW])
def direct_memoryblock_stress_scenario():
    AR.comment(comment="Direct memory_block_stress scenario start here")
    mem_block = Sources.MemoryBlock(byte_size=random.randint(10,15), shared=True)
    for _ in range(20):
        byte_size = AR.choice(values=[1,2,4,8])
        max_offset = mem_block.byte_size - byte_size
        offset = random.randint(0, max_offset)
        mem = Sources.Memory(byte_size=byte_size, memory_block=mem_block, memory_block_offset=offset)
        action = AR.choice(values=["src","dest"])
        if action == "src":
            AR.generate(src=mem)
        else:
            AR.generate(dest=mem)