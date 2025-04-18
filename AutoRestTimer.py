import time
import threading
import ctypes

class AutoRestTimer:
    def __init__(self, parent_gui=None):
        self.start_time = time.time()
        self.parent_gui = parent_gui
        self.rest_warning_sent = False
        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()

    def run_timer(self):
        while True:
            elapsed = time.time() - self.start_time

            if elapsed >= 25 * 60 and not self.rest_warning_sent:
                self.rest_warning_sent = True
                self.send_warning()
            elif elapsed >= 30 * 60:
                self.force_sleep()
                break

            time.sleep(5)

    def send_warning(self):
        if self.parent_gui:
            self.parent_gui.chat_display.append("<b>Fairy:</b> 💡 Master, it's been 25 minutes already. Let's take a break.")
            threading.Thread(target=self.parent_gui.speak, args=("そろそろ、休憩しましょう、マスター。",)).start()
        else:
            print("⚠️ Waktu istirahat! Silakan ambil jeda 5 menit!")

    def force_sleep(self):
        if self.parent_gui:
            self.parent_gui.chat_display.append("<b>Fairy:</b> ⏲️ Since the master is not resting, I will sleep😠.")
            threading.Thread(target=self.parent_gui.speak, args=("マスター、強制的にスリープします。おやすみなさい〜",)).start()
            time.sleep(10)
        ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)
