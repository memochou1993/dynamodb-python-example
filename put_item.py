from client import dynamodb_client, table_name;

term = 'Apple0'

response = dynamodb_client.put_item(
    TableName=table_name,
    Item={
        'term': {
            'S': term,
        },
    }
)

print(response)
