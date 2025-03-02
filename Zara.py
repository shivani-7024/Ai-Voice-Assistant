import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import json
import music_library as ml

recognizer = sr.Recognizer()
engine = pyttsx3.init()

GEMINI_API_KEY = "YOUR_API_KEY"

def get_gemini_response(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        # Extract response text
        try:
            answer = result["candidates"][0]["content"]["parts"][0]["text"]
            return answer
        except KeyError:
            return "❌ Error: Unexpected API response format."
    else:
        return f"❌ API Error: {response.status_code} - {response.text}"


def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):

    command = c.lower()
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com/")

    elif command.startswith("play"):
        for key in ml.music.keys():
            if command == key.lower().strip():
                song_url = ml.music[key]
                print(f"🎵 Playing: {command}")
                webbrowser.open(song_url)
                return
        else:
            speak("Song not found!")
    else:
        response = get_gemini_response(command)
        print(f"🤖 Gemini Response: {response}")
        speak(response)
    print(c)

if __name__ == "__main__":
    speak("Initializing Zara")
    while True:
        r = sr.Recognizer()

        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            try:
                word = r.recognize_google(audio)
            except Exception:
                print("❌ Could not understand audio")
                continue

            if(word.lower() == "zara"):
                speak("Yaa")
                with sr.Microphone() as source:
                    print("Zara Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)
                    
        except Exception as e:
            print("Error; {0}".format(e))
        except KeyboardInterrupt:
            print("\n❌ Program stopped manually.")
            exit()
