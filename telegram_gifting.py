from time import sleep

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 2220


def gift_premium(automation, username):
    """
    Gifts a premium subsctiption to a specified Telegram username.
    """

    # Tap on the cancel cross
    automation.tap(SCREEN_WIDTH * 0.95, SCREEN_HEIGHT / 2 - 100)
    sleep(1)

    # Tap to enter username
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100)
    sleep(0.5)

    # Insert username
    automation.input_text(username)
    sleep(0.5)

    # Confirm username
    automation.press_keyevent(66)
    sleep(1)

    # Tap on "3 month"
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.7)
    sleep(0.5)

    # Tap on "Gift Telegram Premium"
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.76)
    sleep(2)

    # Tap on "Buy Gift for {username}"
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.9)
    sleep(2)

    # Tap on "Buy Premium with Tonkeeper"
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.85)
    sleep(3)

    # Tap on "Confirm"
    automation.tap(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.9)
    sleep(2)

    # Temporary tap for return
    automation.tap(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.25)
    sleep(1)
