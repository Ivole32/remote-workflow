from logger import Logger
import os

logger = Logger()

def delete_dir(dir:str) -> None:
    """
    A function to delete a directory

    Arguments:
        dir: str (The path to the directory to remove)
    """
    logger.info(f"Deleting {dir}")
    os.system(rf"rmdir /s /q {dir}")
    logger.ok(f"{dir} deleted")

def delete_file(file:str) -> None:
    """
    A function to delete a file

    Arguments:
        file: str (The path to the file to remove)
    """
    logger.info(f"Deletion {file}")
    os.system(rf"del /f /q {file}")
    logger.ok(f"{file} deleted")

def delete_venv() -> None:
    """
    A function to delete the program's enviornement
    """
    logger.info("Removing envoirnement...")
    os.system(r".\remote-workflow\Scripts\deactivate.bat")
    delete_dir(r".\remote-workflow")
    logger.ok("Envoirnement removed")

    logger.info("Deleting other files...")
    os.system(r"del /f /q .\python")
    os.system(r"del /f /q .\python.cmd")
    logger.ok("Other files were deleted")
    
    exit(0)

delete_venv()