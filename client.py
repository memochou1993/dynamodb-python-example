import boto3

session = boto3.Session()

dynamodb_client = session.client('dynamodb')

table_name = 'WilliamTest'
