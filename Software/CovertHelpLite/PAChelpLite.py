import serial
import re
import json
import pathlib as path


# Use the first port from socat output
jsonpath = path.Path("config.json")

def Connect(serialPort):

    ser = serial.Serial(str(serialPort), 115200, timeout=100)
    pattern = re.compile(r"Host Information: \('(.+?)', '(.+?)'\)")

    line = ser.readline().decode("utf-8").strip()
    if line:
        print("Received:", line)
        if line.startswith("Host Information:"):
            print("Host Information received.")
            print("DEBUG: Raw Host Information line:", line)
        match = pattern.match(line)
        if match:
            device_id, security_key = match.groups()
            print(f"Device ID: {device_id}, Security Key: {security_key}")

            # Load existing config if it exists
            if jsonpath.exists():
                with open(jsonpath, "r") as f:
                    config = json.load(f)
            else:
                config = {}

            # Update only the hostInfo section
            config["hostInfo"] = {
                "deviceID": device_id,
                "securityKey": security_key
            }

            # Write the updated config back
            with open(jsonpath, "w") as f:
                json.dump(config, f, indent=4)

            print(f"Host information saved to {jsonpath}")
            ser.write(f"Host Info Received\n".encode('utf-8'))
            
        else:
            print("Could not parse Host Information line.")
    if line.startswith("Client Information Request"):
        print("Client Information Request received.")
        if jsonpath.exists():

            jsonInfo = json.loads(jsonpath.read_text())
            client_info = jsonInfo.get("clientInfo", {})
            print("Client Information:", client_info)
            ser.write(f"Client Information: {json.dumps(client_info)}\n".encode('utf-8'))
        else:
            print("No client information available.")
            ser.write(f"No client information available\n".encode('utf-8'))
    if line.startswith("Request Extra"):
        print("Request Extra received.")
        ### ADD ANY COMMANDS THE HOST MACHINE NEEDS TO RUN HERE, THIS CAN BE USED TO INSTALL DEPENDENCIES OR RUN SCRIPTS
        extraList = [
            "python3 --version"
        ]
        ser.write(f"Extra: {json.dumps(extraList)}\n".encode('utf-8'))
while True:
    Connect("/dev/pts/4")