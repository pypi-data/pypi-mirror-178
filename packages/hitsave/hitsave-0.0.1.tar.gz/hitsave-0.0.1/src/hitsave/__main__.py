
import typer

app = typer.Typer()

@app.callback()
def thanks():
    print("Thanks for downloading hitsave. We are working hard to release the library and CLI tool. Watch this space!")

if __name__ == "__main__":
    app()