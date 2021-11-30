import os, json
from azure.eventhub import EventHubConsumerClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Connection information about Event Hub
CONNECTION_STR = os.environ["EVENT_HUB_CONN_STR"]
EVENTHUB_NAME = os.environ['EVENT_HUB_NAME']

# Connection information about Cognitive Saerch
endpoint = os.environ["SEARCH_ENDPOINT"]
key = os.environ["SEARCH_API_KEY"]
index_name = os.environ["SEARCH_INDEX_NAME"]

def send_to_index(doc):
    search_client = SearchClient(endpoint, index_name, AzureKeyCredential(key))

    result = search_client.merge_or_upload_documents(documents=[doc])
    print("Upload of new document succeeded: {}".format(result[0].succeeded))


def on_event(partition_context, event):
    # Put your code here.
    print(event.body_as_str())

    send_to_index(json.loads(event.body_as_str()))

    # If the operation is i/o intensive, multi-thread will have better performance.
    print("Received event from partition: {}.".format(partition_context.partition_id))

    partition_context.update_checkpoint(event)


def on_partition_initialize(partition_context):
    # Put your code here.
    print("Partition: {} has been initialized.".format(partition_context.partition_id))


def on_partition_close(partition_context, reason):
    # Put your code here.
    print("Partition: {} has been closed, reason for closing: {}.".format(
        partition_context.partition_id,
        reason
    ))


def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


if __name__ == '__main__':
    consumer_client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group='$Default',
        eventhub_name=EVENTHUB_NAME,
    )

    try:
        with consumer_client:
            consumer_client.receive(
                on_event=on_event,
                on_partition_initialize=on_partition_initialize,
                on_partition_close=on_partition_close,
                on_error=on_error,
                starting_position="-1",  # "-1" is from the beginning of the partition.
            )
    except KeyboardInterrupt:
        print('Stopped receiving.')