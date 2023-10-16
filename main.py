import boto3

session = boto3.Session()

dynamodb = session.client('dynamodb')

table_name = 'example'
last_name_value = 'Chou'

response = dynamodb.query(
    TableName=table_name,
    KeyConditionExpression='last_name = :value',
    ExpressionAttributeValues={
        ':value': {
            'S': last_name_value,
        },
    },
)

print(response)
