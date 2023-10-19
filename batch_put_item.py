from client import dynamodb_client, table_name;
import batch_write_item;

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
