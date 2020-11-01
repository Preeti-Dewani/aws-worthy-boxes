import botocore
import boto3

from .exceptions import (
    IncorrectServiceException,
)
from .loader import (
    load_credentials_via_file,
    load_credentials_via_config,
)


class AWSClient:
    def __init__(self, load_via="file", resource="ec2"):
        self._load_via = load_via
        self._resource = resource
        self.service_client = self.get_service_client()

    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, resource):
        self._resource = resource
        self.service_client = self.get_service_client()

    @property
    def load_via(self):
        return self._load_via

    @load_via.setter
    def load_via(self, load_via):
        self._load_via = load_via
        self.service_client = self.get_service_client()

    def get_service_client(self):
        cred_source = self._load_via
        resource = self._resource
        if cred_source == "file":
            load_credentials_via_file()
            client = boto3.client(resource)
            return client

        creds = load_credentials_via_config()
        client = boto3.client(
            resource,
            aws_access_key_id=creds['aws_access_key_id'],
            aws_secret_access_key=creds['aws_secret_access_key'],
        )
        return client

    def get_ec2_instances_details(self):
        if self._resource != "ec2":
            raise IncorrectServiceException
        try:
            reservations = self.service_client.describe_instances()
        except botocore.exceptions.ClientError as error:
            raise error
        except botocore.exceptions.ParamValidationError as error:
            raise ValueError(f'The parameters you provided are incorrect:\
                             {error}')

        all_instances = {}
        for reservation in reservations['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                all_instances[instance_id] = {
                    'state': instance['State']['Name'],
                    'key_name': instance['KeyName'],
                    'instance_id': instance_id,
                    'public_ip': instance.get('PublicIpAddress', 'na'),
                    'user': 'ec2-user'
                }
        return all_instances




