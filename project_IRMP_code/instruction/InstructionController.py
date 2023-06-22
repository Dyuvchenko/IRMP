from queue import Queue
from instruction.Instruction import Instruction


class InstructionController:
    # множество из Instruction
    instructionsSet: set = set()

    # текущие инструкции для выполнения
    __current_instructions__ = Queue()

    current_instruction: Instruction = None

    """ Получить инструкцию для выполнения """

    def __init__(self):
        self.current_instruction = Instruction()
        self.current_instruction .name = "Команда отсутствует"
        self.current_instruction .status_current_instruction = "Команда отсутствует"

    def get_current_instruction_or_none(self):
        if self.__current_instructions__.qsize() > 0:
            self.current_instruction = self.__current_instructions__.get()
            return self.current_instruction
        else:
            return None

    """ добавить инструкцию (функцию) в очередь на исполнение """

    def add_in_instruction_execution_queue(self, instruction):
        self.__current_instructions__.put(instruction)

    def find_instruction(self, name_instruction):
        for instruction in self.instructionsSet:
            if instruction.name.lower() == name_instruction.lower():
                return instruction

    def add_instruction(self, name, function):
        instruction = Instruction()
        instruction.name = name
        instruction.function = function
        self.instructionsSet.add(instruction)
