import sys

class Colors:
    RESET = "\033[0m"
    INFO = "\033[94m"
    WARN = "\033[93m"
    OK = "\033[92m"
    ERROR = "\033[91m"

class Logger:
    def __init__(self, stream=sys.stdout):
        self.stream = stream

    def info(self, message: str):
        self._print_colored("[INFO]", message, Colors.INFO)

    def warn(self, message: str):
        self._print_colored("[WARN]", message, Colors.WARN)

    def ok(self, message: str):
        self._print_colored("[OK]", message, Colors.OK)

    def error(self, message: str):
        self._print_colored("[ERROR]", message, Colors.ERROR)

    def _print_colored(self, prefix: str, message: str, color: str):
        self.stream.write(f"{color}{prefix}{Colors.RESET} {message}\n")
        self.stream.flush()