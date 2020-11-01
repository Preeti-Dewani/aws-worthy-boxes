ACTION_DEFINITIONS = {
    'AWS_SQLITE_SSH_CONFIG': {
        'cloud': {
            'command': 'CloudCommand',
            'service': 'aws_cloud',
            'resource': 'ec2',
            'actions': [{
                'actionable': 'get_ec2_instances_details',
                'result': True
            }]
        },
        'storage': {
            'command': 'DatabaseStorageCommand',
            'service': 'sqlite_engine',
            'database': 'instances.db',
            'actions': [{
                    'actionable': 'run_prerequisites',
                    'setup': True,
                },
                {
                    'actionable': 'insert_row',
                    'sql': "INSERT INTO servers(key_name, state, instance_id,"
                           "created_on, public_ip, server_user)"
                           "VALUES(?, ?, ?,"
                           "'2020-30-10', ?, ?);",
                    'format_keys': ['key_name', 'state',
                                    'instance_id', 'public_ip', 'user'],
                    'sql_data_source': 'get_ec2_instances_details',
                    'atomic': True,
                },
                {
                    'actionable': 'query_result',
                    'result': True,
                    'sql': "select * from servers where state='running';"
            }]
        },
        'target': {
            'command': 'SSHConfigTargetCommand',
            'service': 'ssh_config_service',
            'actions': [{
                'actionable': 'write_config_entry',
                'writeable': True,
                'data_source': 'query_result',
            }]
        }
    }
}
