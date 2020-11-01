import os

from .configuration import FILE_CRED, CONFIG_CRED


def load_credentials_via_file():
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = \
              FILE_CRED['AWS_SHARED_CREDENTIALS_FILE']
    os.environ['AWS_CONFIG_FILE'] = FILE_CRED['AWS_CONFIG_FILE']


def load_credentials_via_config():
    creds = {
        'aws_access_key_id': CONFIG_CRED['aws_access_key_id'],
        'aws_secret_access_key': CONFIG_CRED['aws_secret_access_key']
    }
    return creds

