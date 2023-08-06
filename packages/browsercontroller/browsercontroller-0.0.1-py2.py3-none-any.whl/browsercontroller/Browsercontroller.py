"""Gets a website controller and opens it."""
import time
from typing import Any

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from browsercontroller.Hardcoded import Hardcoded
from browsercontroller.helper import get_browser_drivers, open_url


# pylint: disable=R0903
# pylint: disable=R0913
class Browsercontroller:
    """Gets the GitLab runner from the GitLab server."""

    def __init__(
        self,
        url: str,
        default_profile: bool = True,
    ) -> None:
        """Initialises object that gets the browser controller, then it gets
        the issues from the source repo, and copies them to the target repo."""

        # Store the hardcoded values used within this project
        self.hardcoded = Hardcoded()

        # get browser drivers
        get_browser_drivers(self.hardcoded)
        driver = initialise_website_controller(default_profile)
        time.sleep(1)

        # Go to extension settings.
        driver = open_url(
            driver,
            url,
        )
        time.sleep(1)


# pylint: disable=R0903
def initialise_website_controller(default_profile: bool) -> Any:
    """Constructs object that controls a firefox browser.

    TODO: Allow user to switch between running browser
    in background or foreground.
    """
    hardcoded = Hardcoded()
    # To run Firefox browser in foreground
    print("Loading geckodriver")
    try:
        options = Options()

        if default_profile:
            options.add_argument("-profile")
            options.add_argument(hardcoded.firefox_profile)
        else:
            options.add_argument("-private")

        # options.add_argument("window-size=400,600")
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)

        driver = webdriver.Firefox(
            options=options,
            executable_path=r"firefox_driver/geckodriver",
        )

        return driver
    # pylint: disable=W0707
    except ValueError:
        # pylint: disable=W0707
        raise Exception(
            "Error, you have the snap Firefox browser installed. Please"
            " use the apt one instead. This switching is automated"
            + " in a bash script of the Self-host GitLab."
        )

    # To run Firefox browser in background
    # os.environ["MOZ_HEADLESS"] = "1"
    # self.driver = webdriver.Firefox(
    # executable_path=r"firefox_driver/geckodriver")

    # To run Chrome browser in background
    # options = webdriver.ChromeOptions();
    # options.add_argument('headless');
    # options.add_argument('window-size=1200x600'); // optional
