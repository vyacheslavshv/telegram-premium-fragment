import pytesseract
from time import sleep
from PIL import Image
from io import BytesIO
from fuzzywuzzy import fuzz

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 2220


def gift_premium(automation, username):
    """
    Gifts a premium subscription to a specified Telegram username.
    """

    # Ensure we're on the right screen before proceeding
    while not wait_for_correct_screen(automation, "Buy Telegram Premium"):
        handle_failure(automation)

    # Tap on the cancel cross
    for _ in range(2):
        automation.tap(SCREEN_WIDTH * 0.95, SCREEN_HEIGHT * 0.4)
        sleep(0.5)

    # Tap to enter username
    automation.tap(SCREEN_WIDTH * 0.95, SCREEN_HEIGHT * 0.4)
    sleep(0.7)

    # Insert username
    automation.input_text(username)
    sleep(0.7)

    # Confirm username
    automation.press_keyevent(66)
    sleep(0.7)

    # Take a screenshot to check for specific messages
    screenshot = take_screenshot(automation.device)

    if is_desired_screen(screenshot, "No Telegram users found."):
        print(f"Skipping: No Telegram users found for username {username}")
        return

    if is_desired_screen(screenshot, "This account is already subscribed to Telegram Premium."):
        print(f"Skipping: The account {username} is already subscribed to Telegram Premium.")
        return

    # Tap on "6 month"
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.6)
    sleep(0.7)

    # Tap on "Gift Telegram Premium"
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.76)
    sleep(3)

    if not wait_for_correct_screen(automation, "Gift Telegram Premium"):
        handle_failure(automation)
        return

    # Tap on "Buy Gift for {username}"
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.9)
    sleep(2)

    if not wait_for_correct_screen(automation, "Scan the QR code"):
        handle_failure(automation)
        return

    # Tap on "Buy Premium with Tonkeeper"
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.85)
    sleep(2)

    if not wait_for_correct_screen(automation, "Confirm action"):
        handle_failure(automation)
        return

    # Tap on "Confirm"
    automation.tap(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.9)
    sleep(2)

    if not wait_for_correct_screen(automation, "Enter passcode"):
        handle_failure(automation)
        return

    # Tap on "Passcode"
    for _ in range(4):
        automation.tap(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.65)
        sleep(0.5)
    sleep(10)

    # Open "Tonkeeper" again
    automation.start_app("com.ton_keeper", ".TonkeeperActivity")
    sleep(2)

    if not wait_for_correct_screen(automation, "Gift Sent!", msg=False):
        handle_failure(automation)
        return

    # Tap on "Send another gift"
    automation.tap(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.7)
    sleep(2)

    if not wait_for_correct_screen(automation, "Premium Giveaways"):
        handle_failure(automation)
        return

    # Tap on "Buy Premium for a User"
    automation.tap(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.6)
    sleep(2)

    # Tap for return
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.25)

    save_successful_username(username)


def wait_for_correct_screen(automation, expected_text, msg=True):
    message_displayed = False
    iteration_count = 0
    while True:
        iteration_count += 1

        # Take a screenshot
        screenshot = take_screenshot(automation.device)

        # Check if it's the desired screen
        if is_desired_screen(screenshot, expected_text):
            if message_displayed and msg:
                print("\033[92mSuccessfully found the desired screen: '{}'\033[0m".format(expected_text))
            sleep(0.5)
            return True

        if iteration_count > 50:
            print(f"Failed to find the '{expected_text}' screen within 100 seconds.")
            return False

        if not message_displayed and msg:
            print(f"Waiting for the '{expected_text}' screen to appear...")
            message_displayed = True

        sleep(1)


def handle_failure(automation):
    # Open "Tonkeeper" again
    automation.start_app("com.ton_keeper", ".TonkeeperActivity")
    sleep(2)

    # Tap for return
    for _ in range(3):
        automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.25)
        sleep(1)

    # Tap on reload
    for _ in range(2):
        automation.tap(SCREEN_WIDTH * 0.77, SCREEN_HEIGHT * 0.07)
        sleep(1)

    # Tap on "Buy Premium for a User"
    automation.tap(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.6)
    sleep(2)


def take_screenshot(device):
    image_data = device.screencap()
    return Image.open(BytesIO(image_data))


def get_screen_text(image):
    return pytesseract.image_to_string(image)


def is_desired_screen(image, expected_text, similarity_threshold=90):
    screen_text = get_screen_text(image)
    similarity = fuzz.partial_ratio(screen_text, expected_text)
    return similarity >= similarity_threshold


def save_successful_username(username, filename="successful_usernames.txt"):
    with open(filename, "a") as f:
        f.write(username + "\n")
