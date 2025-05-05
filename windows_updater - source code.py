import customtkinter as ctk
import requests
import zipfile
import os
import shutil
import subprocess
import sys
import tempfile
from threading import Thread

APP_DIR = r"C:\Program Files\AI Password Manager"
UPDATE_ZIP_URL = "https://AI-Password-Manager.github.io/apm.zip"
EXE_NAME = "AI Password Manager.exe"

class UpdaterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Password Manager Updater")
        self.geometry("600x150")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")

        self.label = ctk.CTkLabel(self, text="Preparing update...", font=("Segoe UI", 18))
        self.label.pack(pady=20)

        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.set(0)
        self.progress.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Starting...")
        self.status_label.pack(pady=10)

        self.start_update()

    def start_update(self):
        Thread(target=self.update_app, daemon=True).start()

    def update_app(self):
        try:
            self.status_label.configure(text="Downloading update...")
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, "apm.zip")

            r = requests.get(UPDATE_ZIP_URL, stream=True)
            total_size = int(r.headers.get('content-length', 0))
            downloaded = 0

            with open(zip_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percent = downloaded / total_size
                        self.progress.set(percent)
                        self.update_idletasks()

            self.status_label.configure(text="Extracting files...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            self.status_label.configure(text="Installing update...")
            self.progress.set(0)
            self.update_idletasks()

            items = os.listdir(temp_dir)
            total_items = len(items)
            for index, item in enumerate(items):
                src = os.path.join(temp_dir, item)
                dst = os.path.join(APP_DIR, item)

                if os.path.abspath(dst) == os.path.abspath(sys.argv[0]):
                    continue

                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

                self.progress.set((index + 1) / total_items)
                self.update_idletasks()

            self.status_label.configure(text="Update complete. Launching app...")
            exe_path = os.path.join(APP_DIR, EXE_NAME)
            subprocess.Popen([exe_path])
            self.quit()

        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")

if __name__ == "__main__":
    app = UpdaterApp()
    app.mainloop()
