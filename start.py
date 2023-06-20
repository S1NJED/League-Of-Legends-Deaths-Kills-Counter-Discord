import subprocess
import os

MAIN_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(MAIN_DIRECTORY, ".env", "Scripts", "python.exe")
RUN_SCRIPT = os.path.join(MAIN_DIRECTORY, "scripts", "run.py")

# Run run.py script within the virtual environment
subprocess.Popen([VENV_PYTHON, RUN_SCRIPT])