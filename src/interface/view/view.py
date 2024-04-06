import os
import subprocess
from utils.config import config

info = config.get_use_interface("view")

script_dir = os.path.dirname(os.path.realpath(__file__))
main_path = os.path.join(script_dir, "main.py")

def run_command():
    command = [
        "python", main_path,
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
# print(config.get_use_interface("view", "character"))


# command = [
#     "D:\anaconda3\envs\eaiv\python.exe webui.py",
#     "--main_port", "7888",
#     "--webui_port", "7999"
# ]