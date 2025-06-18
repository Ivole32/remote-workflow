import os
import sys
import subprocess
import shutil
from pathlib import Path
import platform
from logger import Logger

logger = Logger()

venv_dir = Path("remote-workflow")
requirements_file = Path("requirements.txt")

system_infos = {
    "system": platform.system(),
    "release": int(platform.release()),
    "system_version": platform.version(),
    "architecture": platform.machine(),
    "python_version": platform.python_version()
}

def create_venv():
    if not venv_dir.exists():
        logger.info("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
        logger.ok(f"Virtual environment created at: {venv_dir.resolve()}")
    else:
        logger.info(f"Virtual environment already exists at: {venv_dir.resolve()}")

    python_executable = (
        venv_dir / "Scripts" / "python.exe" if os.name == "nt"
        else venv_dir / "bin" / "python"
    )

    logger.info("Upgrading pip...")
    subprocess.check_call([str(python_executable), "-m", "pip", "install", "--upgrade", "pip"])
    logger.ok("pip upgraded.")

    if requirements_file.exists():
        logger.info("Installing packages from requirements.txt...")
        subprocess.check_call([str(python_executable), "-m", "pip", "install", "-r", str(requirements_file)])
        logger.ok("Packages installed.")
    else:
        logger.warn("requirements.txt not found.")

def remove_venv():
    if venv_dir.exists():
        logger.info(f"Removing virtual environment at: {venv_dir.resolve()}")
        shutil.rmtree(venv_dir)
        logger.ok("Virtual environment removed.")
    else:
        logger.info("No virtual environment to remove.")

def print_system_info():
    logger.info("System Info:")
    logger.info(f"System: {system_infos['system']}")
    logger.info(f"Release: {system_infos['release']}")
    logger.info(f"Version: {system_infos['system_version']}")
    logger.info(f"Architecture: {system_infos['architecture']}")
    logger.info(f"Python Version: {system_infos['python_version']}")

def read_tested_systems_simple(file_path="tested_systems.yml"):
    tested = {}
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    key, value = line.split(":", 1)
                    tested[key.strip()] = value.strip()
    except FileNotFoundError:
        logger.warn(f"{file_path} not found.")
        return {}

    return tested

def check_tested_systems():
    tested = read_tested_systems_simple()
    if not tested:
        return

    logger.info("Checking system compatibility...")

    for key, expected in tested.items():
        actual = system_infos.get(key.lower())
        if actual is None:
            logger.warn(f"{key} not found in current system info")
            continue

        if str(actual) != expected:
            logger.warn(f"{key} mismatch: expected '{expected}', got '{actual}'")
        else:
            logger.ok(f"{key} matches ({actual})")

if __name__ == "__main__":
    try:
        print_system_info()
        check_tested_systems()
    except Exception as e:
        logger.error(f"Failed to display system information:\n{e}")
    finally:
        try:
            while True:
                action = input("Create, delete or switch to environment (c/D): ")
                if action == "c":
                    create_venv()
                    break
                elif action == "D":
                    remove_venv()
                    break
                else:
                    logger.warn("Wrong action type...")
        except Exception as e:
            logger.error(f"Unknown error while handling virtual environment:\n{e}")