from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import time

text = "오늘은 좋은 하루 입니다."

# 1.번역
translated = GoogleTranslator(source="auto", target="en" ).translate(text)
print(translated)

# 2.tts
tts = gTTS(text=translated, lang="en")
tts.save("voice.mp3")

# 3.재생
pygame.mixer.init()
pygame.mixer.music.load("voice.mp3")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    time.sleep(0.1)
    




