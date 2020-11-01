CREATE TABLE IF NOT EXISTS `servers`(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_name TEXT,
    state TEXT,
    instance_id TEXT,
    created_on TEXT,
    public_ip TEXT,
    server_user TEXT
);