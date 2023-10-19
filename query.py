from client import dynamodb_client, table_name;

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
