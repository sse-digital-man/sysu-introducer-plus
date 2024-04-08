import os
import subprocess
from utils.config import config

os.chdir("src\\interface\\view")

info = config.get_use_interface("view")

def run_command():
    command = [
        "python", "main.py",
        "--character", info["character"],
        "--output_size", info["output_size"],
        "--simplify", info["simplify"],
        "--output_webcam", info["output_webcam"],
        "--model", info["model"],
        "--anime4k",
        "--sleep", info["sleep"],
        "--port", info["port"]
    ]
    subprocess.run(command)

run_command()
