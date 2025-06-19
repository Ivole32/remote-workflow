from logger import Logger
import os

logger = Logger()

def delete_venv() -> None:
    logger.info("Removing envoirnement...")
    os.system(r".\remote-workflow\Scripts\deactivate.bat")
    os.system("rmdir /s /q remote-workflow")
    logger.ok("Envioprnement removed")

delete_venv()