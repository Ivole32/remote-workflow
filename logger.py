"""
The main file for the custom logger
"""
import sys
from config import config_path

class Colors:
    """
    The main class for all color codes
    """
    RESET = "\033[0m"
    INFO = "\033[94m"
    WARN = "\033[93m"
    OK = "\033[92m"
    ERROR = "\033[91m"

class Logger:
    """
    The main class for the custom logger
    """
    def __init__(self, stream=sys.stdout) -> None:
        self.__stream = stream
        self.debug_mode = self.__get_debug_mode()

    def __get_debug_mode(self) -> bool:
        """
        Returns the debug mode of the program

        Returns:
            bool: The current debug mode
        """
        try:
            with open(config_path, "r") as config:
                content = config.read()
                if "debug-mode = False" in content:
                    return False
                return True
        except Exception:
            return True
        
    def info(self, message: str) -> None:
        """
        Logger info
        """
        if self.debug_mode:
            self._print_colored("[INFO]", message, Colors.INFO)

    def warn(self, message: str) -> None:
        """
        Logger warning
        """
        self._print_colored("[WARN]", message, Colors.WARN)

    def ok(self, message: str) -> None:
        """
        Logger ok
        """
        if self.debug_mode:
            self._print_colored("[OK]", message, Colors.OK)

    def error(self, message: str) -> None:
        """
        Logger error
        """
        self._print_colored("[ERROR]", message, Colors.ERROR)

    def _print_colored(self, prefix: str, message: str, color: str) -> None:
        """
        Writes a formatted and colored message to the output stream.

        Arguments:
            prefix: str (A prefix string (e.g., a log level like "[INFO]"))
            message: str (The main message to be printed)
            color: str (An ANSI color code applied to the prefix)
        """
        self.__stream.write(f"{color}{prefix}{Colors.RESET} {message}\n")
        self.__stream.flush()