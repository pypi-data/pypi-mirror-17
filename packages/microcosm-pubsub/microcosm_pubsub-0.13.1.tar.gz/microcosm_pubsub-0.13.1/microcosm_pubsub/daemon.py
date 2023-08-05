"""
Consume Daemon main.

"""
from abc import abstractproperty

import microcosm.opaque  # noqa
from microcosm_daemon.api import SleepNow
from microcosm_daemon.daemon import Daemon


class ConsumerDaemon(Daemon):

    def make_arg_parser(self):
        parser = super(ConsumerDaemon, self).make_arg_parser()
        parser.add_argument("--sqs-queue-url")
        return parser

    @abstractproperty
    def schema_mappings(self):
        """
        Define the PubSub message media-type to schema mappings.

        """
        pass

    def handler_mappings(self):
        """
        Define the PubSub message media-type to handler mappings.

        This function is an alternative to configuring `graph.sqs_message_handlers` as
        a graph component; it's useful for very simple mappings (e.g. that don't need access
        to the graph.)

        """
        return {}

    @property
    def defaults(self):
        dct = dict(
            pubsub_message_codecs=dict(
                mappings=self.schema_mappings,
            ),
            sqs_consumer=dict(
                visibility_timeout_seconds=None,
            ),
        )
        if self.handler_mappings:
            dct.update(
                sqs_message_dispatcher=dict(
                    mappings=self.handler_mappings,
                ),
            )
        if self.args.sqs_queue_url:
            dct.sqs_consumer.sqs_queue_url = self.args.sqs_queue_url

        return dct

    @property
    def components(self):
        return super(ConsumerDaemon, self).components + [
            "opaque",
            "pubsub_message_codecs",
            "sqs_consumer",
            "sqs_message_dispatcher",
        ]

    def __call__(self, graph):
        """
        Implement daemon by sinking messages from the consumer to a dispatcher function.

        """
        result = graph.sqs_message_dispatcher.handle_batch()
        if not result.message_count:
            raise SleepNow()
