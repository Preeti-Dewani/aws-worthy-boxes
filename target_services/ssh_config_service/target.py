import os

from .configuration import (
    DEFAULT_KEYS_PATH,
    DEFAULT_SSH_CONFIG_FILE_PATH,
    SSH_CONFIG_FORMAT,
)


class SSHConfigClient:
    def __init__(self, file_path=DEFAULT_SSH_CONFIG_FILE_PATH[0]):
        self.ssh_config_file = file_path

    def write_config_entry(self, data):
        with open(self.ssh_config_file, 'w') as ptr:
            for instance in data:
                try:
                    key_path = os.path.join(DEFAULT_KEYS_PATH[0],
                                            "{0}.pem".format(instance[1]))
                    host_line = SSH_CONFIG_FORMAT.format(
                                host_to_access=instance[1],
                                public_ip=instance[5],
                                user_of_server=instance[6],
                                file_location_of_key=key_path)
                    ptr.write(host_line)
                except KeyError as err:
                    raise err
                except Exception as err:
                    raise err
