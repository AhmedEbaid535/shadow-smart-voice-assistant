command1 = None
command2 = None
class HardwareControlCommands:
    def __init__(self):
        self.feed = None
        self.value = None
        self.command_map = {
            "turn_on_big_light": self.turn_on_big_light,
            "turn_on_small_light": self.turn_on_small_light,
            "turn_off_big_light": self.turn_off_big_light,
            "turn_off_small_light": self.turn_off_small_light,
            "turn_on_fan": self.turn_on_fan,
            "turn_off_fan": self.turn_off_fan
        }

    def turn_on_big_light(self):
        print("Turning on light")
        self.feed = "big lamp"
        self.value = "on"
        return "Turning on big light"


    def turn_on_small_light(self):
        print("Turning on light")
        self.feed = "small lamp"
        self.value = "on"
        return "Turning on small light"

    def turn_off_big_light(self):
        print("Turning off light")
        self.feed = "big lamp"
        self.value = "off"
        return "Turning off big light"

    def turn_off_small_light(self):
        print("Turning off light")
        self.feed = "small lamp"
        self.value = "off"
        return "Turning off small light"

    def turn_on_fan(self):
        self.feed = "fan"
        self.value = "on"
        return "Turning on fan"

    def turn_off_fan(self):
        self.feed = "fan"
        self.value = "off"
        return "Turning off fan"