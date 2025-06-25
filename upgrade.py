from logger import Logger
import subprocess
import os


logger = Logger()

def update_repo() -> None:
    """
    Pulls the newest version of the project
    """
    logger.info("Upgrading repo")
    os.system("git pull")
    logger.ok("Repo upgraded")

def create_venv() -> None:
    """
    Creates the virtual enviornement and installs requirements
    """
    logger.info("Creating virtual enviornement")
    result = subprocess.run(["python", "-m", "venv", "remote-workflow"], capture_output=True, text=True)

    logger.ok("Virtual envoirnement created")

    logger.info("Installing requirements")
    os.system(r".\remote-workflow\Scripts\python.exe -m pip install --upgrade pip")
    os.system(r".\remote-workflow\Scripts\python.exe -m pip install -r requirements.txt")
    logger.ok("Requirements installed")

def upgrade_venv() -> None:
    """
    Reinstalls the requirements.txt in the venv to be up to date with the requirements
    """
    logger.info("Deleting venv")
    system_command = r"rmdir /s /q .\remote-workflow"
    os.system(system_command)
    logger.ok("Venv deleted")

    logger.info("Recreating venv")
    create_venv()
    logger.ok("Venv recreated")

if __name__ == "__main__":
    update_repo()
    upgrade_venv()