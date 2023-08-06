import os
import logging
from typing import Callable
from signalsdk.local_mqtt import LocalMqtt
from signalsdk.api import get_app_config_api, get_local_device_config_api
from signalsdk.config import LOCALMQTT_SDK_TOPIC_PREFIX, LOCALMQTT_SDK_APPLICATION_CONFIG_TOPIC
from signalsdk.signal_exception import SignalAppLocalMqttEventCallBackError, \
    SignalAppConfigEnvError, SignalAppLocalHttpServerError, \
        SignalAppOnConfigChangedCallBackError

from .validator import throw_if_parameter_not_found_in

OnConfigurationChangeRequested=Callable[[dict], None]
OnEventReceived=Callable[[str], None]

class SignalApp:
    def __init__(self):
        self.localMqtt = None
        self.baseConfig = {}
        self.app_id = ""
        self.thing_name = ""
        self.account_id = ""
        self.configurationChangedCallback = None
        self.onEventReceivedCallback = None
        self.local_pub_topic = None

    def __get_application_config(self):
        appSettings = get_app_config_api(self.app_id)
        current_subtopic = self.localMqtt.get_subscribed_topic()
        if not appSettings:
            logging.info(f"{__name__}: signalsdk: "
                         f"failed to get application config. Ignore")
            return

        logging.debug(f"{__name__}: APP SETTING: {appSettings}")
        if 'settingsForSDK' in appSettings:
            sdkSettings = appSettings['settingsForSDK']
            if 'sdkSubTopic' in sdkSettings and sdkSettings['sdkSubTopic']:
                desired_subtopic = LOCALMQTT_SDK_TOPIC_PREFIX + \
                            sdkSettings['sdkSubTopic']
                self.__renew_topic_subscription(current_subtopic, desired_subtopic)
            if 'sdkPubTopic' in sdkSettings and sdkSettings['sdkPubTopic']:
                self.local_pub_topic = LOCALMQTT_SDK_TOPIC_PREFIX + \
                    sdkSettings['sdkPubTopic']
                logging.debug(f"{__name__}: signalsdk:local_pub_topic: {self.local_pub_topic}")

        if 'settingsForApp' in appSettings and \
            appSettings['settingsForApp']:
            # declare app setting dictionary
            settings_for_app_dict = {}
            # convert settingsForApp to json string
            for each_setting in appSettings['settingsForApp']:
                if each_setting['key'] and each_setting['value']:
                    settings_for_app_dict[each_setting['key']] = each_setting['value']
            logging.debug(f"{__name__}: APP SETTING FOR APP: {settings_for_app_dict}")
            try:
                logging.debug(f"{__name__}: signalsdk:calling configurationChangedCallback")
                self.configurationChangedCallback(settings_for_app_dict)
            except Exception as err:
                logging.info(f"{__name__}: signalsdk:__get_application_config "
                            f"function threw an error: {err}")
                raise SignalAppLocalMqttEventCallBackError from err
        else:
            logging.info(f"{__name__}: signalsdk:__get_application_config "
                        f"settingsForApp not found in appSettings")

    def __local_app_event_handler(self, event):
        try:
            self.onEventReceivedCallback(event)
        except Exception as error:
            logging.debug(f'{__name__}: App Event received: event: {event}')
            raise SignalAppLocalMqttEventCallBackError from error

    def __app_config_handler(self, event):
        try:
            logging.debug(f"{__name__}: signalsdk:on_config_change_requested"
                         f" received event: {event}")
            self.__get_application_config()
        except Exception as err:
            logging.info(f"{__name__}: Ignore event in config change callback. Error: {err}")
            raise SignalAppOnConfigChangedCallBackError from err

    def __start_listening_app_config_updates(self):
        #get application from device agent
        self.__get_application_config()
        app_config_topic = LOCALMQTT_SDK_APPLICATION_CONFIG_TOPIC.replace("${appId}", self.app_id)
        self.localMqtt.set_on_event_received(app_config_topic, self.__app_config_handler)
        self.localMqtt.subscribe(app_config_topic, False)
        app_local_event_topic = LOCALMQTT_SDK_TOPIC_PREFIX + self.app_id
        self.localMqtt.set_on_event_received(app_local_event_topic, self.__local_app_event_handler)
        self.localMqtt.subscribe(app_local_event_topic, False)

    def __renew_topic_subscription(self, current_topic, desired_topic):
        logging.debug(f"{__name__}: signalsdk:__renew_topic_subscription "
                     f"current_topic: {current_topic} "
                     f"desired_topic: {desired_topic}")
        if current_topic and current_topic != desired_topic:
            self.localMqtt.remove_event_callbacks(current_topic)
            self.localMqtt.unsubscribe()
        if desired_topic and current_topic != desired_topic:
            self.localMqtt.subscribe(desired_topic, True)
            self.localMqtt.set_on_event_received(desired_topic, self.__local_app_event_handler)

    def initialize(self, onConfiguratioChangedCallback: OnConfigurationChangeRequested,
                   onEventReceivedCallback: OnEventReceived):
        """Signal Application Initialize
        Following objects are created
        localMqtt: it is used to subscribe or publish to local MQTT broker
        served as local event bus
        :param onConfiguratioChangedCallback: call back function provided by
        signal application for configuration change
        :param onEventReceivedCallback: call back function provided by signal
        application for events handling
        """
        logging.info(f"{__name__}: signalsdk::Starting signal app initialize.")
        self.configurationChangedCallback = onConfiguratioChangedCallback
        self.onEventReceivedCallback = onEventReceivedCallback
        self.baseConfig = get_local_device_config_api()
        throw_if_parameter_not_found_in(self.baseConfig, 'device config', \
                                        'local http server', SignalAppLocalHttpServerError)
        self.thing_name = self.baseConfig['thingName']
        throw_if_parameter_not_found_in(self.thing_name, 'thing name', \
                                        'local http server', SignalAppLocalHttpServerError)
        self.account_id = self.baseConfig['accountId']
        throw_if_parameter_not_found_in(self.account_id, 'account id', \
                                        'local http server', SignalAppLocalHttpServerError)
        self.app_id = os.getenv('APPLICATION_ID')
        throw_if_parameter_not_found_in(self.app_id, 'application id', \
                                        'environment variables', SignalAppConfigEnvError)
        #generate local mqtt client id
        local_mqtt_client_id = self.thing_name + "_" + self.app_id
        self.localMqtt = LocalMqtt(local_mqtt_client_id)
        self.localMqtt.set_on_connected(self.__start_listening_app_config_updates)
        self.localMqtt.connect()

    def next(self, event, next_app_id=''):
        """Publish the event
        :param event: event received on local event bus
        :             nexe_app_id: next application to receive the event
        :return:
        """
        if not self.local_pub_topic and not next_app_id:
            logging.info(f"{__name__}: signalsdk:next "
                         f"called without topic to publish to: {event}")
            return
        logging.info(f"{__name__}: signalsdk: forwarding event: {event}")

        if next_app_id:
            topic = LOCALMQTT_SDK_TOPIC_PREFIX + next_app_id
            logging.debug(f"{__name__}: signalsdk next() publishing to "
                          f"applicationId topic: {topic}")
            self.localMqtt.publish(topic, event)
        elif self.local_pub_topic:
            logging.debug(f"{__name__}: signalsdk next() publishing to sdk topic: "
                         f"{self.local_pub_topic}")
            self.localMqtt.publish(self.local_pub_topic, event)
