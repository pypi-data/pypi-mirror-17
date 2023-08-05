"""
Message consumer.

"""
from boto3 import client
from microcosm.api import defaults


class SQSConsumer(object):
    """
    Consume message from a (single) SQS queue.

    """
    def __init__(self,
                 sqs_client,
                 sqs_envelope,
                 sqs_queue_url,
                 limit,
                 wait_seconds):
        self.sqs_client = sqs_client
        self.sqs_envelope = sqs_envelope
        self.sqs_queue_url = sqs_queue_url
        self.limit = limit
        self.wait_seconds = wait_seconds

    def consume(self):
        """
        Consume a batch of messages.

        :returns: a list of `SQSMessage`
        """
        return [
            self.sqs_envelope.parse_raw_message(self, raw_message)
            for raw_message in self.sqs_client.receive_message(
                QueueUrl=self.sqs_queue_url,
                MaxNumberOfMessages=self.limit,
                WaitTimeSeconds=self.wait_seconds,
            ).get("Messages", [])
        ]

    def ack(self, message):
        """
        Acknowledge that a message was processed successfully.

        Deletes the message from the queue.

        """
        self.sqs_client.delete_message(
            QueueUrl=self.sqs_queue_url,
            ReceiptHandle=message.receipt_handle,
        )

    def nack(self, message):
        """
        Acknowledge that a message was NOT processed successfully.

        Does nothing, allowing queue dead-lettering to take effect.

        """
        pass


@defaults(
    # SQS will not return more than ten messages at a time
    limit=10,
    # SQS will only return a few messages at time unless long polling is enabled (>0)
    wait_seconds=1,
)
def configure_sqs_consumer(graph):
    """
    Configure an SQS consumer.

    """
    sqs_queue_url = graph.config.sqs_consumer.sqs_queue_url
    limit = graph.config.sqs_consumer.limit
    wait_seconds = graph.config.sqs_consumer.wait_seconds

    if graph.metadata.testing:
        from mock import MagicMock
        sqs_client = MagicMock()
    else:
        sqs_client = client("sqs")

    return SQSConsumer(
        sqs_client=sqs_client,
        sqs_envelope=graph.sqs_envelope,
        sqs_queue_url=sqs_queue_url,
        limit=limit,
        wait_seconds=wait_seconds,
    )
