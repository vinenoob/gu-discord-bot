from gtts import gTTS

def generateTTS(whatToSay: str, filename: str):
    tts = gTTS(text = whatToSay, lang="en", slow=False)
    tts.save(filename)

if __name__ == "__main__":
    generateTTS("Pussy ass son of a bitch", "hello.mp3")
    print("TTS generated")