#  Shadow – Smart Voice Assistant (Python + ESP32 + MQTT + Automation)

Shadow is a smart voice assistant built using **Python**, designed to interact with users through **voice commands & questions**, understand intentions using **AI**, answer the questions,  and control **IoT devices (ESP32)** through **MQTT (Adafruit IO)**.

The assistant listens for a wake word, processes speech input, executes hardware or software actions, and responds with natural voice feedback.

---

##  Features

-  Wake-word based voice activation  
-  AI-powered command understanding (Ollama – Mistral)  
-  Natural text-to-speech responses  
-  Speech recognition (Google Speech + VOSK)
-  Questions & Commands responding  
-  IoT device control using ESP32 via MQTT  
-  Hardware control:
  - Turn lights ON / OFF
  - Fan control
  - Brightness adjustment
-  Software control:
  - Media play / pause
  - Volume control
-  Clean, modular, and scalable architecture

---

##  Project Structure

```
shadow_assistant/
│
├── esp32/
│   └── esp32_program_code.ino
│
├── src/
│   ├── commands/
│   │   ├── hardware.py
│   │   ├── software.py
│   │   └── __init__.py
│   │
│   ├── mqtt/
│   │   ├── adafruit_client.py
│   │   └── __init__.py
│   │
│   ├── speech/
│   │   ├── speech_communication.py
│   │   └── __init__.py
│   │
│   └── main.py
│
├── config.py
├── config.example.py
├── .gitignore
└── README.md

---

##  Technologies Used

- Python 3.10+
- Ollama (Mistral model)
- SpeechRecognition
- VOSK
- Edge TTS
- Pygame
- MQTT (Adafruit IO)
- ESP32 (Arduino)

---

##  How It Works

1. The assistant waits for a wake word  
2. Voice input is converted to text  
3. AI model interprets the command  
4. Action is classified as:
   - Hardware command (ESP32 via MQTT)
   - Software command (media / brightness)
5. The assistant responds using voice output

---

##  Setup & Run

### 1️- Clone the repository
```bash
git clone https://github.com/your-username/shadow-assistant.git
cd shadow-assistant
```

### 2️- Install dependencies
```bash
pip install -r requirements.txt
```

### 3️- Configuration
- Copy `config.example.py` to `config.py`
- Add your:
  - Adafruit IO credentials
  - VOSK model path

### 4️- Run the assistant
```bash
python src/main.py
```

---

##  ESP32 Integration

- ESP32 subscribes to Adafruit IO feeds
- Commands are received via MQTT
- Hardware reacts in real-time (lights, fan, etc.)

---

##  Future Improvements

- Fast Responding
- Custom wake-word engine
- Mobile app integration
- Task reminders & notes
- Multi-language support
- GUI dashboard

---

##  Author

**Ahmed Ebaid**  
Embedded Systems & Python Developer  
IoT • Voice Assistants • AI Integration
