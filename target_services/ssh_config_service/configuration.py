import os

path_to_config = '/.ssh/aws_demo.config'
DEFAULT_SSH_CONFIG_FILE_PATH = [os.path.expanduser('~') + path_to_config]


defaultKeyPath = '/.ssh/keys/'
DEFAULT_KEYS_PATH = [os.path.expanduser('~') + defaultKeyPath]

SSH_CONFIG_FORMAT = """
                    Host {host_to_access}
                    HostName {public_ip}
                    User {user_of_server}
                    IdentityFile {file_location_of_key}

                    """
