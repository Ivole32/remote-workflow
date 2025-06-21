from logger import Logger
import subprocess
import typer
import os
from rich import print

logger = Logger()

app = typer.Typer()

@app.command()
def install() -> None:
    """Starts Installation"""
    print("[blue]Should be already installed...[/blue]")
    print("[blue]Reinstall (y/n):[/blue]")
    if input("") == "y":
        os.system(r"python .\install.py")

@app.command()
def uninstall() -> None:
    """Starts Installation"""
    print("[blue]Starting uninstallation[/blue]")

    full_path = os.getcwd()
    pid = os.getpid()
    subprocess.Popen([r".\uninstall.cmd", rf"{full_path}", f"{pid}"])

@app.command()
def open_UI():
    """Opens the UI"""
    print("[blue]Opening UI...[/blue]")
    os.system(r".\python.exe .\UI.py")

if __name__ == "__main__":
    app()