import typer
from .HealthCheck import HealthCheck
from .Connect import Connect


app = typer.Typer()

app.command()(HealthCheck)
app.command()(Connect)
app.command(name="hc", hidden=True)(HealthCheck)


if __name__ == "__main__":
    app()