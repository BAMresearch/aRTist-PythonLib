import subprocess
import os

path = os.path.dirname(os.path.abspath(__file__))
correctedPath = path.replace("\\", "/")


def main():
    subprocess.run(["python", correctedPath + "/remote_access.py"])


if __name__ == "__main__":
    main()
