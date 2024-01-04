import subprocess
from PIL import Image
from time import sleep


class AdbAutomation:
    """
    A class to abstract the interactions with an Android device using ADB.
    """

    def __init__(self, device_id):
        """
        Get the DEVICE_ID.
        """
        self.device_id = device_id

    def run(self, command, text=True):
        """
        Executes an ADB command on the specified device.
        """
        try:
            result = subprocess.run(
                f"adb -s {self.device_id} shell {command}",
                capture_output=True, text=text, shell=True)
            return result
        except Exception as e:
            print(f"Error running command: {command}, message: {e}")

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
        if activity_name:
            self.run(f"am start -n {package_name}/{activity_name}")
        else:
            self.run(f"am start -a android.intent.action.MAIN -n {package_name}")

    def take_screenshot(self):
        """
        Captures a screenshot from the specified Android device, saves it on the device,
        then pulls the image to the local system and opens it as a PIL image.
        """
        screenshot_name = f"screenshot_{self.device_id}.png"
        local_screenshot_path = f"{screenshot_name}"

        while True:
            try:
                # Save the screenshot to the device's storage
                subprocess.run(
                    f"adb -s {self.device_id} shell screencap -p /sdcard/{screenshot_name}",
                    shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )

                # Pull the image to the local machine
                subprocess.run(
                    f"adb -s {self.device_id} pull /sdcard/{screenshot_name} {local_screenshot_path}",
                    shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )

                # Open the image from the local file
                image = Image.open(local_screenshot_path)
                return image

            except subprocess.CalledProcessError as e:
                print(f"ADB command failed: {e}")
                sleep(1)
            except Exception as e:
                print(f"Error processing screenshot file: {e}")
                sleep(1)
