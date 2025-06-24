from logger import Logger
from config import Configuration
import os

logger = Logger()
config = Configuration()

def update_repo() -> None:
    """
    Pulls the newest version of the project
    """
    os.system("git pull")

def create_venv() -> None:
    """
    Creates the virtual enviornement and installs requirements
    """
    logger.info("Creating virtual enviornement")
    os.system(r".\python_no_venv.exe -m venv remote-workflow")
    logger.ok("Virtual envoirnement created")

    logger.info("Installing requirements")
    os.system(r".\remote-workflow\Scripts\python.exe -m pip install --upgrade pip")
    os.system(r".\remote-workflow\Scripts\pip.exe install -r requirements.txt")
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
    logger.ok("Venv recteated")

if __name__ == "__main__":
    update_repo()
    upgrade_venv()