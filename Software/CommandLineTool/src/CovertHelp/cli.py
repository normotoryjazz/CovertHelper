import typer
from .HealthCheck import HealthCheck
from .Connect import Connect


app = typer.Typer()

app.command(name= "HealthCheck")(HealthCheck)
app.command(name="connect")(Connect)
app.command(name="hc", hidden=True)(HealthCheck)


if __name__ == "__main__":
    app()