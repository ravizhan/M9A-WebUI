# /// script
# dependencies = [
#   "requirements-parser",
#   "nuitka",
# ]
# ///

import importlib.util
from pathlib import Path
import requirements
import subprocess
import sys
import os

def get_package_path(package_name):
    """动态获取已安装包的物理路径"""
    spec = importlib.util.find_spec(package_name)
    if spec is None or spec.submodule_search_locations is None:
        return None
    # 返回包的文件夹路径 (取第一个搜索位置)
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
                pkg_path
            ]
            
            try:
                run_command(nuitka_cmd)
            except subprocess.CalledProcessError as e:
                print(f"Failed to compile {package_name}: {e}")

if __name__ == "__main__":
    main()