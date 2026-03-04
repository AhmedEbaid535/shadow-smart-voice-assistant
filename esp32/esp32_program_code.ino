#include "AdafruitIO_WiFi.h"
#include "WiFi.h"

// Wi-Fi and Adafruit IO config
#define IO_USERNAME "IO_USERNAME"
#define IO_KEY      "IO_KEY"
#define WIFI_SSID   "WIFI_SSID"
#define WIFI_PASS   "WIFI_PASS"

AdafruitIO_WiFi io(IO_USERNAME, IO_KEY, WIFI_SSID, WIFI_PASS);

// Declare the feeds
AdafruitIO_Feed *bigLampControl = io.feed("big lamp");     // For big lamp
AdafruitIO_Feed *smallLampControl = io.feed("small lamp"); // For small lamp

int bigLampPin = 17;
int smallLampPin = 16;  // You can change this to any available GPIO

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Set LED pins as output
  pinMode(bigLampPin, OUTPUT);
  pinMode(smallLampPin, OUTPUT);

  digitalWrite(bigLampPin, HIGH);
  digitalWrite(smallLampPin, HIGH);

  // Setup the message handlers
  bigLampControl->onMessage(handleBigLampMessage);
  smallLampControl->onMessage(handleSmallLampMessage);

  // Start connection to Adafruit IO
  io.connect();

  // Wait until connected
  while (io.status() < AIO_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("Connected to Adafruit IO!");
}

void loop() {
  // Keep the connection and handle incoming messages
  io.run();
}

// Handler for "big lamp"
void handleBigLampMessage(AdafruitIO_Data *data) {
  String raw = data->toString();
  if (raw == "ON") {
    digitalWrite(bigLampPin, LOW);
  } else if (raw == "OFF") {
    digitalWrite(bigLampPin, HIGH);
    Serial.println("Big Lamp OFF");
  }
}

// Handler for "small lamp"
void handleSmallLampMessage(AdafruitIO_Data *data) {
  String raw = data->toString();
  if (raw == "ON") {
    digitalWrite(smallLampPin, LOW);
  } else if (raw == "OFF") {
    digitalWrite(smallLampPin, HIGH);
}
}