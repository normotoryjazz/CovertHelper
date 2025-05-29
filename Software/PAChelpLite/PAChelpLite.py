import serial
import re
import json
import pathlib as path


# Use the first port from socat output
ser = serial.Serial("/dev/pts/3", 115200, timeout=100)
pattern = re.compile(r"Host Information: \('(.+?)', '(.+?)'\)")
jsonpath = path.Path("config.json")

while True:
    line = ser.readline().decode("utf-8").strip()
    if line:
        print("Received:", line)
    if line.startswith("Host Information:"):
        print("Host Information received.")
        match = pattern.match(line)
        if match:
            device_id, security_key = match.groups()
            print(f"Device ID: {device_id}, Security Key: {security_key}")
            hostInfo = {
                "hostInfo": {
                    "deviceID": device_id,
                    "securityKey": security_key
                }
            }
            jsonpath.write_text(json.dumps(hostInfo, indent=4))
            print(f"Host information saved to {jsonpath}")
            ser.write(f"Host Info Received\n".encode('utf-8'))
            continue
    if line.startswith("Client Information Request"):
        print("Client Information Request received.")
        if jsonpath.exists():
            client_info = json.loads(jsonpath.read_text())
            print("Client Information:", client_info)
            ser.write(f"Client Information: {client_info}\n".encode('utf-8'))
            continue
        else:
            print("No client information available.")
            ser.write(f"No client information available\n".encode('utf-8'))
            continue        