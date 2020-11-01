from abc import ABC, abstractmethod

from .exceptions import (
    MissingSQLStatementException,
    UnsupportedServiceActionException
)
from .factory_interfaces import (
    CloudFactory,
    StorageFactory,
    TargetFactory,
)


class AbstractCommand(ABC):

    def __init__(self, service, factory, results={}):
        self.client = factory.get_client(service)
        self.results = results

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    # TODO: from future point
    # @abstractmethod
    # def retry(self):
    #     pass

    # TODO: from future point
    # @abstractmethod
    # def reset(self):
    #     pass


class CloudCommand(AbstractCommand):

    def __init__(self, service="aws_cloud", results={}, **kwargs):
        factory = CloudFactory()
        self.client = factory.get_client(service, **kwargs)
        self.service = service
        self.results = results

    def execute(self, *args, **kwargs):
        resource = kwargs['resource']
        self.client.resource = resource
        for action in kwargs['actions']:
            actionable = action['actionable']

            try:
                callable = getattr(self.client, actionable)
            except AttributeError:
                err = f"Action: {actionable} is not available"\
                        " for service: {self.service}"
                raise UnsupportedServiceActionException(err)

            if action.get('result'):
                if action.get('params'):
                    self.results[actionable] = callable(action['params'])
                else:
                    self.results[actionable] = callable()
            else:
                callable()
        return self.results


class DatabaseStorageCommand(AbstractCommand):

    def __init__(self, service="sqlite_engine", results={}, **kwargs):
        factory = StorageFactory()
        self.client = factory.get_client(service, **kwargs)
        self.service = service
        self.results = results

    def execute(self, *args, **kwargs):
        for action in kwargs['actions']:
            actionable = action['actionable']

            # To handle if callable is not part of that service
            try:
                callable = getattr(self.client, actionable)
            except AttributeError as err:
                err = f"Action: {actionable} is not available"\
                        " for service: {self.service}"
                raise UnsupportedServiceActionException(err)

            sql = action.get('sql')
            if not sql and not action.get('setup'):
                raise MissingSQLStatementException

            # To handle setup calls from storage service
            if not sql:
                callable()
                continue

            if sql:
                # if action is query
                sql_type = actionable.split("_")[0]
                if sql_type in ['query', 'create', 'alter', 'drop', 'delete']:
                    if sql_type == "query":
                        self.results[actionable] = callable(sql)
                    else:
                        callable(sql)
                else:
                    # To handle inserts
                    sql_source = self.results[action['sql_data_source']]
                    for key, value in sql_source.items():
                        parameters = []
                        for param in action['format_keys']:
                            parameters.append(value[param])
                        sql_statement = action['sql']
                        callable(sql_statement, tuple(parameters))
        return self.results


class SSHConfigTargetCommand(AbstractCommand):

    def __init__(self, service="ssh_config_service", results={}, **kwargs):
        factory = TargetFactory()
        self.client = factory.get_client(service, **kwargs)
        self.service = service
        self.results = results

    def execute(self, *args, **kwargs):
        for action in kwargs['actions']:
            actionable = action['actionable']

            try:
                callable = getattr(self.client, actionable)
            except AttributeError:
                err = f"Action: {actionable} is not available"\
                        " for service: {self.service}"
                raise UnsupportedServiceActionException(err)

            if action.get('writeable'):
                data = self.results[action['data_source']]
                callable(data)
            else:
                callable()
        return self.results
