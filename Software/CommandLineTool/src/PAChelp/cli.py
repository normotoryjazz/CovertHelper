import typer
from .HealthCheck import HealthCheck


app = typer.Typer()

app.command()(HealthCheck)
app.command(name="hc", hidden=True)(HealthCheck)


if __name__ == "__main__":
    app()