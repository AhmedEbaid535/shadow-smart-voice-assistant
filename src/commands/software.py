import pyautogui
import screen_brightness_control as sbc

class SoftwareControlCommands:
    def __init__(self):
        self.command_map = {
            "play_the_video": self.play_pause,
            "pause": self.play_pause,
            "volume_up": self.volume_up,
            "volume_down": self.volume_down,
            "mute": self.mute,
            "set_brightness_to": self.set_brightness_command

        }

    def play_pause(self):
        pyautogui.press("playpause")


    def volume_up(self, steps=5):
        for _ in range(steps):
           pyautogui.press("volumeup")
        return "Volume up"


    def volume_down(self, steps =5):
        for _ in range(steps):
           pyautogui.press("volumedown")
        return "Volume down"

    def mute(self):
        pyautogui.press("volumemute")
        return "mute"

    def set_brightness_command(self, level):
        sbc.set_brightness(level)
        return f"Brightness set to {level}%"