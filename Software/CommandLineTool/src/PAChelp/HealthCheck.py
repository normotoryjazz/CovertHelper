import typer
from typing_extensions import Annotated

def HealthCheck(
    side: Annotated[
        str,
        typer.Option(
            "--side",
            "-s",
            help="Indicate the panel you are trying to check health of. [Options: Left, Right, Top, Bottom, Back or All.]",
            show_default=True,
        )
    ] = "All"
):
    """
    Check the status of incoming and outgoing traffic to the panels. Panels must be running the most up to date version of PAChelpAssist to work properly.
    Alias: hc
    """
    valid_options = ["all", "left", "right", "top", "bottom", "back"]
    sidelower = side.lower()

    if sidelower in valid_options:
        if sidelower == "all":
            typer.echo("Checking health of all panels...")
        else:
            typer.echo(f"Checking health of the {sidelower.capitalize()} panel...")
    else:
        typer.echo(
            typer.style(
                "Invalid option. Please choose from: Left, Right, Top, Bottom, Back, or All.",
                fg=typer.colors.RED
            ),
            err=True
        )
        raise typer.Exit(code=1)

def PanelCheck(panel):
    # Placeholder for the PanelCheck function
    print("WIP")