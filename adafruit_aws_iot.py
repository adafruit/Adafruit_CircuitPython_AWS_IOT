# SPDX-FileCopyrightText: 2019 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_aws_iot`
================================================================================

Amazon AWS IoT MQTT Client for CircuitPython


* Author(s): Brent Rubell

Implementation Notes
--------------------

**Hardware:**


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""
import json
from adafruit_minimqtt.adafruit_minimqtt import MMQTTException

try:
    from typing import Optional, Type, Union
    from types import TracebackType
    from adafruit_minimqtt.adafruit_minimqtt import MQTT
except ImportError:
    pass

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_AWS_IOT.git"


class AWS_IOT_ERROR(Exception):
    """Exception raised on MQTT API return-code errors."""

    # pylint: disable=unnecessary-pass
    pass


class MQTT_CLIENT:
    """Client for interacting with Amazon AWS IoT MQTT API.

    :param ~MQTT.MQTT mmqttclient: Pre-configured MiniMQTT Client object.
    :param int keep_alive: Optional Keep-alive timer interval, in seconds.
                          Provided interval must be 30 <= keep_alive <= 1200.

    """

    def __init__(self, mmqttclient: MQTT, keep_alive: int = 30) -> None:
        if "MQTT" in str(type(mmqttclient)):
            self.client = mmqttclient
        else:
            raise TypeError(
                "This class requires a preconfigured MiniMQTT object, \
                                please create one."
            )
        # Verify MiniMQTT client object configuration
        try:
            self.cid = self.client.client_id
            assert (
                self.cid[0] != "$"
            ), "Client ID can not start with restricted client ID prefix $."
        except Exception as ex:
            raise TypeError(
                "You must provide MiniMQTT with your AWS IoT Device's Identifier \
                                as the Client ID."
            ) from ex
        # Shadow-interaction topic
        self.shadow_topic = "$aws/things/{}/shadow".format(self.cid)
        # keep_alive timer must be between 30 <= keep alive interval <= 1200 seconds
        # https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html
        assert (
            30 <= keep_alive <= 1200
        ), "Keep_Alive timer \
            interval must be between 30 and 1200 seconds"
        self.keep_alive = keep_alive
        # User-defined MQTT callback methods must be init'd to None
        self.on_connect = None
        self.on_disconnect = None
        self.on_message = None
        self.on_subscribe = None
        self.on_unsubscribe = None
        # Connect MiniMQTT callback handlers
        self.client.on_connect = self._on_connect_mqtt
        self.client.on_disconnect = self._on_disconnect_mqtt
        self.client.on_message = self._on_message_mqtt
        self.client.on_subscribe = self._on_subscribe_mqtt
        self.client.on_unsubscribe = self._on_unsubscribe_mqtt
        self.connected_to_aws = False

    def __enter__(self) -> "MQTT_CLIENT":
        return self

    def __exit__(
        self,
        exception_type: Optional[Type[type]],
        exception_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.disconnect()

    @property
    def is_connected(self) -> bool:
        """Returns if MQTT_CLIENT is connected to AWS IoT MQTT Broker"""
        return self.connected_to_aws

    def disconnect(self) -> None:
        """Disconnects from Amazon AWS IoT MQTT Broker and de-initializes the MiniMQTT Client."""
        try:
            self.client.disconnect()
        except MMQTTException as error:
            raise AWS_IOT_ERROR("Error disconnecting with AWS IoT: ", error) from error
        self.connected_to_aws = False
        # Reset user-defined callback methods to None
        self.on_connect = None
        self.on_disconnect = None
        self.on_message = None
        self.on_subscribe = None
        self.on_unsubscribe = None
        self.client.deinit()

    def reconnect(self) -> None:
        """Reconnects to the AWS IoT MQTT Broker"""
        try:
            self.client.reconnect()
        except MMQTTException as error:
            raise AWS_IOT_ERROR("Error re-connecting to AWS IoT:", error) from error

    def connect(self, clean_session: bool = True) -> None:
        """Connects to Amazon AWS IoT MQTT Broker with Client ID.

        :param bool clean_session: Establishes a clean session with AWS broker.

        """
        try:
            self.client.connect(clean_session)
        except MMQTTException as error:
            raise AWS_IOT_ERROR("Error connecting to AWS IoT: ", error) from error
        self.connected_to_aws = True

    # MiniMQTT Callback Handlers
    # pylint: disable=not-callable, unused-argument
    def _on_connect_mqtt(
        self, client: MQTT, userdata: str, flag: int, ret_code: int
    ) -> None:
        """Runs when code calls on_connect.

        :param ~MQTT.MQTT client: MiniMQTT client object.
        :param str user_data: User data from broker
        :param int flag: QoS flag from broker.
        :param int ret_code: Return code from broker.

        """
        self.connected_to_aws = True
        # Call the on_connect callback if defined in code
        if self.on_connect is not None:
            self.on_connect(self, userdata, flag, ret_code)

    # pylint: disable=not-callable, unused-argument
    def _on_disconnect_mqtt(
        self, client: MQTT, userdata: str, flag: int, ret_code: int
    ) -> None:
        """Runs when code calls on_disconnect.

        :param ~MQTT.MQTT client: MiniMQTT client object.
        :param str user_data: User data from broker
        :param int flag: QoS flag from broker.
        :param int ret_code: Return code from broker.

        """
        self.connected_to_aws = False
        # Call the on_connect callback if defined in code
        if self.on_connect is not None:
            self.on_connect(self, userdata, flag, ret_code)

    # pylint: disable=not-callable
    def _on_message_mqtt(self, client: MQTT, topic: str, payload: str) -> None:
        """Runs when the client calls on_message.

        :param ~MQTT.MQTT client: MiniMQTT client object.
        :param str topic: MQTT broker topic.
        :param str payload: Payload returned by MQTT broker topic

        """
        if self.on_message is not None:
            self.on_message(self, topic, payload)

    # pylint: disable=not-callable
    def _on_subscribe_mqtt(
        self, client: MQTT, user_data: str, topic: int, qos: int
    ) -> None:
        """Runs when the client calls on_subscribe.

        :param ~MQTT.MQTT client: MiniMQTT client object.
        :param str user_data: User data from broker
        :param str topic: Desired MQTT topic.
        :param int qos: Quality of service level for topic, from broker.

        """
        if self.on_subscribe is not None:
            self.on_subscribe(self, user_data, topic, qos)

    # pylint: disable=not-callable
    def _on_unsubscribe_mqtt(
        self, client: MQTT, user_data: str, topic: str, pid: int
    ) -> None:
        """Runs when the client calls on_unsubscribe.

        :param ~MQTT.MQTT client: MiniMQTT client object.
        :param str user_data: User data from broker
        :param str topic: Desired MQTT topic.
        :param int pid: Process ID.
        """
        if self.on_unsubscribe is not None:
            self.on_unsubscribe(self, user_data, topic, pid)

    # MiniMQTT Network Control Flow
    def loop(self) -> None:
        """Starts a synchronous message loop which maintains connection with AWS IoT.
        Must be called within the keep_alive timeout specified to init.
        This method does not handle network connection/disconnection.

        Example of "pumping" an AWS IoT message loop:
        ..code-block::python

            while True:
                aws_iot.loop()

        """
        if self.connected_to_aws:
            self.client.loop()

    def loop_forever(self) -> None:
        """Begins a blocking, asynchronous message loop.
        This method handles network connection/disconnection.
        """
        if self.connected_to_aws:
            self.client.loop_forever()

    @staticmethod
    def validate_topic(topic: str) -> None:
        """Validates if user-provided pub/sub topics adhere to AWS Service Limits.
        https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html

        :param str topic: Desired topic to validate
        """
        assert hasattr(topic, "split"), "Topic must be a string"
        assert len(topic) < 256, "Topic must be less than 256 bytes!"
        assert len(topic.split("/")) <= 9, "Topics are limited to 7 forward slashes."

    # MiniMQTT Pub/Sub Methods, for usage with AWS IoT
    def subscribe(self, topic: str, qos: int = 1) -> None:
        """Subscribes to an AWS IoT Topic.

        :param str topic: MQTT topic to subscribe to.
        :param int qos: Desired topic subscription's quality-of-service.

        """
        assert qos < 2, "AWS IoT does not support subscribing with QoS 2."
        self.validate_topic(topic)
        self.client.subscribe(topic, qos)

    def publish(
        self, topic: str, payload: Union[str, float, bytes], qos: int = 1
    ) -> None:
        """Publishes to a AWS IoT Topic.

        :param str topic: MQTT topic to publish to.
        :param payload: Data to publish to topic.  Must be able to be converted
            to a string using ``str()``
        :type payload: str|float|bytes
        :param int qos: Quality of service level for publishing

        """
        assert qos < 2, "AWS IoT does not support publishing with QoS 2."
        self.validate_topic(topic)
        if isinstance(payload, int or float):
            payload = str(payload)
        self.client.publish(topic, payload, qos=qos)

    # AWS IoT Device Shadow Service

    def shadow_get_subscribe(self, qos: int = 1) -> None:
        """Subscribes to  device's shadow get response.

        :param int qos: Optional quality of service level.
        """
        self.client.subscribe(self.shadow_topic + "/get/#", qos)

    def shadow_subscribe(self, qos: int = 1) -> None:
        """Subscribes to all notifications on the device's shadow update topic.

        :param int qos: Optional quality of service level.
        """
        self.client.subscribe(self.shadow_topic + "/update/#", qos)

    def shadow_update(self, document: str):
        """Publishes a request state document to update the device's shadow.

        :param str state_document: JSON-formatted state document string.
        """
        self.client.publish(self.shadow_topic + "/update", document)

    def shadow_get(self) -> None:
        """Publishes an empty message to shadow get topic to get the device's shadow."""

        self.client.publish(
            self.shadow_topic + "/get", json.dumps({"message": "ignore"})
        )

    def shadow_delete(self) -> None:
        """Publishes an empty message to the shadow delete topic to delete a device's shadow"""

        self.client.publish(
            self.shadow_topic + "/delete", json.dumps({"message": "delete"})
        )
