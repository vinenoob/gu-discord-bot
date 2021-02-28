from gtts import gTTS

def generateTTS(whatToSay: str, filename: str):
    tts = gTTS(text = whatToSay, lang="en", slow=False)
    tts.save(filename)