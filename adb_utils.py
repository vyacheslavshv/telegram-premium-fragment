import os
import subprocess
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO


class AdbAutomation:
    """
    A class to abstract the interactions with an Android device using ADB.
    """

    def __init__(self):
        """
        Load the .env file and get the DEVICE_ID.
        """
        load_dotenv()
        self.device_id = os.getenv("DEVICE_ID")

        if self.device_id is None:
            raise ValueError("DEVICE_ID not found in .env file")

    def run(self, command):
        """
        Executes an ADB command on the specified device.
        """
        try:
            subprocess.run(f"adb -s {self.device_id} shell {command}",
                           capture_output=True, text=True, shell=True)
        except Exception as e:
            print(f"Error running command: {command}, error message: {e}")

    def tap(self, x, y):
        """
        Simulates a tap on the device screen at coordinates (x, y).
        """
        try:
            self.run(f"input tap {x} {y}")
        except Exception as e:
            print(f"Error taping {x} {y}, error message: {e}")

    def input_text(self, text):
        """
        Inputs the specified text into the active field on the device.
        """
        try:
            self.run(f"input text {text}")
        except Exception as e:
            print(f"Error while inputting text: {e}")

    def press_keyevent(self, keyevent_code):
        """
        Simulates the pressing of a key event.
        """
        try:
            self.run(f"input keyevent {keyevent_code}")
        except Exception as e:
            print(f"Error while pressing keyevent {keyevent_code}, error message: {e}")

    def start_app(self, package_name, activity_name=None):
        """
        Starts an app using its package name and activity name.
        """
        try:
            if activity_name:
                self.run(f"am start -n {package_name}/{activity_name}")
            else:
                self.run(f"am start -a android.intent.action.MAIN -n {package_name}")
        except Exception as e:
            print(f"Error while starting an app, error message: {e}")

    def take_screenshot(self):
        """
        Captures a screenshot from the specified Android device and returns it as a PIL image.
        """
        try:
            result = subprocess.run(f"adb -s {self.device_id} exec-out screencap -p",
                                    capture_output=True, shell=True)
            image_data = BytesIO(result.stdout)
            image = Image.open(image_data)

            return image
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
