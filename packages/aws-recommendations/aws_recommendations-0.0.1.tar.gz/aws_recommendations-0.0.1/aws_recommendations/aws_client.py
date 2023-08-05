from aws_recommendations import functions as fn
from boto3 import session


class aws_client:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.session = session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        self.recommendation = {}

    get_recommendations = fn.get_recommendations
