import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from config_handler import config
import datetime
from queue import Queue, Empty
import time
import threading
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import aws_client
import mqtt_client
import rekognition_api as rekognition
from multiprocessing import Pool
from pprint import pprint as pp
import json

def timeout(seconds):
    print(datetime.datetime.now(), 'Timeout', seconds, 'seconds')
    time.sleep(seconds)

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.jpg", "*.png"]

    def __init__(self):
        PatternMatchingEventHandler.__init__(self)
        self.client = aws_client.get_client('rekognition', verify=True)
        self.last_modification = None
        self.last_file = None
        self.mqttc = mqtt_client.MQTT_Client(name='ScreenshotWatchdogPub', subscribe_default=False)
        return

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        print(datetime.datetime.now(), event.src_path, event.event_type)
        return

    def on_modified(self, event):
        self.process(event)
        self.last_modification= datetime.datetime.now()

    def on_created(self, event):
        self.process(event)
        if 'face_crop' not in event.src_path:
            self.last_modification = datetime.datetime.now()
            self.last_file = event.src_path

            # Wait x seconds for the file to finish copying
            pool = Pool(processes=1)
            pool.apply_async(timeout, [1], callback=self.check_last_modification_timestamp)

    def check_last_modification_timestamp(self, seconds):
        now = datetime.datetime.now()
        time_difference_us = (now - self.last_modification).microseconds
        time_difference_sec = (now - self.last_modification).seconds
        time_difference = (time_difference_sec * 1000000) + time_difference_us
        print('td=', time_difference)
        if time_difference > 500000:
            print('Time difference > 0.5sec')
            self.request_screenshot_analysis(self.last_file)
        return

    def request_screenshot_analysis(self, image_url, collection_id=None, face_match_threshold=80.0):
        if not collection_id:
            collection_id = config.get('rekognition', 'default_collection', fallback='col_reyeslua')
        res = rekognition.search_all_faces_by_image(self.client, image_url, collection_id, face_match_threshold=face_match_threshold)
        print(datetime.datetime.now(), 'Results:')
        pp(res)
        self.mqttc.publish_msg(json.dumps(res))
        return

class ScreenshotWatchdog(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.watched_folder = config.get('rekognition', 'tmp_folder', fallback='')
        return

    def run(self):
        observer = Observer()
        observer.schedule(MyHandler(), path=self.watched_folder)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()
        return

if __name__ == "__main__":
    screenshot_watchdog = ScreenshotWatchdog()
    screenshot_watchdog.start()

