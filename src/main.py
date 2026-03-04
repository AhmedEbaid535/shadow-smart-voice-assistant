import asyncio
from commands.hardware import HardwareControlCommands
from commands.software import SoftwareControlCommands
from speech.speech_communication import SpeechCommunication
from mqtt.adafruit_client import MqttCommunication

hardware_command = HardwareControlCommands()
software_command = SoftwareControlCommands()
speech_comm = SpeechCommunication(hardware_command, software_command)
mqtt_comm = MqttCommunication()

mqtt_comm.client_connect()

asyncio.run(speech_comm.speak("Hi, I'm shadow, your personal assistant."))

while True:
    wake_command = speech_comm.listen_for_wake_word_vosk()
    if wake_command == "shut down":
        asyncio.run(speech_comm.speak("Shutting down. Goodbye!"))
        exit(0)
    elif wake_command == "":
        asyncio.run(speech_comm.speak("Hi sir, I'm ready to listen"))
        while True:
            if not speech_comm.handle_talk():
                break
            if hardware_command.feed and hardware_command.value:
               mqtt_comm.send_commands(hardware_command.feed, hardware_command.value)
    elif wake_command:
        speech_comm.respond(wake_command)
        if hardware_command.feed and hardware_command.value:
            mqtt_comm.send_commands(hardware_command.feed, hardware_command.value)
        while True:
            if not speech_comm.handle_talk():
                break
            if hardware_command.feed and hardware_command.value:
                mqtt_comm.send_commands(hardware_command.feed, hardware_command.value)
