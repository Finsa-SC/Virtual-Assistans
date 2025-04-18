import os
import time
from gtts import gTTS
from playsound import playsound

def speak_gtts(text):
    filename = f"temp_tts_{int(time.time())}.mp3"
    tts = gTTS(text=text, lang="ja", tld="co.jp")
    tts.save(filename)
    
    playsound(filename)
    os.remove(filename)

def speak_and_do(gui_instance, user_input, action_func):
    response_text = f"Master, {user_input} will execute in ３、２、１"
    gui_instance.skip_tts = True
    gui_instance.ai_response_received.emit(response_text)
    time.sleep(0.5)
    speak_gtts(response_text)
    time.sleep(0.3)
    action_func()

def shutdown(gui_instance, user_input):
    speak_and_do(gui_instance, user_input, lambda: os.system("shutdown /s /t 0"))

def restart(gui_instance, user_input):
    speak_and_do(gui_instance, user_input, lambda: os.system("shutdown /r /t 0"))

def sleep(gui_instance, user_input):
    speak_and_do(gui_instance, user_input, lambda: os.system(
        "powershell -Command \"Add-Type -AssemblyName System.Windows.Forms; "
        "[System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false)\""
    ))

def hibernate(gui_instance, user_input):
    speak_and_do(gui_instance, user_input, lambda: os.system("shutdown /h"))
