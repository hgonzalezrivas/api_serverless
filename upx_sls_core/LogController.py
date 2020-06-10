import boto3
from json import dumps
from datetime import datetime
import time

class LogController():

    def stream(self, path, service_name, request, response):
        client = boto3.client('firehose', region_name = 'us-east-1')
        event = {}
        event['os'] = request['os']
        event['userId'] = request['userId']
        del request['os']
        del request['userId']
        event['request'] = dumps(request)
        event['response'] = dumps(response)
        event['path'] = path
        event['service'] = service_name
        event[u'EventTime'] = datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        client.put_record(
            DeliveryStreamName = 'LOGS_UPXSLS',
            Record = {
                'Data': dumps(event)
            }
        )

