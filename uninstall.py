from logger import Logger
import os

logger = Logger()

def delete_dir(dir:str) -> None:
    logger.info(f"Deleting {dir}")
    os.system(rf"rmdir /s /q {dir}")
    logger.ok(f"{dir} deleted")

def delete_file(file:str) -> None:
    logger.info(f"Deletion {file}")
    os.system(rf"del /f /q {file}")
    logger.ok(f"{file} deleted")

def delete_venv() -> None:
    logger.info("Removing envoirnement...")
    os.system(r".\remote-workflow\Scripts\deactivate.bat")
    delete_dir(r".\remote-workflow")
    logger.ok("Envoirnement removed")

    logger.info("Deleting other files...")
    delete_file(r".\python")
    delete_file(r".\python.cmd")
    logger.ok("Other files were deleted")
    
    exit(0)

delete_venv()