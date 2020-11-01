def split_statements(sql_statements):
    return sql_statements.split(";")


class AtomicAction():
    def __init__(self, client, atomic):
        self.client = client
        self.atomic = atomic

    def __enter__(self):
        self.connection = self.client.get_service_connection()
        return self.connection

    def __exit__(self, *args):
        try:
            self.connection.commit()
        except Exception as err:
            print(f"Error while committing: {err}")
            if self.atomic:
                try:
                    self.connection.rollback()
                except Exception as err:
                    # An error during rollback means that something
                    # went wrong with the connection. Drop it.
                    print(f"Error while rolling back: {err}")
        finally:
            self.connection.close()
