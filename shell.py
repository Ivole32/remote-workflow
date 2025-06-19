from logger import Logger
import typer
from rich import print

logger = Logger()

app = typer.Typer()

@app.command()
def install() -> None:
    """Starts Installation"""
    print("[blue]Started Installation[/blue]")

@app.command()
def uninstall() -> None:
    """Starts uninstallation"""
    print("[blue]Started uninstallation[/blue]")

'''
Examples:
    @app.command()
    def greet(name: str, loud: bool = False):
        """Gibt einen freundlichen Gruß aus."""
        msg = f"Hallo, {name}!"
        if loud:
            msg = msg.upper()
        print(f"[green]{msg}[/green]")

    @app.command()
    def version():
        """Zeigt die Version des Tools."""
        print("[blue]Tool v1.0.0[/blue]")
'''

if __name__ == "__main__":
    app()