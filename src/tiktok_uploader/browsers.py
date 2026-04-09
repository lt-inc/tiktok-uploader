"""Gets the browser's given the user's input"""

from typing import Any, Literal

from patchright.sync_api import Page, sync_playwright

from tiktok_uploader import config, logger
from tiktok_uploader.types import ProxyDict

# Type alias for supported browsers
browser_t = Literal["chrome", "firefox", "webkit", "edge", "safari", "chromium"]


def get_browser(
    name: browser_t = "chrome",
    headless: bool = False,
    proxy: ProxyDict | None = None,
    *args,
    **kwargs,
) -> Page:
    """
    Gets a browser based on the name with the ability to pass in additional arguments
    """
    p = sync_playwright().start()

    # Patchright is chromium-focused; fallback unsupported engines to chromium.
    if name == "chrome" or name == "edge" or name == "chromium":
        browser_type = p.chromium
    elif name == "firefox":
        logger.warning("Patchright does not support Firefox; falling back to Chromium.")
        browser_type = p.chromium
    elif name == "webkit" or name == "safari":
        logger.warning("Patchright does not support WebKit/Safari; falling back to Chromium.")
        browser_type = p.chromium
    else:
        browser_type = p.chromium  # Default to chromium

    launch_args: dict[str, Any] = {
        "headless": headless,
        "args": [
            "--disable-blink-features=AutomationControlled",
        ],
    }

    if name == "chrome":
        launch_args["channel"] = "chrome"
    elif name == "edge":
        launch_args["channel"] = "msedge"

    if proxy:
        launch_args["proxy"] = {
            "server": f"{proxy['host']}:{proxy['port']}",
        }
        if "user" in proxy and "password" in proxy:
            launch_args["proxy"]["username"] = proxy["user"]
            launch_args["proxy"]["password"] = proxy["password"]

    browser = browser_type.launch(**launch_args)

    # Create a new context with stealth-like options if needed
    # For now, we use standard context but set locale/timezone if passed in kwargs
    # or rely on defaults.

    context_args: dict[str, Any] = {
        "viewport": {"width": 1280, "height": 720},
        "user_agent": config.disguising.user_agent,
        "locale": "en-US",
    }

    context = browser.new_context(**context_args)

    # Add init script to mask webdriver
    context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)

    page = context.new_page()
    page.set_default_timeout(config.implicit_wait * 1000)  # Convert seconds to ms

    return page
