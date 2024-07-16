# src/helpers/milvus_client.py

from milvus import Milvus, DataType
import numpy as np
import logging


class MilvusClient:
    def __init__(self, host='localhost', port='19530'):
        """
        Initialize the Milvus client.

        :param host: The hostname of the Milvus server.
        :param port: The port of the Milvus server.
        """
        self.client = Milvus(host, port)
        logging.info(f"Connected to Milvus at {host}:{port}")

    def create_collection(self, collection_name, dimension,
                          index_file_size=1024, metric_type='L2'):
        """
        Create a collection in Milvus.

        :param collection_name: Name of the collection to create.
        :param dimension: The dimension of the vectors to be stored.
        :param index_file_size: Size of each index file.
        :param metric_type: The metric type for similarity search.
        """
        param = {
            'collection_name': collection_name,
            'dimension': dimension,
            'index_file_size': index_file_size,
            'metric_type': metric_type
        }
        status = self.client.create_collection(param)
        if not status.OK():
            logging.error(f"Failed to create collection: {status}")
        else:
            logging.info(f"Collection {collection_name} created.")

    def insert_vectors(self, collection_name, vectors):
        """
        Insert vectors into a collection.

        :param collection_name: The name of the collection.
        :param vectors: A list of vectors to insert.
        """
        status, ids = self.client.insert(
            collection_name=collection_name, records=vectors)
        if not status.OK():
            logging.error(f"Failed to insert vectors: {status}")
        else:
            logging.info(f"Inserted vectors with ids: {ids}")
        return ids

    def create_index(self, collection_name,
                     index_type='IVF_FLAT', params=None):
        """
        Create an index on the collection.

        :param collection_name: The name of the collection.
        :param index_type: The type of index to create.
        :param params: Additional parameters for the index.
        """
        if params is None:
            params = {"nlist": 16384}
        status = self.client.create_index(collection_name, index_type, params)
        if not status.OK():
            logging.error(f"Failed to create index: {status}")
        else:
            logging.info(f"Index created for collection {collection_name}.")

    def search_vectors(self, collection_name, query_vectors,
                       top_k=10, params=None):
        """
        Search for similar vectors in a collection.

        :param collection_name: The name of the collection.
        :param query_vectors: A list of vectors to search for.
        :param top_k: The number of top results to return.
        :param params: Additional search parameters.
        :return: The search results.
        """
        if params is None:
            params = {"nprobe": 16}
        status, results = self.client.search(
            collection_name, top_k, query_vectors, params)
        if not status.OK():
            logging.error(f"Failed to search vectors: {status}")
        else:
            logging.info(f"Search results: {results}")
        return results

    def drop_collection(self, collection_name):
        """
        Drop a collection from Milvus.

        :param collection_name: The name of the collection to drop.
        """
        status = self.client.drop_collection(collection_name)
        if not status.OK():
            logging.error(f"Failed to drop collection: {status}")
        else:
            logging.info(f"Collection {collection_name} dropped.")


if __name__ == "__main__":
    # Example usage
    client = MilvusClient()
    client.create_collection("example_collection", 128)
    vectors = [np.random.rand(128).tolist() for _ in range(10)]
    client.insert_vectors("example_collection", vectors)
    client.create_index("example_collection")
    query_vector = [np.random.rand(128).tolist()]
    results = client.search_vectors("example_collection", query_vector)
    print("Search results:", results)
    client.drop_collection("example_collection")
