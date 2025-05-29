#import typer
#from typing_extensions import Annotated
import serial
#import serial.tools.list_ports
import json
import pathlib as path
import time

currentDir = path.Path(__file__).parent
configPath = currentDir / "config.json"

def hostInformation():
    if configPath.exists():
        with open(configPath, "r") as file:
            config = json.load(file)
            deviceSettings = config.get("deviceSettings", {})
            return deviceSettings.get("deviceID"), deviceSettings.get("securityKey")


def Connect(Port):
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
                        clientRequest()
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
    
def clientRequest():
    print("WIP")
    
Connect("/dev/pts/2")