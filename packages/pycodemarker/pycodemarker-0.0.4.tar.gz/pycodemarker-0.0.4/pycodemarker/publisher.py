import json
import datetime

import os

from urllib import request, parse

import base64

KAFKA_BROKERS = ['54.68.13.37:29092']
DRDROID_HOST = os.environ.get('DRDROID_HOST')

CORELLIAN_HOST = 'http://{}:8082/ingest_code_log'.format(DRDROID_HOST)

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

class Publisher():

    # def __init__(self):
        # self.producer = KafkaProducer(bootstrap_servers=KAFKA_BROKERS, value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    def get_base64(self, json_object):
        string_bytes = json.dumps(json_object).encode("ascii")
        base64_bytes = base64.b64encode(string_bytes)
        base64_string = base64_bytes.decode("ascii")
        return base64_string

    def clean(self, json_object):
        json_object["@timestamp"] = json_object["event_time"] #datetime.datetime.now().strftime(TIMESTAMP_FORMAT) #+ ".0000000000"
        return {"b64_enc_data": self.get_base64(json_object)}

    def send(self, extras):
        try:
            self.send_http(extras)
            # self.clean(extras)
            # self.producer.send('droid-events', extras)
        except:
            pass

    def send_http(self, extras):
        data = self.clean(extras)
        data = parse.urlencode(data).encode()
        req =  request.Request(CORELLIAN_HOST, data=data)
        resp = request.urlopen(req)