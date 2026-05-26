import time
import serial
import speech_recognition as sr
from google import genai

# 1. Setup Gemini API Client
# Replace with your actual Gemini API key
client = genai.Client(api_key="")

# 2. Setup Serial Communication with Arduino
# Change 'COM3' to whatever port your Arduino is using (e.g., '/dev/ttyUSB0' on Linux/Mac)
try:
    arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1)
    time.sleep(2) # Give the Arduino time to reset/initialize
    print("Connected to Arduino successfully!")
except Exception as e:
    print(f"Error connecting to Arduino: {e}")
    print("Make sure your Arduino IDE Serial Monitor is CLOSED.")
    exit()

# 3. Setup Microphone
recognizer = sr.Recognizer()
mic = sr.Microphone()

def send_to_arduino(text):
    """Sends a string of text to the Arduino over Serial."""
    print(f"Sending to LCD: {text}")
    # We add a '\n' so the Arduino knows the message is finished
    arduino.write(f"{text}\n".encode('utf-8'))

print("\nVoice Assistant is alive! Say something...")

while True:
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("\nListening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Processing speech...")
            
            # Convert speech to text using Google's free web recognizer
            user_text = recognizer.recognize_google(audio)
            print(f"You said: {user_text}")
            
            # Send your request to Gemini
            print("Asking the raptor-ai...")
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Give a super short answer (max 30 characters) to this: {user_text}"
            )
            
            # Clean up the response text
            reply = response.text.strip()
            print(f"raptor-ai replied: {reply}")
            
            # Send the shortened reply to your screen
            send_to_arduino(reply)
            
        except sr.WaitTimeoutError:
            print("Listening timed out. Speak up!")
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    time.sleep(1)
