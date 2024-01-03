import os
from dotenv import load_dotenv
from ppadb.client import Client as AdbClient


class AdbAutomation:
    """
    A class to abstract the interactions with an Android device using ADB.
    """

    def __init__(self, host="localhost", port=5038):
        # Load the .env file and get the DEVICE_ID
        load_dotenv()
        device_id = os.getenv("DEVICE_ID")

        if device_id is None:
            raise ValueError("DEVICE_ID not found in .env file")

        client = AdbClient(host=host, port=port)
        device = client.device(device_id)

        if device is None:
            raise Exception(f"No device found with ID {device_id}")

        self.device = device

    def tap(self, x, y):
        """
        Simulates a tap on the device screen at coordinates (x, y).
        """
        try:
            self.device.shell(f"input tap {x} {y}")
        except Exception as e:
            print(f"Error taping {x} {y}, error was: {e}")

    def input_text(self, text):
        """
        Inputs the specified text into the active field on the device.
        """
        try:
            self.device.shell(f"input text {text}")
        except Exception as e:
            print(f"Error while inputting text: {e}")

    def press_keyevent(self, keyevent_code):
        """
        Simulates the pressing of a key event.
        """
        try:
            self.device.shell(f"input keyevent {keyevent_code}")
        except Exception as e:
            print(f"Error while pressing keyevent {keyevent_code}, error was: {e}")

    def start_app(self, package_name, activity_name=None):
        """
        Starts an app using its package name and activity name.
        """
        try:
            if activity_name:
                self.device.shell(f"am start -n {package_name}/{activity_name}")
            else:
                self.device.shell(f"am start -a android.intent.action.MAIN -n {package_name}")
        except Exception as e:
            print(f"Error while starting an app, error was: {e}")
