from parliament import Context, event
from pymongo import MongoClient
import logging
import sys

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)  # Write to stdout
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def connect(mongo_uri="mongodb://my-user:admin@example-mongodb-svc:27017/hello?authMechanism=SCRAM-SHA-256"):
    """
    Connects to the MongoDB server and retrieves all collections from the 'test' database.
    
    Args:
        mongo_uri (str): The MongoDB URI with credentials. Defaults to 
                         'mongodb://username:password@localhost:27017/'.

    Returns:
        list: A list of collection names in the 'test' database.
    """
    try:
        # Create a MongoDB client with credentials in the URI
        client = MongoClient(mongo_uri)
        
        # Access the 'test' database
        db = client['hello']
        
        # Get the list of collections
        collections = db.list_collection_names()
        return collections
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
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

    # print(connect())
    data = context.cloud_event.data
    data["recevied"] = "true"
    data["stuff"] = connect()
    logger.info(data)
    # The return value here will be applied as the data attribute
    # of a CloudEvent returned to the function invoker
    return data
