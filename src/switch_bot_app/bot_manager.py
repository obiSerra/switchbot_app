import json

from aws_lambda_powertools import Logger
from switch_bot_app.errors import CommandNotSupportedError, UnauthorizedError
from switch_bot_app.autentication import authenticate, AuthData


import requests
import logging

BASE_URL = "https://api.switch-bot.com"


logger = Logger()


def parse_request(r):
    response = r.json()
    logger.info(response)

    if r.status_code == 401:
        raise UnauthorizedError(f"Unauthorized request to {r.url}")
    elif response["statusCode"] == 160:
        logging.error(response)
        raise CommandNotSupportedError(response.get("message", "Command not supported"))

    body = response.get("body")

    if body is None or len(body.keys()) == 0:
        logging.error(response)
    return body


class Device:
    def __init__(self, auth_data, device_id) -> None:
        self.auth_data = auth_data
        self.base_url = BASE_URL
        self.device_id = device_id

    def status(self):
        r = requests.get(f"{self.base_url}/v1.1/devices/{self.device_id}/status", headers=self.auth_data.to_headers())
        body = parse_request(r)
        return body

    def command(self, command):
        body = json.dumps(command)
        headers = {"Content-Type": "application/json"}
        headers = {**headers, **self.auth_data.to_headers()}

        r = requests.post(
            f"{self.base_url}/v1.1/devices/{self.device_id}/commands",
            headers=headers,
            data=body,
        )
        return parse_request(r)


class Bot(Device):
    def press(self):
        command = {"command": "press", "parameter": "default", "commandType": "command"}
        return self.command(command)

    def turn_on(self):
        command = {"command": "turnOn", "parameter": "default", "commandType": "command"}
        return self.command(command)

    def turn_off(self):
        command = {"command": "turnOff", "parameter": "default", "commandType": "command"}
        return self.command(command)


def make_request(token, sign, nonce, t, body):
    device_id = "D7:FC:3F:CE:0A:7A"
    base_url = "https://api.switch-bot.com"
    path = f"/v1.1/devices/{device_id}/commands"
    headers = {
        "Authorization": token,
        "sign": sign,
        "nonce": nonce,
        "t": t,
        "Content-Type": "application/json",
        "Content-Length": len(body),
    }
    r = requests.post(base_url + path, headers=headers, data=body)
    return r


class BotManager:
    def __init__(self, token, secret) -> None:
        self.auth_data: AuthData = authenticate(token, secret)
        self.base_url = BASE_URL

    def get_device_list(self):
        r = requests.get(f"{self.base_url}/v1.1/devices", headers=self.auth_data.to_headers())
        body = parse_request(r)
        return body["deviceList"]

    def get_device_by_id(self, device_id):
        return Bot(self.auth_data, device_id)
