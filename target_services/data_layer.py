import os
import sqlite3
from get_all_running_instances import get_running_instances


defaultKeyPath = '~/.ssh/keys/'
path_to_config = '/.ssh/aws_demo.config'
ssh_config_file = open(os.path.expanduser(
            '~') + path_to_config, 'w')

conn = sqlite3.connect(r'storage/instances.db')
curr = conn.cursor()
curr.execute("""
CREATE TABLE IF nOT EXISTS servers(
    id INT PRIMARY KEY,
    key_name TEXT,
    state TEXT,
    instance_id TEXT,
    created_on TEXT,
    public_ip TEXT,
    server_user TEXT,
    soft_delete INT DEFAULT 0
);
""")
conn.commit()
all_instances = get_running_instances()
for instance_id, key in enumerate(all_instances):
    sql = f"""INSERT INTO servers(id, key_name, state, instance_id,
              created_on, public_ip, server_user, soft_delete)
              VALUES({instance_id}, '{all_instances[key]['key_name']}',
              '{all_instances[key]['state']}',
              '{all_instances[key]['instance_id']}',
              '2020-30-10', '{all_instances[key]['public_ip']}',
              '{all_instances[key]['user']}', 0 );"""
    curr.execute(sql)
    conn.commit()

get_running_instances_sql = """ SELECT * from servers where state='running'"""
running_instances = curr.execute(get_running_instances_sql).fetchall()

for instance in running_instances:
    host_line = """Host {0}
                    HostName {1}
                    User {2}
                    IdentityFile {3}

                """.format(instance[1], instance[5], instance[6],
                           os.path.join(defaultKeyPath,
                           "{0}.pem".format(instance[1])))
    ssh_config_file.write(host_line)
