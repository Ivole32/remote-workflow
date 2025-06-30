import platform
import sys
import os
import subprocess
from logger import Logger
from pathlib import Path

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

def create_symlink(target, link_name, is_dir=False):
    """
    Creates a symlink

    Arguments:
        target: str (the symlink target)
        link_name: str (the symlink name)
        is_dir: bool (Shows if the target is a dir)
    """
    link_path = Path(link_name)

    if link_path.exists() or link_path.is_symlink():
        if link_path.is_dir() and not link_path.is_symlink():
            os.rmdir(link_path)
        else:
            link_path.unlink()

    os.symlink(target, link_name, target_is_directory=is_dir)
    logger.ok(f"Symlink created: {link_name} -> {target}")

def create_venv() -> None:
    """
    Creates the virtual enviornement and installs requirements
    """
    logger.info("Creating virtual envoirnement")
    subprocess.run(["python", "-m", "venv", "remote-workflow"], check=True)
    subprocess.run([r".\remote-workflow\Scripts\activate"], shell=True, check=True)
    logger.ok("Virtual envoirnement created")

    logger.info("Installing requirements")
    subprocess.run([r".\remote-workflow\Scripts\python.exe", "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([r".\remote-workflow\Scripts\pip.exe", "install", "-r", "requirements.txt"], check=True)
    logger.ok("Requirements installed")

def create_symlinks() -> None:
    """
    Creates all required symlinks
    """
    logger.info("Creating symlinks...")
    create_symlink(r".\python.cmd", r".\python", is_dir=False)
    create_symlink(f"{sys.executable}", r".\python_no_venv.exe", is_dir=False)
    logger.ok("Symlinks created")

def print_version() -> None:
    with open(r".\version.txt", "r") as version_file:
        version = version_file.read()

    logger.info(f"Installing remote workflow, version: {version}")

if __name__ == "__main__":
    try:
        print_version()
        print_system_info()
        check_tested_systems()
        create_venv()
        create_symlinks()
    except Exception as e:
        logger.error(f"Error:\n{e}")