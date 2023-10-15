import pytesseract
from time import sleep
from PIL import Image
from io import BytesIO
from fuzzywuzzy import fuzz

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 2220


def take_screenshot(device):
    image_data = device.screencap()
    return Image.open(BytesIO(image_data))


def get_screen_text(image):
    return pytesseract.image_to_string(image)


def is_desired_screen(image, expected_text, similarity_threshold=90):
    screen_text = get_screen_text(image)
    similarity = fuzz.partial_ratio(screen_text, expected_text)
    return similarity >= similarity_threshold


def wait_for_correct_screen(automation, expected_text):
    message_displayed = False
    while True:
        # Take a screenshot
        screenshot = take_screenshot(automation.device)

        # Check if it's the desired screen
        if is_desired_screen(screenshot, expected_text):
            if message_displayed:
                print("\033[92mSuccessfully found the desired screen: '{}'\033[0m".format(expected_text))
            break

        if not message_displayed:
            print(f"We are not on the '{expected_text}' screen, trying again...")
            message_displayed = True

        sleep(2)


def gift_premium(automation, username):
    """
    Gifts a premium subscription to a specified Telegram username.
    """

    # Ensure we're on the right screen before proceeding
    wait_for_correct_screen(automation, "Buy Telegram Premium")

    # Tap on the cancel cross
    automation.tap(SCREEN_WIDTH * 0.95, SCREEN_HEIGHT * 0.4)
    sleep(1)

    # Tap on the cancel cross again
    automation.tap(SCREEN_WIDTH * 0.95, SCREEN_HEIGHT * 0.4)
    sleep(1)

    # Tap to enter username
    automation.tap(SCREEN_WIDTH * 0.95, SCREEN_HEIGHT * 0.4)
    sleep(1)

    # Insert username
    automation.input_text(username)
    sleep(1)

    # Confirm username
    automation.press_keyevent(66)
    sleep(1)

    # Tap on "3 month"
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.7)
    sleep(1)

    # Tap on "Gift Telegram Premium"
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.76)
    sleep(2)

    wait_for_correct_screen(automation, "Gift Telegram Premium")

    # Tap on "Buy Gift for {username}"
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.9)
    sleep(2)

    wait_for_correct_screen(automation, "Scan the QR code")

    # Tap on "Buy Premium with Tonkeeper"
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.85)
    sleep(3)

    wait_for_correct_screen(automation, "Telegram Premium for 3 months")

    # Tap on "Confirm"
    automation.tap(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.9)
    sleep(3)

    # Tap on "Passcode"
    automation.tap(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.65)
    sleep(1)
    automation.tap(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.65)
    sleep(1)
    automation.tap(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.65)
    sleep(1)
    automation.tap(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.65)
    sleep(7)

    # Open "Tonkeeper" again
    automation.start_app("com.ton_keeper", ".TonkeeperActivity")
    sleep(5)

    wait_for_correct_screen(automation, "Gift Sent!")

    # Tap on "Send another gift"
    automation.tap(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.7)
    sleep(2)

    # Tap for return
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.25)
    sleep(1)
