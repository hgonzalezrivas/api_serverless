import json
import boto3

class UpaxController():

    def __init__(self):
        self.client = boto3.client('lambda',
                                   region_name='us-east-1')

    def encrypt(self, data):
        payload = {
            'body': {
                'method': 'encrypt',
                'data': data
            }
        }

        return json.loads(self.client.invoke(
            FunctionName='upx_sls_domain_controller',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )['Payload'].read().decode('utf-8'))['body']['data']

    def decrypt(self, data):
        payload = {
            'body': {
                'method': 'decrypt',
                'data': data.decode('utf-8')
            }
        }

        return json.loads(self.client.invoke(
            FunctionName='upx_sls_domain_controller',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )['Payload'].read().decode('utf-8'))['body']['data']