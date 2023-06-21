import logging
import threading
import json

import pyttsx3
from vosk import Model, KaldiRecognizer
import os
import pyaudio

import ProjectConsts
from externalControllers.VoiceGuidance.TTS import _TTS


class VoiceGuidanceController:
    """Логгер"""
    _logger_ = logging.getLogger()

    __model = None
    __rec = None
    __stream = None
    __engine = None

    def __init__(self):
        self.configuration_up_voice_work()

    def main_recognition(self):
        self._logger_.info("Стар процесса распознавания")
        while True:
            data = self.__stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                break
            if self.__rec.AcceptWaveform(data):
                recognized_text = ""
                try:
                    recognized_text = json.loads(self.__rec.Result())['text']
                except Exception:
                    self._logger_.error("Ошибка распознавания")
                self.processing_of_recognition_results(recognized_text)

    def configuration_up_voice_work(self):
        self._logger_.info("Стар инициализации голосового сопровождения")
        self.__model = Model(
            ProjectConsts.RootDerictory + "externalControllers/VoiceGuidance/vosk-model-small-ru-0.22")  # полный путь к модели
        self.__rec = KaldiRecognizer(self.__model, 44100)
        p = pyaudio.PyAudio()
        self.__stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=44100
        )
        self.__stream.start_stream()

        voice_recognition_thread = threading.Thread(target=self.main_recognition)  # запускаем основной процесс core
        voice_recognition_thread.start()

        self._logger_.info("Голосовое сопровождение успешно инициализировано")
        pass

    def processing_of_recognition_results(self, recognized_text):
        if recognized_text != "":
            self._logger_.info("Распознанный текст: " + recognized_text)
            pass

    def user_verification(self):
        pass

    def play_sound(self, text):
        tts = _TTS()
        tts.start(text)
        del (tts)
