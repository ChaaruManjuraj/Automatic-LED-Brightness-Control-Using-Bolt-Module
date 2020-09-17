from boltiot import Bolt
import json, time
import config

# Configure Bolt device
autoLED = Bolt(config.API_KEY, config.DEVICE_ID)
# Global variable
sensor_value = 0

def checkIntensity():
    while True:
        # Read current room light intensity
        intensity = autoLED.analogRead("A0")
        intensityData = json.loads(intensity)

        # If failed to retrieve current intensity
        if intensityData['success'] != 1:
            raise Exception("Error while retrieving the data")
            print("Error: ", intensityData['value'])
            time.sleep(10)
            continue

        try:
            global sensor_value
            # Assign current intensity to global variable sensor_value
            sensor_value = int(intensityData['value'])
            print("Data retrieval successful...")
            print("Current light intensity = " , sensor_value)
            controlLED()
            time.sleep(10)
            continue
        except Exception as e:
            print("There was an error parsing the response\nError: " , e)
            time.sleep(10)
            continue

def controlLED():

    curIntensity = sensor_value

    # If light is sufficient 
    if(curIntensity > 1000):
        LED = autoLED.analogWrite("1", "0")
        print("Current LED brightness: 0%")

    # If too dark
    elif(curIntensity < 350):
        LED = autoLED.analogWrite("1", "255")
        print("Current LED brightness: 100%")
    
    else:
        # 1 unit is 1/1024 part of 255
        unit = 255/1024
        # Subtract curIntensity from highest value
        value = 1024 - curIntensity
        # value = value * unit
        value *= unit
        res = int(value)
        LED = autoLED.analogWrite("1", str(res)) 
        brightness = (res/255) * 100
        limitedBrightness = round(brightness, 1)
        print("Current LED brightness: " , limitedBrightness , "%")

def isON():
    # Check whether bolt device is up
    isOn = autoLED.isOnline()
    isOnData = json.loads(isOn)

    return True if isOnData['success'] == 1 else False

if(isON()):
    checkIntensity()
else:
    raise Exception("Please turn on Bolt device");    
