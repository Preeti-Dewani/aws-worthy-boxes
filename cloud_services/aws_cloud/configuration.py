import os

BASE_DIR = os.path.dirname(__file__)

FILE_CRED = {
    'AWS_SHARED_CREDENTIALS_FILE': os.path.join(BASE_DIR, '.aws/credentials'),
    'AWS_CONFIG_FILE': os.path.join(BASE_DIR, '.aws/config'),
}

CONFIG_CRED = {
    'aws_access_key_id': 'XXXXX',
    'aws_secret_access_key': 'YYYYYY',
}