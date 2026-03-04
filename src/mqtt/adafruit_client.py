import paho.mqtt.client as mqtt
import time
from config import ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY

class MqttCommunication:
    def __init__(self):
        self.connected = False
        self.client = mqtt.Client()
        self.client.username_pw_set(
            ADAFRUIT_IO_USERNAME,
            ADAFRUIT_IO_KEY
        )
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to Adafruit IO.")
            self.connected = True
        else:
            print("Failed to connect. Code:", rc)
            self.connected = False

    def client_connect(self):
        self.client.connect("io.adafruit.com", 1883, 60)
        self.client.loop_start()

        timeout = 10
        start_time = time.time()
        while not self.connected and (time.time() - start_time) < timeout:
            time.sleep(0.1)

        if not self.connected:
            print("Could not connect to MQTT broker. Exiting.")
            self.client.loop_stop()
            self.client.disconnect()
            exit(1)

    def send_commands(self,feed,value):
        try:
                feed_name = feed.strip()
                feed_value = value.strip().upper()
                if feed_value in ["ON", "OFF"]:
                    topic = f"{ADAFRUIT_IO_USERNAME}/feeds/{feed_name}"
                    if self.connected:
                        self.client.publish(topic, feed_value)
                    else:
                        print("Not connected to MQTT broker. Cannot send message.")
                else:
                    print("Invalid input. Please type 'on', 'off', or 'exit'.")
        except KeyboardInterrupt:
            print("\nInterrupted by user.")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Disconnected from Adafruit IO.")

#Run
if __name__ == '__main__':
    communication1 = MqttCommunication()
    communication1.client_connect()
    communication1.send_commands()
    communication1.disconnect()