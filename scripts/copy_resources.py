import shutil
import os
import json

os.makedirs("build", exist_ok=True)
shutil.copytree("agent", "build/agent")
shutil.copytree("assets/resource","build/resource")
shutil.copy2("assets/interface.json","build")
with open("assets/interface.json", "r", encoding="utf-8") as f:
    interface = json.load(f)
interface["version"] = "3.17.4"
interface["custom_title"] = f"M9A 3.17.4 | 亿韭韭韭小助手"