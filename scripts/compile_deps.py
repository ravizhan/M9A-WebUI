# /// script
# dependencies = [
#   "requirements-parser",
#   "nuitka",
# ]
# ///

import importlib.util
import os
from pathlib import Path
import requirements
import subprocess
import sys

def get_package_path(package_name):
    if package_name.lower() == 'pillow':
        spec = importlib.util.find_spec('PIL')
        if spec and spec.submodule_search_locations:
            return spec.submodule_search_locations[0]
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        return None
    if spec.submodule_search_locations is None:
        try:
            module = __import__(package_name)
            if hasattr(module, '__file__') and module.__file__:
                return os.path.dirname(module.__file__)
        except ImportError:
            pass
        return None
    return spec.submodule_search_locations[0]

def run_command(cmd):
    print(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)

def main():
    req_file = 'requirements.txt'
    if not os.path.exists(req_file):
        print(f"Error: {req_file} not found")
        return

    with open(req_file, 'r') as f:
        reqs = requirements.parse(f)
    
        for req in reqs:
            package_name = req.name
            if package_name == 'maafw' or not package_name:
                continue
            
            print(f'\n--- Installing package: {package_name} ---')
            
            run_command(["uv", "pip", "install", package_name])

            print(f'\n--- Compiling package: {package_name} ---')

            pkg_path = get_package_path(package_name)
        
            if not pkg_path:
                print(f"Warning: Could not find path for package '{package_name}', skipping...")
                continue
            
            nuitka_cmd = [
                sys.executable, "-m", "nuitka",
                "--mode=package",
                f"--output-dir=agent_deps",
                "--remove-output",
                "--assume-yes-for-downloads"
                pkg_path
            ]
            
            try:
                run_command(nuitka_cmd)
            except subprocess.CalledProcessError as e:
                print(f"Failed to compile {package_name}: {e}")

if __name__ == "__main__":
    main()