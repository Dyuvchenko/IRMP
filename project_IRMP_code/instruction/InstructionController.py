from queue import Queue


class InstructionController:
    # словарь, ключ которого название функции в виде строки, а значение - выполняемый код
    instructionsDict = dict()

    # текущие инструкции для выполнения
    __current_instructions__ = Queue()

    """ Получить инструкцию для выполнения """

    def get_current_instruction_or_none(self):
        if self.__current_instructions__.qsize() > 0:
            return self.__current_instructions__.get_nowait()
        else:
            return None

    """ добавить инструкцию (функцию) в очередь на исполнение """

    def add_in_instruction_execution_queue(self, instruction):
        self.__current_instructions__.put(instruction)

