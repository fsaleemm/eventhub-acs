# Azure Event Hub Consumer Client to Index events with Azure Cognitive Search

This is a sample Event Hub consumer client code to demonstrate the ability to index event data with Azure Cognitive Search by using an Event Hub Consumer Client. This sample uses Python SDK for [Event Hub](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-python-get-started-send) and [Azure Cognitive Search](https://docs.microsoft.com/en-us/python/api/overview/azure/search-documents-readme?view=azure-python).

## Pre-work

1. Python 3.6 or later
1. Setup and [Event Hub Namespace and an Event Hub](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-create).
1. Setup the [Azure Cognitive Search service](https://docs.microsoft.com/en-us/azure/search/search-create-service-portal).

## Setup the Search Index

Create an index with the following fields and the index schema.

1. id
1. title
1. summary

![Index Setup](/images/s1.png)

## Setup the Environment

### Install Python Packages

Install Azure Event Hub packages

```bash
pip install azure-eventhub
pip install azure-eventhub-checkpointstoreblob-aio
```

Install Azure Cognitive Search packages

```bash
pip install azure-search-documents
```

### Setup Variables

Set the Event Hub connection information environment variables.

```bash
export EVENT_HUB_CONN_STR="<Your Event Hub Namespace Connection String>"
export EVENT_HUB_NAME="<Your Event Hub Name>"
```

NOTE: The default consumer group "$Default" is used by the sample.

Setup the Cognitive Search connection information environment variables.

```bash
export SEARCH_ENDPOINT="<Your Azure Cognitive Search Endpoint>"
export SEARCH_API_KEY="<Your Search API Key>"
export SEARCH_INDEX_NAME="<Your Search Index Name>"
```

## Run the Sample Code

### Run the Receiver

To test that you can receive events from the Event Hub without sending data to Azure Cognitive Search run the "receiver.py"

Run the receiver in a terminal that indexes data to Azure Cognitive Search.

```bash
python3 receiver-acs.py
```

![Run receiver](/images/s2.png)

### Run the Sender

In a separate terminal window run the Event Hub sender code.

```bash
python3 send.py
```

When the sender runs, there should be an indication on the receiver terminal that data was uploaded successfully to Azure Cognitive Search.

![Run receiver](/images/s3.png)

Go to the Azure Cognitive Search service and to the index you created and in the Search Explorer click "Search". You should see the data sent to Event Hub will be indexed in Azure Cognitive Search.

![Run receiver](/images/s4.png)
