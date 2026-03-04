import os
import json
import asyncio
import pygame
import ollama
import speech_recognition as sr
import edge_tts
from vosk import Model, KaldiRecognizer
from config import VOSK_MODEL_PATH

class SpeechCommunication:
    def __init__(self, hardware_control, software_control):
        self.hardware_command = hardware_control
        self.software_command = software_control
        # Initialize recognizer and pygame mixer
        self.recognizer = sr.Recognizer()
        pygame.mixer.init()

        # History for chatting
        self.MAX_HISTORY = 6
        self.chat_history = [
            {
                "role": "system",
                "content": (
                    "You are a smart voice assistant called Shadow.\n\n"
                    "Respond ONLY with a JSON object in one of these formats:\n\n"
                    "For commands:\n"
                    '{ "type": "command", "action": "turn_on_light" }\n\n'
                    "Available actions:\n"
                    '1- turn_on_big_light\n'
                    '2- turn_off_big_light\n'
                    '3- turn_on_small_light\n'
                    '4- turn_off_small_light\n'
                    '5- turn_on_fan\n'
                    '6- turn_off_fan\n'
                    '7- what_is_the_time\n'
                    '8- play_the_video\n'
                    '9- pause\n'
                    '10- volume_up\n'
                    '11- volume_down\n'
                    '12- mute\n'
                    '13- set_brightness_to_[value] (e.g., set_brightness_to_70)\n\n'
                    "If the type is not a command, respond with:\n"
                    '{ "type": "response", "text": "Your short answer here." }\n\n'
                    "In this case, the 'text' field must contain one or two short sentences only.\n"
                    "Do not use 'content' or any other keys — always use 'text' for regular replies.\n"
                    "Always reply with a single valid JSON object. No extra explanations, no markdown, no natural language outside the JSON."
                )
            }
        ]
        # Initialize VOSK model
        self.model = Model(VOSK_MODEL_PATH)

    def listen_for_wake_word_vosk(self):
        rec = KaldiRecognizer(self.model, 16000)

        with sr.Microphone() as source:
            print("🎧 Waiting for wake word...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            try:
                audio = self.recognizer.listen(source, timeout=20)
                data = audio.get_raw_data(convert_rate=16000, convert_width=2)

                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                else:
                    result = json.loads(rec.PartialResult())

                text = result.get("text", result.get("partial", "")).lower()
                print(f"Detected: {text}")

                if "shutdown" in text or "shut down" in text:
                   command = "shut down"
                   return command

                if "shadow" in text:
                    command = text.replace("shadow", "")
                    return command if command else ""

            except Exception as e:
                print("Error in wake word detection:", e)
        return False

    async def speak(self, text):
        tts = edge_tts.Communicate(text, voice="en-US-GuyNeural")
        await tts.save("speech.mp3")

        pygame.mixer.music.load("speech.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        await asyncio.sleep(0.2)

        try:
            os.remove("speech.mp3")
        except PermissionError:
            print("Couldn't delete speech.mp3 — still in use.")


    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            try:
                audio = self.recognizer.listen(source, timeout=10)
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                asyncio.run(self.speak("I'm ready to listen to what you want to say"))
            except sr.RequestError:
                asyncio.run(self.speak("Speech service is not available right now."))
        return None

    def respond(self, text):
        if "shutdown" in text.lower() or "shut down" in text.lower():
            asyncio.run(self.speak("Shutting down. Goodbye!"))
            exit(0)

        if "thank you" in text.lower():
            asyncio.run(self.speak("You're welcome, goodbye!"))
            return False

        self.chat_history.append({"role": "user", "content": text})


        try:
            print("processing...")
            response = ollama.chat(
                model='mistral',
                messages=self.chat_history
            )

            answer = response['message']['content']
            try:
                data = json.loads(answer)

                if isinstance(data, dict) and data.get("type") == "command":
                    action = data.get("action")
                    if action in self.hardware_command.command_map:
                        message = self.hardware_command.command_map[action]()
                        if message:
                            asyncio.run(self.speak(message))
                    #for brightness
                    elif action.startswith("set_brightness_to"):
                        try:
                            level = int(''.join(filter(str.isdigit, action)))
                            message = self.software_command.set_brightness_command(level)
                            if message:
                                asyncio.run(self.speak(message))
                        except ValueError:
                            asyncio.run(self.speak("I couldn't understand the brightness level."))
                    elif action in self.software_command.command_map:
                        message = self.software_command.command_map[action]()
                        if message:
                            asyncio.run(self.speak(message))
                    else:
                        print("Unknown command.")
                        print(data)
                elif isinstance(data, dict) and "text" in data:
                    print(f"Shadow says: {answer}")
                    asyncio.run(self.speak(data["text"]))
            except json.JSONDecodeError:
                    # Not JSON at all — just speak as natural language
                    print(f"Shadow says: {answer}")
                    asyncio.run(self.speak(answer))

            self.chat_history.append({"role": "assistant", "content": answer})

            if len(self.chat_history) > self.MAX_HISTORY + 1:
                self.chat_history = [self.chat_history[0]] + self.chat_history[-self.MAX_HISTORY:]

        except Exception as e:
            print("Error:", e)
            asyncio.run(self.speak("Sorry, I couldn't connect to my brain."))

        return True

    def handle_talk(self):
            user_input = self.listen()
            if user_input:
               return self.respond(user_input)
            return True


    def main(self):
        asyncio.run(self.speak("Hi, I'm shadow, your personal assistant."))
        while True:
            command = self.listen_for_wake_word_vosk()
            if command == "shut down":
                asyncio.run(self.speak("Shutting down. Goodbye!"))
                exit(0)
            elif command == "":
                asyncio.run(self.speak("Hi sir, I'm ready to listen"))
                self.handle_talk()
            elif command:
                self.respond(command)
                self.handle_talk()