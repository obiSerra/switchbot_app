import os
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, CORSConfig, Response, ResponseBuilder

import json
from switch_bot_app.bot_manager import BotManager

from switch_bot_app.errors import ConfigurationMissingError

logger = Logger()

cors_config = CORSConfig(allow_origin="*", max_age=300)
app = ApiGatewayResolver(cors=cors_config)


def gen_response(status_code, body):
    """Gen response."""
    logger.info("Generate Response", extra={"status_code": status_code, "body": body})
    try:
        return Response(
            status_code=status_code,
            content_type="application/json",
            body=json.dumps(body, use_decimal=True),
            headers=cors_config.to_dict(),
        )
    except Exception:
        logger.exception("Response Generation Exception", extra={"status_code": status_code, "body": body})


token = os.environ.get("SWITCHBOT_TOKEN")
secret = os.environ.get("SWITCHBOT_SECRET")
if token is None:
    raise ConfigurationMissingError("SWITCHBOT_TOKEN not found in environment variables")
if secret is None:
    raise ConfigurationMissingError("SWITCHBOT_SECRET not found in environment variables")


@app.get("/devices")
def get_devices():
    logger.info("Get Devices", extra={"token": token, "secret": secret})
    bot_manager = BotManager(token, secret)
    devices = bot_manager.get_device_list()
    # logger.info("Get Devices", extra={"devices": devices})
    return devices


def lambda_handler(event, context):
    """Lambda handler."""

    try:
        logger.info("Received Event", extra={"event": event})
        return app.resolve(event, context)
    except Exception as err:
        logger.error("Catch All Exception", extra={"error": err})
        return {"statusCode": 500, "body": "Internal Server Error"}
