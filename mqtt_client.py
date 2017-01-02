import paho.mqtt.client as mqtt
from config_handler import config
import datetime

class MQTT_Client(mqtt.Client):

    def __init__(self, name=None, subscribe_default=True):
        mqtt.Client.__init__(self)
        self.mqtt_broker = config.get('mqtt', 'broker', fallback='iot.eclipse.org')
        self.name = name
        if self.name is None:
            self.name = config.get('mqtt', 'client_id', fallback='default_client_id')
        self.port = config.getint('mqtt', 'port', fallback=1883)
        self.topic = config.get('mqtt', 'topic', fallback='default_topic')
        self.subscribe_default = subscribe_default
        self.on_message = self.cb_on_message
        self.on_connect = self.cb_on_connect
        self.on_publish = self.cb_on_publish
        self.on_subscribe = self.cb_on_subscribe
        self.on_log = self.cb_on_log

        self.connect(self.mqtt_broker, port=self.port, keepalive=60)
        self.loop_start()

        self.last_message = None
        return

    def cb_on_connect(self, client, userdata, flags, rc):
        print(datetime.datetime.now(), self.name, 'on_connect   |', "rc: " + str(rc))
        if self.subscribe_default:
            self.subscribe_to_default()

    def cb_on_message(self, client, userdata, msg):
        print(datetime.datetime.now(), self.name, 'on_message   |',  msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        self.last_message = msg.payload

    def cb_on_publish(self, client, userdata, mid):
        print(datetime.datetime.now(), self.name, 'on_publish   |',  "mid: " + str(mid))

    def cb_on_subscribe(self, client, userdata, mid, granted_qos):
        print(datetime.datetime.now(), self.name, 'on_subscribe |',  "Subscribed: " + str(mid) + " " + str(granted_qos))

    def cb_on_log(self, client, userdata, level, string):
        print(datetime.datetime.now(), self.name, 'on_log       |', string)

    def close(self):
        self.loop_stop()
        self.disconnect()
        return

    def subscribe_to_default(self):
        self.subscribe(self.topic)
        return

    def publish_msg(self, message):
        print(datetime.datetime.now(), self.name, 'Publishing:', message)
        self.publish(self.topic, message)
        return