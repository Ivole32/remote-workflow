import platform
import os
from logger import Logger

logger = Logger()

system_infos = {
    "system": platform.system(),
    "release": int(platform.release()),
    "system_version": platform.version(),
    "architecture": platform.machine(),
    "python_version": platform.python_version()
}

def print_system_info() -> None:
    """
    Prints the current system infos
    """
    logger.info("System Info:")
    logger.info(f"System: {system_infos['system']}")
    logger.info(f"Release: {system_infos['release']}")
    logger.info(f"Version: {system_infos['system_version']}")
    logger.info(f"Architecture: {system_infos['architecture']}")
    logger.info(f"Python Version: {system_infos['python_version']}")

def read_tested_systems_simple(file_path="tested_systems.yml") -> dict:
    """
    Returns the tested system specifications

    Arguments:
        Optional:
            file_path (str): The path to the tested_systems.yml file.
    Returns:
        dict: The tested system specifications 
    """
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

def check_tested_systems() -> None:
    """
    Checks the system for compatibility and prints out a warning if it's not compatible
    """
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

def create_venv() -> None:
    logger.info("Creating virtual envoirnement")
    os.system("python -m venv remote-workflow")
    os.system(r".\remote-workflow\Scripts\activate")
    logger.ok("Virtual envoirnement created")
    logger.info("Installing requirements")
    os.system(r".\remote-workflow\Scripts\python.exe -m pip install --upgrade pip")
    os.system(r".\remote-workflow\Scripts\pip.exe install -r requirements.txt")
    logger.ok("Requirements installed")

if __name__ == "__main__":
    try:
        print_system_info()
        check_tested_systems()
        create_venv()
    except Exception as e:
        logger.error(f"Failed to display system information:\n{e}")

# cmd /c mklink /J MeinJunction ZielOrdner