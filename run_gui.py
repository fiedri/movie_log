import subprocess
import sys
import os

if __name__ == "__main__":
    app_path = os.path.join(os.path.dirname(__file__), "tkinter_app", "app.py")
    subprocess.run([sys.executable, app_path])
