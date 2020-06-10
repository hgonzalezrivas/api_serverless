import boto3
import json

class RemoteConfig:

    bucket = 'upaxer-serverless-api'
    file = 'config_sls/upx_sls_config.json'

    def __init__(self):
        self.client = boto3.client('s3')

    def get_config(self):
        return json.loads(self.client.get_object(Bucket = self.bucket, Key = self.file)['Body'].read().decode())