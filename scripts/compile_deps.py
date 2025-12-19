# /// script
# dependencies = [
#   "requirements-parser",
#   "nuitka",
# ]
# ///

import requirements
import subprocess
import sys
import os

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
            
            nuitka_cmd = [
                sys.executable, "-m", "nuitka",
                "--module",
                "--mode=package",
                f"--output-dir=agent_deps/{package_name}",
                f"--include-package={package_name}",
                f"--include-package-data={package_name}",
                "--follow-imports",
                "--remove-output"
            ]
            
            try:
                run_command(nuitka_cmd)
            except subprocess.CalledProcessError as e:
                print(f"Failed to compile {package_name}: {e}")

if __name__ == "__main__":
    main()