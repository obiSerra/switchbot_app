from switch_bot_app.bot_manager import BotManager
from switch_bot_app.errors import ConfigurationMissingError

import os


if __name__ == "__main__":
    token = os.environ.get("SWITCHBOT_TOKEN")
    secret = os.environ.get("SWITCHBOT_SECRET")
    if token is None:
        raise ConfigurationMissingError("SWITCHBOT_TOKEN not found in environment variables")
    if secret is None:
        raise ConfigurationMissingError("SWITCHBOT_SECRET not found in environment variables")

    bot_manager = BotManager(token, secret)
    # print(bot_manager.get_device_list())
    citofono_id = token = os.environ.get("SWITCHBOT_CITOFONO_ID")
    if citofono_id is None:
        raise ConfigurationMissingError("SWITCHBOT_CITOFONO_ID not found in environment variables")
    citofono = bot_manager.get_device_by_id(citofono_id)
    # print(citofono.status())
    print(citofono.press())
