import pyttsx3

class _TTS:

    engine = None
    rate = None
    def __init__(self):
        self.engine = pyttsx3.init()
        # зададим свойства
        self.engine.setProperty('rate', 150)  # скорость речи
        self.engine.setProperty('volume', 0.9)  # громкость (0-1)
        # Задать голос по умолчанию
        self.engine.setProperty('voice', 'ru')


    def start(self,text_):
        self.engine.say(text_)
        self.engine.runAndWait()