import typer
from typing_extensions import Annotated
import serial
#import serial.tools.list_ports
import json
import pathlib as path
import time
import platformdirs
import importlib.resources

from CovertHelp import ConfigManager

config_dir = path.Path(platformdirs.user_config_dir("CovertHelp"))
config_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
configPath = config_dir / "config.json"

if not configPath.exists():
    # Create an empty config file if it doesn't exist
    with importlib.resources.files("CovertHelp").joinpath("config.json").open("r") as src, \
        open(configPath, "w") as dst:
        dst.write(src.read())

def hostInformation():
    if configPath.exists():
        with open(configPath, "r") as file:
            config = json.load(file)
            deviceSettings = config.get("deviceSettings", {})
            return deviceSettings.get("deviceID"), deviceSettings.get("securityKey")


def Connect(
    Port: Annotated[
        str,
        typer.Option(
            "--port",
            "-p",
            help="Indicate the port you are trying to connect to.",
            show_default=True,
        )
    ],
    Side: Annotated[
        str,
        typer.Option(
            "--side",
            "-s",
            help="Inidicate the location of the panel you are connecting to. NOTE: THIS WILL ERASE ANY INFORMATION FROM CONFIG OF THIS PANEL. [Options: Left, Right, Top, Bottom, Back or All.]"
        )
    ]
):
    """
    Used to connect to specific module on a specified port.
    This function is used as initial module setup and pairing.
    """
    baudRate = 115200
    timeout = 1
    ser = serial.Serial(
        port=Port,
        baudrate=baudRate,
        timeout=timeout
    )
    print(f"Attempting connection to {Port} at {baudRate} baud...")
    try:
        max_attempts = 6
        delay_between_attempts = 5  # seconds
        for attempt in range(1, max_attempts + 1):
            print(f"Attempt {attempt} of {max_attempts}...")
            ser.write(f"Host Information: {hostInformation()}\n".encode('utf-8'))
            start_time = time.time()
            while time.time() - start_time < delay_between_attempts:
                response = ser.readline().decode('utf-8').strip()
                if response:
                    print("Received response:", response)
                    if response == "Host Info Received":
                        print("Pairing Complete")
                        print("Starting Client Information Request...")
                        clientRequest(ser, Side)
                        break
                time.sleep(0.1)
            else:
                print(f"No response received after {delay_between_attempts} seconds. Retrying...")
                continue
            break
        else:
            print("Failed to receive response after maximum attempts.")
            return None
        
        
    except serial.SerialException as e:
        print(f"Failed to connect to {Port}: {e}")
        return None
    
def clientRequest(ser, side):
    ser.write("Client Information Request\n".encode('utf-8'))
    start_time = time.time()
    while time.time() - start_time < 5:  # wait for 5 seconds
        response = ser.readline().decode('utf-8').strip()
        if response.startswith("Client Information:"):
            print("Received Client Information:", response)
            try:
                client_info = json.loads(response.split("Client Information: ")[1])
                print("Client Information JSON:", client_info)
                ConfigManager.load_config()  # Load existing configuration

                # Normalize side to lowercase for attribute names
                side_lower = side.lower()
                # Map panel keys to ConfigManager variable names
                panel_var_map = {
                    "panelID": f"{side_lower}PanelID",
                    "panelName": f"{side_lower}PanelName",
                    "panelType": f"{side_lower}PanelType",
                    "securityKey": f"{side_lower}PanelSecurityKey"
                }
                # Set variables dynamically
                for key, value in client_info.items():
                    var_name = panel_var_map.get(key)
                    if var_name and hasattr(ConfigManager, var_name):
                        setattr(ConfigManager, var_name, value)
                        print(f"Set {var_name} to {value}")

                ConfigManager.save_config()  # Save once after all variables are set

            except Exception as e:
                print(f"Failed to process client information: {e}")
            return

        time.sleep(0.1)
    print("No response received for Client Information Request.")
