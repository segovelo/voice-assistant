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

        self.assistant = GenericAssistant("intents.json", intent_methods=self.mappings)
                                          #"file": self.create_file})
        self.assistant.train_model()

        self.root = tk.Tk()
        self.label = tk.Label(text="🤖", font=("Arial", 150, "bold"))
        self.label.pack()

        threading.Thread(target=self.run_assistant).start()

        self.root.mainloop()

    def create_file(self):
        print("Creating a new file...")
        self.speaker.say("Creating a new file")
        self.speaker.runAndWait()
        with open("test.txt", "w") as f:
            f.write("This a test text file")
            f.close()

    def hello(self):
        print("Inside hello function...")
        self.speaker.say("Hello Sebastian , how are you today?")
        self.speaker.runAndWait()

    def run_assistant(self):
        while True:
            try:
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)

                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()

                    if "listen" in text:
                        print("Listening... 🎤")
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
                                    print("Bot: ",response)
                                    self.speaker.say(response)
                                    self.speaker.runAndWait()
                            self.label.config(fg="black")
            except speech_recognition.UnknownValueError:
                print("Exception  speech_recognition.UnknownValueError !")
                self.recognizer = speech_recognition.Recognizer()
                self.speaker.say("I did not understand, please try again")
                self.speaker.runAndWait()

            except:
                print("Exception occurred !")
                self.label.config(fg="black")
                continue
    mappings = {
        "file": create_file,
        "greeting": hello
    }


Assistant()
