import typer

from kclii.database.database import Base, engine
from kclii.modules.profiles import profiles


import kclii.modules.profiles.models

app = typer.Typer(pretty_exceptions_enable=False)
app.add_typer(profiles.app, name="profile")


@app.command()
def hello(name: str = ""):
    print(f"Welcome sr! {name}")


@app.command()
def version() -> None:
    print("0.1.12")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app()
