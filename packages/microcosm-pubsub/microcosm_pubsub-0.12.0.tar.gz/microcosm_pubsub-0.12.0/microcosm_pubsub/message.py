"""
A single SQS message.

"""


class SQSMessage(object):
    """
    SQS message wrapper.

    """
    def __init__(self, consumer, content, media_type, message_id, receipt_handle):
        self.consumer = consumer
        self.content = content
        self.media_type = media_type
        self.message_id = message_id
        self.receipt_handle = receipt_handle

    def ack(self):
        """
        Acknowledge this message was processed successfully.

        """
        self.consumer.ack(self)

    def nack(self):
        """
        Acknowledge this message was NOT processed successfully.

        """
        self.consumer.nack(self)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type is None:
            self.ack()
        else:
            self.nack()
