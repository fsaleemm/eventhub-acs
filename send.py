import asyncio, os, json
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

CONNECTION_STR = os.environ["EVENT_HUB_CONN_STR"]
EVENTHUB_NAME = os.environ['EVENT_HUB_NAME']

async def run():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STR, eventhub_name=EVENTHUB_NAME)
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Assuming JSON data
        dataBody = {
            'id': '2',
            'title': 'Second Event Update',
            'summary': 'This is my second event to be indexed in Azure Cognitive Search'
        }
        # Add events to the batch.
        event_data_batch.add(EventData(json.dumps(dataBody)))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())