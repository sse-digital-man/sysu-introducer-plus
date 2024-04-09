import os
import subprocess
from utils.config import config

os.chdir("src\\interface\\view\\EasyAIVtuber")

info = config.get_use_interface("view")

def run_command():
    command = [
        "python", "main.py",
        "--character", str(info["character"]),
        "--output_size", str(info["output_size"]),
        "--simplify", str(info["simplify"]),
        "--output_webcam", str(info["output_webcam"]),
        "--model", str(info["model"]),
        "--anime4k",
        "--sleep", str(info["sleep"]),
        "--port", str(info["port"])
    ]
    subprocess.run(command)
    
if __name__ == '__main__':
    run_command()