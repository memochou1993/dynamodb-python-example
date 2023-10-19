import sys
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
        success_count=len(batch_items) - len(failed_items),
        failed_items=failed_items
    )

sys.modules[__name__] = batch_write_item
