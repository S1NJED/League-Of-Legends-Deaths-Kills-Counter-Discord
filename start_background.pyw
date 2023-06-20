import subprocess
import os

MAIN_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHONW = os.path.join(MAIN_DIRECTORY, ".env", "Scripts", "pythonw.exe")
RUN_SCRIPT = os.path.join(MAIN_DIRECTORY, "scripts", "run.py")

# Run run.py script within the virtual environment
subprocess.Popen([VENV_PYTHONW, RUN_SCRIPT])