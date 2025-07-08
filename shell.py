from logger import Logger
from config import Configuration
import subprocess
import typer
import os
from rich import print

logger = Logger()
config = Configuration()

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
def upgrade() -> None:
    """Upgrades the program"""
    print("[blue]Starting upgrade[/blue]")
    subprocess.run([r".\python_no_venv.exe", r".\upgrade.py"])

@app.command()
def set_up_ssh() -> None:
    """A command to set up SSH linking"""
    options = {"ssh-user": [], "ssh-ip": [], "ssh-port": ["22"], "ssh-file": [r".\.ssh"], "ssh-key-name": ["id_rsa"]}
    for option in options.keys():
        if options[option] != []:
            print(f"[blue]{option}[/blue] (default: {options[option][0]}): ", end="")
            value = input("")
            if value == "":
                value = options[option][0]
        else:
            print(f"[blue]{option}[/blue]: ", end="")
            value = input("")

        config.write_to_config(option, value, "SSH")

@app.command()
def set_up_workflow() -> None:
    """A command to set up the workflow"""
    pass

@app.command()
def open_UI() -> None:
    """Opens the UI"""
    print("[blue]Opening UI...[/blue]")
    os.system(r".\python.exe .\UI.py")

if __name__ == "__main__":
    app()