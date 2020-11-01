from importlib import import_module

from cloud_services import settings as cloud_settings
from storage_services import settings as storage_settings
from target_services import settings as target_settings


from .exceptions import UnSupportedServiceException
from .utilities import smart_import


class CloudFactory:

    def get_client(self, service_type, **kwargs):
        supported_clouds = {}
        for service in cloud_settings.SUPPORTED_SERVICES:
            cloud = service.split(".")[0]
            supported_clouds[cloud] = service

        if service_type not in supported_clouds:
            raise UnSupportedServiceException

        client = smart_import('cloud_services.' + supported_clouds[service_type])
        return client()


class StorageFactory:

    def get_client(self, service_type, **kwargs):
        supported_storages = {}
        for service in storage_settings.SUPPORTED_SERVICES:
            storage = service.split(".")[1]
            supported_storages[storage] = service

        if service_type not in supported_storages:
            raise UnSupportedServiceException

        client = smart_import('storage_services.'+supported_storages[service_type])
        if service_type == "sqlite_engine":
            return client(database=kwargs['database'])
        return client()


class TargetFactory:

    def get_client(self, service_type):
        supported_targets = {}
        for service in target_settings.SUPPORTED_SERVICES:
            target = service.split(".")[0]
            supported_targets[target] = service

        if service_type not in supported_targets:
            raise UnSupportedServiceException

        client = smart_import('target_services.'+supported_targets[service_type])
        return client()
