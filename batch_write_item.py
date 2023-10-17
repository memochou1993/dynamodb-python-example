import boto3
import time

def batch_write_item(dynamodb_client, table_name, batch_items: list):
    request_items = {
        table_name: batch_items
    }

    response = dynamodb_client.batch_write_item(
        RequestItems=request_items
    )

    max_retries = 5
    retry_count = 0
    backoff = 2
    unprocessed_items = response.get('UnprocessedItems', {})
    while unprocessed_items and retry_count < max_retries:
        response = dynamodb_client.batch_write_item(
            RequestItems=unprocessed_items
        )
        unprocessed_items = response.get('UnprocessedItems', {})

        time.sleep(backoff**retry_count)  # exponential backoff
        retry_count += 1

    failed_items = [
        request['PutRequest']['Item']['term']
        for request in unprocessed_items.get(table_name, [])
    ]

    return dict(
        succeed_count=len(batch_items) - len(failed_items),
        failed_items=failed_items
    )

session = boto3.Session()

dynamodb_client = session.client('dynamodb')

table_name = 'WilliamTest'

items = [{'term': {'S': 'Apple' + str(i)}} for i in range(1, 100)]

batch_size = 25
batches = [items[i:i + batch_size] for i in range(0, len(items), batch_size)]

succeeded_items = []
failed_items = []

for batch in batches:
    try:
        request_items = [{'PutRequest': {'Item': item}} for item in batch]
        res = batch_write_item(dynamodb_client, table_name, request_items)
        # If there are "failed_items" in the result, consider it a batch failure.
        if res['failed_items']:
            failed_items.extend(batch)
        else:
            succeeded_items.extend(batch)
    except Exception as e:
        print('e', e)
        failed_items.extend(batch)

print('succeeded_items:', succeeded_items)
print('failed_items:', failed_items)
