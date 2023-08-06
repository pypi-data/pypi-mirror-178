#  pylint: disable=missing-module-docstring

import json
from os import environ as env

from google.auth import default
from google.cloud import pubsub_v1 as pubsub
from pydantic import BaseModel

CURRENT_PROJECT = env.get('GCP_PROJECT', None) or str(default()[1])


class PubSub(BaseModel):
    '''
    Extending a pydantic.BaseModel for sending data to
        [Google Cloud PubSub Topic](https://cloud.google.com/pubsub/).
    '''

    def send_pubsub(
        self,
        topic: str,
        attributes: dict | None = None,
        project: str = CURRENT_PROJECT,
        timeout: int = 5
    ) -> str:  # TODO: skyant/data/data.entity#3
        '''
        Send the model data to the Google PubSub topic.

        Args:

            topic (str): The PubSub topic name for send to.

            attributes (dict | None, optional): PubSub message's attributes.
                Must be a dictionary with strings as a values.

            project (str, optional): Google Cloud Platform project id where runs the topic.
                The default value will be got from google.auth.default.

            timeout (int, optional): Timeout for waiting an acceptable confirmation from PubSub.

        Raises:
            RuntimeError: Error during sending PubSub messages. Message contains a tracing from
                google.cloud.PubSub.Client.

        Returns:
            Message identifier.
        '''

        publisher = pubsub.PublisherClient()
        path = publisher.topic_path(project, topic)

        data = json.dumps(self.dict())

        _attributes = {}
        if attributes:
            _attributes = {k: v for k, v in attributes.items() if isinstance(v, str)}
            _attributes = None if len(_attributes.keys()) == 0 else _attributes

        try:

            if _attributes:
                publish_future = publisher.publish(path, data.encode('utf-8'), **_attributes)
            else:
                publish_future = publisher.publish(path, data.encode('utf-8'))

            result = publish_future.result(timeout=timeout)
        except Exception as ex:
            raise RuntimeError(f'The PubSub message failed on topic {path} with data:\n{data}\n{ex}') from ex

        return result
