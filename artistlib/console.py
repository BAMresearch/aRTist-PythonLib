import subprocess
import os

path = os.path.dirname(os.path.abspath(__file__))
correctedPath = path.replace("\\", "/")

cmd = subprocess.run(["python", correctedPath + "/remote_access.py"])