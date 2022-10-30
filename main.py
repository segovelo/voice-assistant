from ast import And
import sys
import threading
import tkinter as tk
import speech_recognition
import pyttsx3 as tts
from datetime import datetime
from neuralintents import GenericAssistant


class Assistant:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate", 150)

        self.assistant = GenericAssistant("intents.json", intent_methods={
                                          "file": self.create_file})
        self.assistant.train_model()

        self.root = tk.Tk()
        self.label = tk.Label(text="🤖", font=("Arial", 120, "bold"))
        self.stopButton = tk.Button(justify="left", height=2, width=20, text ="Stop", command = exit)
        self.label.pack()
        self.stopButton.pack()

        threading.Thread(target=self.run_assistant).start()

        self.root.mainloop()

    def create_file(self):
        with open("test.txt", "w") as f:
            f.write("This a test text file")
            f.close()

    def run_assistant(self):
        while True:
            try:
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)

                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()

                    if "wake up" in text:
                        self.label.config(fg="red")
                        audio = self.recognizer.listen(mic)
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()
                        if text == "stop":
                            self.speaker.say("bye")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            self.root.destroy()
                            sys.exit()
                        else:
                            if text is not None:
                                response = self.assistant.request(text)
                                if response is not None:
                                    self.speaker.say(response)
                                    self.speaker.runAndWait()
                            self.label.config(fg="black")
            except:
                self.label.config(fg="black")
                continue

Assistant()
