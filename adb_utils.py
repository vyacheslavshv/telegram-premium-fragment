from ppadb.client import Client as AdbClient


class AdbAutomation:
    """
    A class to abstract the interactions with an Android device using ADB.
    """

    def __init__(self, host="127.0.0.1", port=5037):
        client = AdbClient(host=host, port=port)
        devices = client.devices()

        if not devices:
            raise Exception("No devices found")

        self.device = devices[0]

    def tap(self, x, y):
        """
        Simulates a tap on the device screen at coordinates (x, y).
        """
        self.device.shell(f"input tap {x} {y}")

    def input_text(self, text):
        """
        Inputs the specified text into the active field on the device.
        """
        self.device.shell(f"input text {text}")

    def press_keyevent(self, keyevent_code):
        """
        Simulates the pressing of a key event.
        """
        self.device.shell(f"input keyevent {keyevent_code}")

    def start_app(self, package_name, activity_name=None):
        """
        Starts an app using its package name and activity name.
        """
        if activity_name:
            self.device.shell(f"am start -n {package_name}/{activity_name}")
        else:
            self.device.shell(f"am start -a android.intent.action.MAIN -n {package_name}")

