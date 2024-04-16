from rethinkdb import r


class RethinkDBConnection:
    def __init__(self, host='localhost', port=28015, db_name='test'):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.connection = None

    def connect(self):
        try:
            self.connection = r.connect(host=self.host, port=self.port, db=self.db_name)
            print("Connected to RethinkDB")
        except r.errors.RqlDriverError as err:
            print("Connection error:", err)

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")

    def create_table(self, table_name):
        try:
            r.table_create(table_name).run(self.connection)
            print("Table '{}' created successfully".format(table_name))
        except r.errors.RqlRuntimeError as err:
            print("Table creation error:", err)

    def insert_document(self, table_name, document):
        try:
            r.table(table_name).insert(document).run(self.connection)
            print("Document inserted successfully")
        except r.errors.RqlRuntimeError as err:
            print("Insertion error:", err)

    def get_documents(self, table_name):
        try:
            documents = r.table(table_name).run(self.connection)
            return list(documents)
        except r.errors.RqlRuntimeError as err:
            print("Retrieval error:", err)
            return []

    def get_documents_by_key(self, table_name, key, value):
        try:
            cursor = r.table(table_name).filter({key: value}).run(self.connection)
            documents = list(cursor)
            return documents
        except r.errors.RqlRuntimeError as err:
            print("Query error:", err)
            return []

    def create_geo_index(self, table_name, field_name):
        try:
            r.table(table_name).index_create(field_name, geo=True).run(self.connection)
            print("Geo index created successfully")
        except r.errors.RqlRuntimeError as err:
            print("Index creation error:", err)

    def get_documents_by_geo(self, table_name, field_name, longitude, latitude, radius):
        try:
            query = r.table(table_name).get_intersecting(
                r.circle([longitude, latitude], radius, {"unit": "km"}), index=field_name)
            documents = query.run(self.connection)
            return list(documents)
        except r.errors.RqlRuntimeError as err:
            print("Geoquery error:", err)
            return []

# if __name__ == "__main__":
#     # Create an instance of the RethinkDBConnection class
#     db_connection = RethinkDBConnection()
#
#     # Connect to the RethinkDB server
#     db_connection.connect()
#
#     # Example usage: Create a table if it doesn't exist
#     # db_connection.create_table('people')
#     #
#     # # Example usage: Insert a document into a table
#     # document = {"name": "John", "age": 30}
#     # db_connection.insert_document('people', document)
#
#     # Example usage: Retrieve documents from a table
#     documents = db_connection.get_documents('people')
#     doc=db_connection.get_documents_by_key(table_name='people',key='name', value='John')
#     print("Retrieved documents:", doc)
#
#
#     # Close the connection
#     db_connection.close()
