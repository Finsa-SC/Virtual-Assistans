import os
import subprocess


def open_application(gui_instance, app_name):
    app_paths = {
        "note": "notepad.exe",
        "cal": "calc.exe",
        "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "fox": r"C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        "edge": r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        "paint": "mspaint.exe",
        "code": r"C:\\Users\\user\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
        "git": r"C:\\Program Files\\Git\\git-bash.exe",
        "vs": r"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe",
        "steam": r"C:\Program Files (x86)\Steam\steam.exe",
        "ssms": r"C:\Program Files (x86)\Microsoft SQL Server Management Studio 20\Common7\IDE\Ssms.exe",
        "share": r"C:\Users\Public\Desktop\SHAREit.lnk",
        "android": r"C:\Users\user\Desktop\Android Studio.lnk"
    }   
    
    found_app = None
    for key in app_paths:
        if app_name.lower() in key:
            found_app = app_paths[key]
            break
    
    if found_app and os.path.exists(found_app):
        try:
            subprocess.Popen(found_app, shell=True)
            response_text = f"Master、{app_name} application has started successfully."
        except Exception as e:
            response_text = f"Master、An error occurred during startup {app_name} : {str(e)}"
    else:
        response_text = f"Master、{app_name} application could not be found."
    
    gui_instance.ai_response_received.emit(response_text)
    gui_instance.speak(response_text)
