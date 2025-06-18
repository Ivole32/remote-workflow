import os
import sys
import subprocess
import shutil
from pathlib import Path
import platform

venv_dir = Path("remote-workflow")
requirements_file = Path("requirements.txt")

def create_venv():
    if not venv_dir.exists():
        print("[INFO] Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
        print(f"[OK] Virtual environment created at: {venv_dir.resolve()}")
    else:
        print(f"[INFO] Virtual environment already exists at: {venv_dir.resolve()}")

    python_executable = (
        venv_dir / "Scripts" / "python.exe" if os.name == "nt"
        else venv_dir / "bin" / "python"
    )

    print("[INFO] Upgrading pip...")
    subprocess.check_call([str(python_executable), "-m", "pip", "install", "--upgrade", "pip"])
    print("[OK] pip upgraded.")

    if requirements_file.exists():
        print("[INFO] Installing packages from requirements.txt...")
        subprocess.check_call([str(python_executable), "-m", "pip", "install", "-r", str(requirements_file)])
        print("[OK] Packages installed.")
    else:
        print("[WARN] requirements.txt not found.")

def remove_venv():
    if venv_dir.exists():
        print(f"[INFO] Removing virtual environment at: {venv_dir.resolve()}")
        shutil.rmtree(venv_dir)
        print("[OK] Virtual environment removed.")
    else:
        print("[INFO] No virtual environment to remove.")

def print_system_info():
    print("\n== System Info ==")
    print(f"System: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Architecture: {platform.machine()}")

if __name__ == "__main__":
    print_system_info()
    while True:
        action = input("Create or delete environment (c/D): ")
        if action == "c":
            create_venv()
            break
        elif action == "D":
            remove_venv()
            break
        else:
            print("[WARN] Wrong action type...")