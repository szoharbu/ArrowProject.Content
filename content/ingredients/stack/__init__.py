
import random
from Utils.configuration_management import Configuration
from Tool.frontend.AR_API import AR
from Tool.frontend.sources_API import Sources

@AR.ingredient_decorator(random=True, priority=Configuration.Priority.HIGH, tags=[Configuration.Tag.STACK])
class basic_stack_ing(AR.Ingredient):
    def init(self):
        pass

    def body(self):
        reg = Sources.RegisterManager.get()
        AR.Stack.push([reg])
        yield
        AR.Stack.pop([reg])

    def final(self):
        pass

@AR.ingredient_decorator(random=True, priority=Configuration.Priority.HIGH, tags=[Configuration.Tag.STACK])
class multi_stack_ing(AR.Ingredient):

    def __init__(self):
        self.count = random.randint(2,5)

    def init(self):
        pass

    def body(self):
        reglist = []
        for _ in range(self.count):
            reg = Sources.RegisterManager.get_and_reserve()
            reglist.append(reg)
        AR.Stack.push(reglist)
        for reg in reglist:
            Sources.RegisterManager.free(reg)

        yield

        reglist = []
        for _ in range(self.count):
            reg = Sources.RegisterManager.get_and_reserve()
            reglist.append(reg)
        AR.Stack.pop(reglist)
        for reg in reglist:
            Sources.RegisterManager.free(reg)

    def final(self):
        pass