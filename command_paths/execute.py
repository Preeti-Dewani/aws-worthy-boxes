from abc import ABC, abstractmethod

from .action_definitions import ACTION_DEFINITIONS
from .command_interfaces import (
    CloudCommand,
    DatabaseStorageCommand,
    SSHConfigTargetCommand,
)
from .exceptions import (
    UnknownActionException,
    UnSupportedCommandException,
)


class Controller:

    def __init__(self, action_name):
        self.action_name = action_name
        self.get_pipeline()

    def get_pipeline(self):
        try:
            self._pipeline = ACTION_DEFINITIONS[self.action_name]
        except KeyError:
            raise UnknownActionException
        return self._pipeline

    def executor(self):
        result = {}
        if self.action_name == "AWS_SQLITE":
            result = CloudDatabaseFacade(self).proceed()
        elif self.action_name == "AWS_SQLITE_SSH_CONFIG":
            result = CloudDatabaseSSHFacade(self).proceed()
        return result


class FacadeInterface(ABC):
    def __init__(self, ctrl_obj):
        self.controller = ctrl_obj
        self.pipeline = ctrl_obj.get_pipeline()

    @abstractmethod
    def proceed(self):
        pass


class CloudDatabaseFacade(FacadeInterface):

    def proceed(self):
        cloud_details = self.pipeline['cloud']

        if cloud_details['command'] == "CloudCommand":
            results = CloudCommand().execute(**cloud_details)
        else:
            raise UnSupportedCommandException

        storage_details = self.pipeline['storage']

        if storage_details['command'] == 'DatabaseStorageCommand':
            kwargs = {'database': storage_details['database']}
            results = DatabaseStorageCommand(
                        results=results, **kwargs).execute(**storage_details)
        else:
            raise UnSupportedCommandException
        return results


class CloudDatabaseSSHFacade(CloudDatabaseFacade):

    def proceed(self):
        results = super().proceed()

        target_details = self.pipeline['target']

        if target_details['command'] == 'SSHConfigTargetCommand':
            SSHConfigTargetCommand(results=results).execute(**target_details)
        return results

