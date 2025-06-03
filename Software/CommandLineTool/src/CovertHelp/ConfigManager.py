import json
from pathlib import Path
import platformdirs

config_dir = Path(platformdirs.user_config_dir("CovertHelp"))
config_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
configPath = config_dir / "config.json"

#devie info
deviceType = ""
version = ""
author = ""
#device settings
deviceID = ""
deviceName = ""
securityKey = ""
# panel settings
leftPanelID = ""
leftPanelName = ""
leftPanelType = ""
leftPanelSecurityKey = ""

rightPanelID = ""
rightPanelName = ""
rightPanelType = ""
rightPanelSecurityKey = ""

topPanelID = ""
topPanelName = ""
topPanelType = ""
topPanelSecurityKey = ""

bottomPanelID = ""
bottomPanelName = ""
bottomPanelType = ""
bottomPanelSecurityKey = ""

backPanelID = ""
backPanelName = ""
backPanelType = ""
backPanelSecurityKey = ""

def load_config():
    global deviceType, version, author
    global deviceID, deviceName, securityKey
    global leftPanelID, leftPanelName, leftPanelType
    global rightPanelID, rightPanelName, rightPanelType
    global topPanelID, topPanelName, topPanelType
    global bottomPanelID, bottomPanelName, bottomPanelType
    global backPanelID, backPanelName, backPanelType
    global leftPanelSecurityKey, rightPanelSecurityKey
    global topPanelSecurityKey, bottomPanelSecurityKey, backPanelSecurityKey

    if configPath.exists():
        with open(configPath, "r") as file:
            config = json.load(file)
            deviceInfo = config.get("deviceInfo", {})
            deviceType = deviceInfo.get("deviceType", "")
            version = deviceInfo.get("version", "")
            author = deviceInfo.get("author", "")
            deviceSettings = config.get("deviceSettings", {})
            deviceID = deviceSettings.get("deviceID", "")
            deviceName = deviceSettings.get("deviceName", "")
            securityKey = deviceSettings.get("securityKey", "")
            panels = config.get("panels", {})
            leftPanelID = panels.get("left", {}).get("panelID", "")
            leftPanelName = panels.get("left", {}).get("panelName", "")
            leftPanelType = panels.get("left", {}).get("panelType", "")
            leftPanelSecurityKey = panels.get("left", {}).get("securityKey", "")
            rightPanelID = panels.get("right", {}).get("panelID", "")
            rightPanelName = panels.get("right", {}).get("panelName", "")
            rightPanelType = panels.get("right", {}).get("panelType", "")
            rightPanelSecurityKey = panels.get("right", {}).get("securityKey", "")
            topPanelID = panels.get("top", {}).get("panelID", "")
            topPanelName = panels.get("top", {}).get("panelName", "")
            topPanelType = panels.get("top", {}).get("panelType", "")
            topPanelSecurityKey = panels.get("top", {}).get("securityKey", "")
            bottomPanelID = panels.get("bottom", {}).get("panelID", "")
            bottomPanelName = panels.get("bottom", {}).get("panelName", "")
            bottomPanelType = panels.get("bottom", {}).get("panelType", "")
            bottomPanelSecurityKey = panels.get("bottom", {}).get("securityKey", "")
            backPanelID = panels.get("back", {}).get("panelID", "")
            backPanelName = panels.get("back", {}).get("panelName", "")
            backPanelType = panels.get("back", {}).get("panelType", "")
            backPanelSecurityKey = panels.get("back", {}).get("securityKey", "")
            print("Configuration loaded successfully.")
    else:
        print("Failed to load configuration: config.json either does not exist or something went wrong.")

def save_config():
    config = {
        "deviceInfo": {
            "deviceType": deviceType,
            "version": version,
            "author": author
        },
        "deviceSettings": {
            "deviceID": deviceID,
            "deviceName": deviceName,
            "securityKey": securityKey
        },
        "panels": {
            "left": {
                "panelID": leftPanelID,
                "panelName": leftPanelName,
                "panelType": leftPanelType,
                "securityKey": leftPanelSecurityKey
            },
            "right": {
                "panelID": rightPanelID,
                "panelName": rightPanelName,
                "panelType": rightPanelType,
                "securityKey": rightPanelSecurityKey
            },
            "top": {
                "panelID": topPanelID,
                "panelName": topPanelName,
                "panelType": topPanelType,
                "securityKey": topPanelSecurityKey
            },
            "bottom": {
                "panelID": bottomPanelID,
                "panelName": bottomPanelName,
                "panelType": bottomPanelType,
                "securityKey": bottomPanelSecurityKey
            },
            "back": {
                "panelID": backPanelID,
                "panelName": backPanelName,
                "panelType": backPanelType,
                "securityKey": backPanelSecurityKey
                
            }
        }
    }
    with open(configPath, "w") as file:
        json.dump(config, file, indent=4)