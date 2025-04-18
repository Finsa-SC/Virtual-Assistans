from Open_APP import open_application
from file_searcher import open_file
from web_searcher import web_search
from AutoRestTimer import AutoRestTimer
from Status_Battery import BatteryMonitor
import os
import time
import threading
import requests
from gtts import gTTS
from playsound import playsound
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QEvent
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor, QIcon
import Command
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class AIChatGUI(QWidget):
    ai_response_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.rest_timer = AutoRestTimer(parent_gui=self)
        self.ai_response_received.connect(self.start_typing_effect)
        self.current_audio_file = None
        QTimer.singleShot(500, self.play_welcome_voice)
        self.battery_monitor = BatteryMonitor(parent_gui=self)

#Welcome aboard
    def get_current_volume(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current_volume = volume.GetMasterVolumeLevelScalar()
        return current_volume

    def set_volume(self, level):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level, None)

    def play_welcome_voice(self):
        threading.Thread(target=self._custom_welcome_voice, daemon=True).start()

    def _custom_welcome_voice(self):
        from datetime import datetime

        original_volume = self.get_current_volume()
        self.set_max_volume()

        try:
            playsound("public/Intro_Fairy.mp3")
            current_hour = datetime.now().hour
            if 5 <= current_hour < 11:
                greeting = "Good morning, Master."
            elif 11 <= current_hour < 18:
                greeting = "afternoon, master"
            else:
                greeting = "good evening, master"
            self.speak(greeting)
        finally:
            self.set_volume(original_volume)

    def set_max_volume(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(1.0, None)

    def initUI(self):
        self.setWindowIcon(QIcon("public/Fairy_Icons.ico"))
        self.setWindowTitle("Fairy-v2")
        self.setGeometry(100, 100, 500, 400)

        self.layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("font-size: 14pt;")
        self.layout.addWidget(self.chat_display)

        input_layout = QHBoxLayout()

        self.input_box = QTextEdit()
        self.input_box.setStyleSheet("font-size: 11pt; padding: 5px; border-radius: 8px;")
        self.input_box.setFixedHeight(30)
        self.input_box.installEventFilter(self)
        input_layout.addWidget(self.input_box)

        self.send_button = QPushButton("➤")
        self.send_button.setFixedSize(35, 35)
        self.send_button.setStyleSheet("""
            background-color: #62BCFF; 
            border-radius: 17px;
            font-size: 18px;
            font-weight: bold;
            color: white;
            text-align: center;
            qproperty-alignment: AlignCenter;
        """)
        input_layout.addWidget(self.send_button)

        self.layout.addLayout(input_layout)
        self.setLayout(self.layout)


    def get_ai_response(self, prompt):
        url = "http://localhost:11434/api/generate"
        data = {
            "model": "openchat:latest",
            "prompt": f"Your name is Fairy. You **must** always call the user is Master. User: {prompt}\nAI:",
            "stream": False
        }

        response = requests.post(url, json=data)
        result = response.json()
        ai_response = result.get("response", "Sorry, I can't reply to this message")
        self.ai_response_received.emit(ai_response)


    def send_message(self):
        user_input = self.input_box.toPlainText().strip()
        if user_input:
            self.chat_display.append(f"<b>You:</b> {user_input}")
            self.input_box.clear()
            self.input_box.setFixedHeight(30)
            QApplication.processEvents()

# Open Application
            if user_input.lower().startswith("open ") or user_input.lower().startswith("-op"):
                if user_input.lower().startswith("open "):
                    app_name = user_input[5:].strip()
                else:  # "-op"
                   app_name = user_input[3:].strip()
                open_application(self, app_name)
#Search File
            elif user_input.lower().startswith("search ") or user_input.lower().startswith("-s"):
                self.chat_display.append(f"<b>Fairy:</b> Searching...")
                print("Searching...")
                QApplication.processEvents()
                
                if user_input.lower().startswith("search "):
                    file_name = user_input[7:].strip()
                else:  # "-s"
                    file_name = user_input[3:].strip()
                
                jmessage = f"Master、Searching for {file_name}, I am looking for it.。"
                threading.Thread(target=self.speak, args=(jmessage,)).start()
                
                threading.Thread(target=open_file, args=(self, file_name)).start()
            elif user_input.lower().startswith("-of "):
                self.chat_display.append(f"<b>Fairy:</b> Search for Folder name {user_input}...")
                
#Search Google                
            elif user_input.lower().startswith(f"/") or user_input.lower().startswith(f"findme "):
                self.chat_display.append(f"<b>Fairy:</b> Searching {user_input} in Google...")
                QApplication.processEvents()

                if user_input.lower().startswith("findme "):
                    query = user_input[7:].strip()
                else:
                    query = user_input[1:].strip()
                threading.Thread(target=web_search, args=(query, self)).start()
#Command    
            elif user_input.lower().strip() == "shutdown":
                threading.Thread(target=Command.shutdown, args=(self, user_input)).start()
            elif user_input.lower().strip() == "restart":
                threading.Thread(target=Command.restart, args=(self, user_input)).start()
            elif user_input.lower().strip() == "sleep":
                threading.Thread(target=Command.sleep, args=(self, user_input)).start()
            elif user_input.lower().strip() == "hibernate":
                threading.Thread(target=Command.hibernate, args=(self, user_input)).start()
#Fairy  Response
            else:
                thread = threading.Thread(target=self.get_ai_response, args=(user_input,))
                thread.start()

#Shift Enter
    def eventFilter(self, obj, event):
        if obj == self.input_box and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return:
                if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
                    # Shift + Enter = Add new line
                    self.input_box.insertPlainText("\n")
                else:
                    # Enter = send message
                    self.send_message()
                return True

            lines = self.input_box.toPlainText().count("\n") + 1
            self.input_box.setFixedHeight(min(30 + (lines * 15), 100))

        return super().eventFilter(obj, event)


    def set_speaking(self, state: bool):
        self.speaking = state

    def speak(self, text):
        if hasattr(self, "speaking") and self.speaking:
            return
        self.speaking = True

        original_volume = self.get_current_volume()
        self.set_max_volume()

        try:
            filename = f"tts_{time.time()}.mp3"
            tts = gTTS(text=text, lang="en")
            tts.save(filename)
            playsound(filename)
            os.remove(filename)
        finally:
            self.set_volume(original_volume)
            self.speaking = False





#------------------------<Desigdn>--------------------------#

    def start_typing_effect(self, ai_response):
        self.send_button.setEnabled(False)
        
        self.chat_display.append("")
        
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertHtml("<b><span style='color:white;'>Fairy:</span></b> ")
        
        self.response_format = QTextCharFormat()
        self.response_format.setForeground(QColor("lightblue"))
        cursor.setCharFormat(self.response_format)
        self.chat_display.setTextCursor(cursor)
        
        self.typing_text = ai_response
        self.typing_index = 0
        
        self.typing_timer = QTimer()
        self.typing_timer.setInterval(70)
        self.typing_timer.timeout.connect(self.add_next_character)
        self.typing_timer.start()

        if not hasattr(self, 'skip_tts') or not self.skip_tts:
            tts_thread = threading.Thread(target=self.speak, args=(ai_response,))
            tts_thread.start()
        else:
            self.skip_tts = False


    def add_next_character(self):
        if self.typing_index < len(self.typing_text):
            char = self.typing_text[self.typing_index]
            cursor = self.chat_display.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)
            cursor.setCharFormat(self.response_format)
            cursor.insertText(char)
            self.chat_display.setTextCursor(cursor)
            self.typing_index += 1
        else:
            self.typing_timer.stop()
            self.typing_timer.deleteLater()
            del self.typing_timer, self.typing_text, self.typing_index
            self.send_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication([])
    window = AIChatGUI()
    window.show()
    app.exec()
