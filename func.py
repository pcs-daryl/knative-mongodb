from parliament import Context, event
from pymongo import MongoClient
import logging
import sys
import copy

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)  # Write to stdout
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def connect_and_insert(mongo_uri="mongodb://my-user:admin@example-mongodb-svc:27017/knative?authMechanism=SCRAM-SHA-256", 
                       collection_name=None, 
                       payload=None):
    """
    Connects to the MongoDB server and inserts data into a specified collection.

    Args:
        mongo_uri (str): The MongoDB URI with credentials. Defaults to a sample URI.
        collection_name (str): The name of the collection to insert data into.
        payload (dict or list): The data to insert. Can be a dictionary for a single document 
                                or a list of dictionaries for multiple documents.

    Returns:
        str: Success message or error message.
    """
    if not collection_name:
        return "Collection name must be provided."
    
    if not payload:
        return "Payload must be provided."

    try:
        # Create a MongoDB client with credentials in the URI
        client = MongoClient(mongo_uri)
        
        # Access the 'hello' database
        db = client['knative']
        
        # Access the specified collection
        collection = db[collection_name]
        logger.info(payload)

        # Insert data
        if isinstance(payload, list):
            result = collection.insert_many(payload)
            return f"Inserted {len(result.inserted_ids)} documents into '{collection_name}' collection."
        elif isinstance(payload, dict):
            result = collection.insert_one(payload)
            return f"Inserted document with ID: {result.inserted_id} into '{collection_name}' collection."
        else:
            return "Payload must be a dictionary or a list of dictionaries."
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        # Close the MongoDB connection
        client.close()

@event
def main(context: Context):
    """
    Function template
    The context parameter contains the Flask request object and any
    CloudEvent received with the request.
    """

    # Add your business logic here
    data = context.cloud_event.data
    collection_name = data["collection_name"]
    data.pop('collection_name', None)
    data_copy = copy.deepcopy(data)
    
    result = connect_and_insert(collection_name=collection_name, payload=data)
    # The return value here will be applied as the data attribute
    # of a CloudEvent returned to the function invoker
    return {"result":result, "data": data_copy}
