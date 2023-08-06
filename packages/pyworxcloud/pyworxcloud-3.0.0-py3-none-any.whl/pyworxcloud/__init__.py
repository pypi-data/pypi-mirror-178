"""IoT mower platform module - Positec/Worx/Kress/Landxcape."""
from __future__ import annotations

import json

from .commands import WorxCommand
from .datamapping import DataMap
from .endpoints import CloudType
from .exceptions import MowerNotFoundError, TokenError
from .handlers.mqtt import MQTT
from .handlers.requests import GET, HEADERS
from .status import WorxError, WorxStatus
from .token import Token


class WorxCloud:
    """Class of WorxCloud."""

    def __init__(
        self,
        email: str,
        password: str,
        cloud: CloudType.WORX
        | CloudType.KRESS
        | CloudType.LANDXCAPE
        | str = CloudType.WORX,
        debug: bool = False,
    ) -> None:
        """Initialize a WorxCloud object."""
        self._email = email
        self._password = password
        self._do_debug = debug

        self.mowers = []

        if isinstance(cloud, str):
            try:
                cloud = getattr(CloudType, cloud.upper())
            except AttributeError:
                raise TypeError(
                    "Wrong type specified, valid types are: worx, landxcape or kress"
                )

        self._cloud = cloud

        # Get token from AUTH endpoint
        self.token = Token(self._email, self._password, self._cloud)

        if isinstance(self.token.access_token, type(None)) or isinstance(
            self.token.refresh_token, type(None)
        ):
            raise TokenError("Access or refresh token was not found")

        # Get all available mowers and convert them to a list of serial numbers
        mowers = GET(
            f"https://{self._cloud.ENDPOINT}/api/v2/product-items?status=1",
            HEADERS(self.token.access_token),
        )

        self.mowers = []
        for mower in mowers:
            new_mower = {}
            data = DataMap(mower, self._do_debug)
            if not isinstance(data, type(None)):
                new_mower.update(data)
            else:
                for key in mower:
                    if key in [
                        "serial_number",
                        "user_id",
                        "mqtt_endpoint",
                        "name",
                        "mqtt_topics",
                    ]:
                        new_mower.update({key: mower[key]})

            new_mower.update({"has_data": False})
            self.mowers.append(new_mower)

        mqtt_endpoint = self.mowers[0]["mqtt_endpoint"]
        user_id = self.mowers[0]["user_id"]

        # Initialize the MQTT connector
        self.mqtt = MQTT(
            self.token.access_token,
            self._cloud.BRAND_PREFIX,
            mqtt_endpoint,
            user_id,
            self.on_update,
        )

    @property
    def status(self) -> WorxStatus | WorxError:
        """Return the status or error state."""

    def do_debug(self, should_debug: bool) -> None:
        """Enables/disables some debug in the results, including unknown keys from the API."""
        self._do_debug = should_debug

    def get_mower(self, serial_number: str) -> dict:
        """Get a specific mower."""
        for mower in self.mowers:
            if mower["serial_number"] == serial_number:
                return mower

        raise MowerNotFoundError(
            f"Mower with serialnumber {serial_number} was not found."
        )

    def connect(self) -> None:
        """Connect to MQTT and subscribe to updates."""
        for mower in self.mowers:
            self.mqtt.subscribe(mower["mqtt_topics"]["command_out"])

        self.mqtt.connect()

    def disconnect(self) -> None:
        """Disconnect from MQTT."""
        self.mqtt.disconnect()

    def update(self, serial_number) -> None:
        """Request a state refresh."""
        mower = self.get_mower(serial_number)
        self.mqtt.ping(serial_number, mower["mqtt_topics"]["command_in"])

    def write_data(self, serial_number: str, data: str) -> None:
        """Update mower data."""
        data = DataMap(data, self._do_debug)

        if isinstance(data, type(None)):
            return  # Exit if no data was present

        for mower in self.mowers:
            if mower["serial_number"] == serial_number:
                mower.update(data)
                mower.update({"has_data": True})
                break

    def on_update(self, topic, payload, dup, qos, retain, **kwargs):
        """Triggered when a MQTT message was received."""
        data = json.loads(payload)
        self.write_data(data["cfg"]["sn"], data)

    def send_command(self, serial_number: str, command: WorxCommand) -> None:
        """Send a command to the mower."""
        self.mqtt.publish(
            self.mqtt.format_message(serial_number, {"cmd": command.value})
        )
