import os

def open_file(gui_instance, file_name, search_dir="C:\\"):
    default_extensions = [".jpg", ".png", ".mp3", ".mp4", ".img", ".jpeg", ".pdf"]

    found_path = None
    print(f"🔍 Searching in Explorer '{file_name}' in {search_dir}...")

    for root, dirs, files in os.walk(search_dir):
        try:
            for f in files:
                f_lower = f.lower()
                file_name_lower = file_name.lower()

                if f_lower == file_name_lower:
                    found_path = os.path.join(root, f)
                    break

                if "." not in file_name:
                    if any(f_lower.startswith(file_name_lower) and f_lower.endswith(ext) for ext in default_extensions):
                        found_path = os.path.join(root, f)
                        print(f"✅ Files Found: {found_path}")
                        break
                
            if found_path:
                break
        except Exception as e:
            print(f"⚠️ Failed to access {root}: {str(e)}")

    if found_path and os.path.exists(found_path):
        try:
            os.startfile(found_path)
            response_text = f"Master、one result found, {os.path.basename(found_path)} has been opened."
        except Exception as e:
            response_text = f"Master、Error opening file: {str(e)}"
    else:
        response_text = f"Master、{file_name} 0 result found, i cant find spesific file"

    print(response_text)
    gui_instance.ai_response_received.emit(response_text)

def open_folder(gui_instance, folder_name, search_dir="C:\\"):
    found_path = None
    print(f"🔍 Searching '{folder_name}' in {search_dir}...")
    gui_instance.ai_response_received.emit(f"Master、{folder_name}, I am looking for it.")

    for root, dirs, _ in os.walk(search_dir):
        try:
            for d in dirs:
                if d.lower() == folder_name.lower():
                    found_path = os.path.join(root, d)
                    print(f"✅ Folder Found: {found_path}")
                    break
                if found_path:
                    break
        except Exception as e:
            print(f"⚠️ failed to access {root}: {str(e)}")  # Log error akses

    if found_path and os.path.exists(found_path):
        try:
            os.startfile(found_path)
            response_text = f"Master、{folder_name} has been opened"
        except Exception as e:
            response_text = f"Master、Error opening Folder: {str(e)}"
    else:
        response_text = f"Master、{folder_name} 0 result found, i cant find spesific Folder"

    gui_instance.ai_response_received.emit(response_text)