from configparser import ConfigParser
from azure.cosmos import CosmosClient, PartitionKey, exceptions
import json

# get Database Secrets
file = "../config.ini"
config = ConfigParser()
config.read(file)

class Database():

    def __init__(self):
        self.client = None

    def connect(self):
        if self.client == None:
            url = config["Database"]["url"]
            key = config["Database"]["key"]
            self.client = CosmosClient(url, credential=key)
        else:
            raise RuntimeError("DB already connected")


    def create_db(self, database_name):

        if self.client == None:
            self.connect()

        self.database = self.client.create_database(database_name)
        # if exits exceptions.CosmosResourceExistsError

    def create_container(self, container_name, database_name):

        if self.client == None:
            self.connect()

        database = self.client.get_database_client(database_name)
        database.create_container(id=container_name, partition_key=PartitionKey(path="/productName"))
        # mögliche Fehler exceptions.CosmosResourceExistsError,  exceptions.CosmosHttpResponseError

    def insert_article(self, article, database, container):

        database_client = self.client.get_database_client(database)
        container_client = database_client.get_container_client(container)

        upload_item = article.__dict__
        key_underscore = [k[1:] for k in upload_item.keys() if k.startswith('_')]

        for key in key_underscore:
            # replace if possible
            try:
                upload_item[key] = article.__getattribute__(key)

            except AttributeError:
                print('ignore')

            # delete
            upload_item.pop('_' + key, None)

        container_client.upsert_item(upload_item)

    def print_all_data(self, database, container):
        database_client = self.client.get_database_client(database)
        container_client = database_client.get_container_client(container)

        # Enumerate the returned items
        for item in container_client.query_items(
                query=f'SELECT * FROM {container}',
                enable_cross_partition_query=True):
            print(json.dumps(item, indent=True))

    def query_id(self, database, container, id):
        database_client = self.client.get_database_client(database)
        container_client = database_client.get_container_client(container)

        item = container_client.query_items(
            query=f'SELECT * FROM {container}  Where {container}.id = "{id}"',
            enable_cross_partition_query=True)

        return list(item)[0]

    def close(self):
        self.client = None






