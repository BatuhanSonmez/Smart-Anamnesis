import speech_recognition as sr
import threading

class SpeechRecognitionApp:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.transcription = ""

    def start_listening(self):
        self.is_listening = True
        transcription_thread = threading.Thread(target=self.listen_and_update)
        transcription_thread.start()

    def stop_listening(self):
        self.is_listening = False

    def listen_and_update(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, phrase_time_limit=60)
                    recognized_text = self.recognizer.recognize_google(audio, language="tr-TR")
                    self.transcription += recognized_text + "\n"  # Add new transcription as a new line
                except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
                    continue
