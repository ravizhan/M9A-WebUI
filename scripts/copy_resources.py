import shutil
import os
import json

os.makedirs("build", exist_ok=True)
shutil.copytree("agent", "build/agent")
shutil.copytree("assets/resource","build/resource")
shutil.copy2("assets/interface.json","build")
with open("build/interface.json", "r", encoding="utf-8") as f:
    interface = json.load(f)
interface["version"] = "3.17.4"
interface["custom_title"] = "M9A 3.17.4 | 亿韭韭韭小助手"
interface["agent"] = {
        "child_exec": "./python/python.exe",
        "child_args": [
            "-u",
            "./agent/main.py"
        ],
        "timeout": -1
    },
with open("build/interface.json", "w", encoding="utf-8") as f:
    json.dump(interface, f, ensure_ascii=False, indent=4)