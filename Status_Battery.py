import psutil
import time
import threading
import os
from playsound import playsound
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class BatteryMonitor:
    def __init__(self, parent_gui=None):
        self.parent_gui = parent_gui
        self.notified_levels = set()
        self.monitor_thread = threading.Thread(target=self.monitor_battery, daemon=True)
        self.monitor_thread.start()
    
    def set_volume_max(self):
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(1.0, None)  # 100%
        except Exception as e:
            print("❌ Set max volume failed:", e)



    def play_mp3_warning(self):
        try:
            mp3_path = r"public/Alarm95_.mp3"
            playsound(mp3_path)
        except Exception as e:
            print("❌ Failed to play the warning sound:", e)


    def monitor_battery(self):
        while True:
            battery = psutil.sensors_battery()
            if battery is None:
                break

            percent = battery.percent
            plugged = battery.power_plugged

            if not plugged:
                if percent <= 10 and 10 not in self.notified_levels:
                    self.notify("Master, my energy is only 10%, please refill!", "Master, my energy is only 10%, please refill!")
                    self.notified_levels.add(10)
                elif percent <= 20 and 20 not in self.notified_levels:
                    self.notify("⚠️ Master, has only 20 percent of energy left.", "Master, has only 20 percent of energy left!")
                    self.notified_levels.add(20)
                elif percent <= 5 and 5 not in self.notified_levels:
                    self.notify("💣 sorry master, you forced me to do this", "sorry master, you forced me to do this")
                    self.notified_levels.add(5)
                    time.sleep(8)
                    os.system("shutdown /s /t 1")
            else:
                if percent >= 90 and 90 not in self.notified_levels:
                    self.notify("🔋 Battery is at 90%, please unplug the charger.", "Battery is at 90%, please unplug the charger.")
                    self.notified_levels.add(90)
                elif percent >= 95 and 95 not in self.notified_levels:
                    self.notify("🔋 Master, I told you to unplug the charger.", "Master, I told you to unplug the charger.")
                    self.notified_levels.add(95)
                elif percent >= 98 and 98 not in self.notified_levels:
                    self.notified_levels.add(98)
                    self.set_volume_max()
                    self.notify("🔊 Master! Unplug it now!! I'm serious!!", "Master! Unplug it now!! I'm serious!!")
                    time.sleep(8)
                    self.play_mp3_warning()

            time.sleep(60) 

    def notify(self, message, jvoice):
        if self.parent_gui:
            self.parent_gui.chat_display.append(f"<b>Fairy:</b> {message}")
            threading.Thread(target=self.parent_gui.speak, args=(jvoice,)).start()
        else:
            print(message)
