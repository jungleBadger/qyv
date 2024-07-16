import os
import json
import logging
from pymilvus import connections, Collection, DataType, FieldSchema, CollectionSchema, utility
from concurrent.futures import ThreadPoolExecutor, as_completed


class MilvusClient:
    def __init__(self, host='localhost', port='19530',
                 collection_name='object_detections'):
        self.collection_name = collection_name
        self.connect(host, port)
        self.create_collection()
        self.create_index()

    def connect(self, host, port):
        connections.connect("default", host=host, port=port)

    def create_collection(self):
        if utility.has_collection(self.collection_name):
            logging.info(
                f"Deleting existing collection: {self.collection_name}")
            utility.drop_collection(self.collection_name)

        frame_id = FieldSchema(
            name="frame_id",
            dtype=DataType.INT64,
            is_primary=True,
            auto_id=True)
        frame_name = FieldSchema(
            name="frame_name",
            dtype=DataType.VARCHAR,
            max_length=255)
        object_class = FieldSchema(
            name="object_class",
            dtype=DataType.VARCHAR,
            max_length=255)
        confidence = FieldSchema(name="confidence", dtype=DataType.FLOAT)
        vector = FieldSchema(
            name="vector",
            dtype=DataType.FLOAT_VECTOR,
            dim=1000)  # Updated to match feature vector length

        schema = CollectionSchema(fields=[frame_id, frame_name, object_class, confidence, vector],
                                  description="Object detections with extracted features")
        self.collection = Collection(name=self.collection_name, schema=schema)
        logging.info(f"Created new collection: {self.collection_name}")

    def insert_data(self, data):
        self.collection.insert(data)
        self.collection.flush()
        logging.info(
            f"Inserted batch of {len(data)} records into collection: {self.collection_name}")

    def create_index(self):
        logging.info(f"Creating index for collection: {self.collection_name}")
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {
                "nlist": 128}}
        self.collection.create_index(
            field_name="vector",
            index_params=index_params)
        self.collection.load()
        logging.info(
            f"Index created and collection loaded: {self.collection_name}")


class IngestToMilvus:
    def __init__(self, frames_dir: str,
                 milvus_client: MilvusClient, batch_size=100):
        self.frames_dir = frames_dir
        self.milvus_client = milvus_client
        self.batch_size = batch_size
        logging.basicConfig(level=logging.INFO)

    def ingest_data(self):
        feature_files = [
            f for f in os.listdir(
                self.frames_dir) if f.endswith('_features.json')]
        detection_files = [
            f for f in os.listdir(
                self.frames_dir) if f.endswith('_detections.json')]

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for feature_file, detection_file in zip(
                    feature_files, detection_files):
                futures.append(
                    executor.submit(
                        self.process_files,
                        feature_file,
                        detection_file))

            for future in as_completed(futures):
                future.result()

    def process_files(self, feature_file, detection_file):
        feature_path = os.path.join(self.frames_dir, feature_file)
        detection_path = os.path.join(self.frames_dir, detection_file)

        try:
            with open(feature_path, 'r') as f:
                features_data = json.load(f)
            with open(detection_path, 'r') as f:
                detections_data = json.load(f)

            batch_data = []
            for detection in detections_data['detections']:
                if len(features_data['features']) != 1000:
                    logging.error(
                        f"Feature vector length for frame {features_data['frame']} does not match expected length of 1000")
                    continue

                data = {
                    "frame_name": features_data['frame'],
                    "object_class": detection['name'],
                    "confidence": detection['confidence'],
                    "vector": features_data['features']
                }
                batch_data.append(data)

                if len(batch_data) >= self.batch_size:
                    self.milvus_client.insert_data(batch_data)
                    logging.info(
                        f"Inserted batch data for frames: {[data['frame_name'] for data in batch_data]}")
                    batch_data.clear()

            # Insert any remaining data
            if batch_data:
                self.milvus_client.insert_data(batch_data)
                logging.info(
                    f"Ingested batch data for frame: {features_data['frame']}")

        except Exception as e:
            logging.error(
                f"Error processing files {feature_file} and {detection_file}: {e}")


# Example usage
if __name__ == "__main__":
    frames_dir = "path_to_frames"
    milvus_client = MilvusClient()
    ingester = IngestToMilvus(frames_dir, milvus_client)
    ingester.ingest_data()
    milvus_client.create_index()
