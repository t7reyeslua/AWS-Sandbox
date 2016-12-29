import boto3
from os import environ
from config_handler import config

aws_clients = {}

class AWS_Client:
    def __init__(self, api_name, region_name=None, endpoint_url=None,
                 verify=False, aws_access_key_id=None, aws_secret_access_key=None):
        '''Create new AWS Client'''
        self.api_name = api_name
        self.region_name = region_name
        self.endpoint_url = endpoint_url
        self.verify = verify
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.api = None
        self.get_client()
        return

    def get_client(self):
        # Get the access keys configured from the config file
        if self.aws_access_key_id is None:
            self.aws_access_key_id = config.get('credentials', 'AWS_ACCESS_KEY_ID', fallback=None)
        if self.aws_secret_access_key is None:
            self.aws_secret_access_key = config.get('credentials', 'AWS_SECRET_ACCESS_KEY', fallback=None)

        # Get the access keys configured from the system
        if self.aws_access_key_id is None:
            self.aws_access_key_id = environ.get('AWS_ACCESS_KEY_ID', None)
        if self.aws_secret_access_key is None:
            self.aws_secret_access_key = environ.get('AWS_SECRET_ACCESS_KEY', None)

        if not self.aws_access_key_id or not self.aws_access_key_id:
            raise Exception('Missing AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY')

        # Get actual client
        self.api = boto3.client(
            self.api_name,
            # region_name= config.get(self.api_name, 'endpoint', fallback='eu-west-1'),
            # endpoint_url= config.get(self.api_name, 'endpoint', fallback='https://rekognition.eu-west-1.amazonaws.com'),
            # verify=self.verify,
            # aws_access_key_id=self.aws_access_key_id,
            # aws_secret_access_key=self.aws_secret_access_key
        )
        return self.api

def get_client(api_name, region_name=None, endpoint_url=None,
               verify=False, aws_access_key_id=None, aws_secret_access_key=None):
    '''
    Find a client by api_name. If not found, create a new one.
    '''
    try:
        return aws_clients[api_name]
    except KeyError:
        # Client does not exist
        new_client = AWS_Client(api_name, region_name, endpoint_url,
                 verify, aws_access_key_id, aws_secret_access_key)
        aws_clients[api_name] = new_client
        return new_client

def find_client(api_name):
    '''
    Find a client by api_name.
    '''
    try:
        return aws_clients[api_name]
    except KeyError:
        # Client does not exist
        return None