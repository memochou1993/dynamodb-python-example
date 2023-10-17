import boto3

session = boto3.Session()

dynamodb_client = session.client('dynamodb')

table_name = 'WilliamTest'
term = 'Apple1'

response = dynamodb_client.query(
    TableName=table_name,
    KeyConditionExpression='term = :value',
    ExpressionAttributeValues={
        ':value': {
            'S': term,
        },
    },
)

print(response)
