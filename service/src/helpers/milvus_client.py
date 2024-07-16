# src/helpers/milvus_client.py
from pymilvus import connections, Collection, DataType, FieldSchema, CollectionSchema
import logging


class MilvusClient:
    """Client for interacting with Milvus database."""

    def __init__(self, host: str = 'localhost', port: str = '19530'):
        """
        Initialize the Milvus client and connect to the server.

        Args:
            host (str): Host address of Milvus server.
            port (str): Port number of Milvus server.
        """
        self.host = host
        self.port = port
        self.connect()

    def connect(self):
        """Connect to the Milvus server."""
        connections.connect(alias="default", host=self.host, port=self.port)
        logging.info(f"Connected to Milvus at {self.host}:{self.port}")

    def create_collection(self, collection_name: str, dimension: int):
        """
        Create a collection in Milvus.

        Args:
            collection_name (str): Name of the collection.
            dimension (int): Dimension of the vectors to be stored.
        """
        fields = [
            FieldSchema(
                name="embedding",
                dtype=DataType.FLOAT_VECTOR,
                dim=dimension),
            FieldSchema(
                name="id",
                dtype=DataType.INT64,
                is_primary=True,
                auto_id=True)
        ]
        schema = CollectionSchema(fields)
        collection = Collection(name=collection_name, schema=schema)
        logging.info(f"Created collection: {collection_name}")
        return collection

    def insert_vectors(self, collection_name: str, vectors: list):
        """
        Insert vectors into a collection.

        Args:
            collection_name (str): Name of the collection.
            vectors (list): List of vectors to insert.
        """
        collection = Collection(name=collection_name)
        entities = {"embedding": vectors}
        ids = collection.insert(entities)
        collection.load()
        logging.info(
            f"Inserted {len(vectors)} vectors into collection: {collection_name}")
        return ids

    def create_index(self, collection_name: str):
        """
        Create an index for the collection.

        Args:
            collection_name (str): Name of the collection.
        """
        collection = Collection(name=collection_name)
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {"nlist": 128}
        }
        collection.create_index(
            field_name="embedding",
            index_params=index_params)
        logging.info(f"Created index for collection: {collection_name}")

    def search_vectors(self, collection_name: str,
                       query_vectors: list, top_k: int):
        """
        Search for similar vectors in a collection.

        Args:
            collection_name (str): Name of the collection.
            query_vectors (list): List of query vectors.
            top_k (int): Number of top results to return.
        """
        collection = Collection(name=collection_name)
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = collection.search(
            query_vectors,
            "embedding",
            params=search_params,
            limit=top_k)
        logging.info(
            f"Searched for {len(query_vectors)} vectors in collection: {collection_name}")
        return results

    def drop_collection(self, collection_name: str):
        """
        Drop a collection from Milvus.

        Args:
            collection_name (str): Name of the collection.
        """
        collection = Collection(name=collection_name)
        collection.drop()
        logging.info(f"Dropped collection: {collection_name}")


if __name__ == "__main__":
    # Example usage
    client = MilvusClient()
    collection_name = 'example_collection'
    dimension = 128
    vectors = [[0.1 * i for i in range(dimension)] for _ in range(5)]

    client.create_collection(collection_name, dimension)
    client.insert_vectors(collection_name, vectors)
    client.create_index(collection_name)
    results = client.search_vectors(collection_name, vectors, top_k=3)

    for result in results:
        print(result)

    client.drop_collection(collection_name)
