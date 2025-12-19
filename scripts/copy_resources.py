import shutil
import os

os.makedirs("build", exist_ok=True)
shutil.copytree("agent", "build/agent")
shutil.copytree("assets/resource","build/resource")
shutil.copy2("assets/interface.json","build")