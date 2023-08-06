# pylint: disable=missing-docstring

import json
from abc import ABC
from enum import Enum

from google.auth import default as gauth
from google.cloud import tasks_v2 as gtasks
from pydantic import BaseModel


class LocationClass(Enum):
    '''
    Enumerator of Google Locations where Google Cloud Tasks service works.
    '''

    US_WEST1 = 'us-west1'
    US_WEST2 = 'us-west2'
    US_WEST4 = 'us-west4'
    US_CENTRAL1 = 'us-central1'
    US_EAST1 = 'us-east1'
    US_EAST4 = 'us-east4'
    NORTHAMERICA_NORTHEAST1 = 'northamerica-northeast1'
    SOUTHAMERICA_EAST1 = 'southamerica-east1'
    EUROPE_WEST2 = 'europe-west2'
    EUROPE_WEST1 = 'europe-west1'
    EUROPE_WEST6 = 'europe-west6'
    EUROPE_WEST3 = 'europe-west3'
    EUROPE_CENTRAL2 = 'europe-central2'
    ASIA_SOUTH1 = 'asia-south1'
    ASIA_SOUTHEAST1 = 'asia-southeast1'
    ASIA_SOUTHEAST2 = 'asia-southeast2'
    ASIA_EAST2 = 'asia-east2'
    ASIA_EAST1 = 'asia-east1'
    ASIA_NORTHEAST1 = 'asia-northeast1'
    ASIA_NORTHEAST2 = 'asia-northeast2'
    AUSTRALIA_SOUTHEAST1 = 'australia-southeast1'
    ASIA_NORTHEAST3 = 'asia-northeast3'


class Tasks(BaseModel, ABC):
    '''
    Class provides the method for making a task in [Google Cloud Tasks](https://cloud.google.com/tasks)
        (serverless asynchronous queue).
    '''

    @classmethod
    @property
    def Location(cls) -> LocationClass:  # pylint: disable=invalid-name
        '''
        Provides a LocationClass to make import more clear in your project.
        '''

        return LocationClass

    @classmethod
    @property
    def Method(cls) -> gtasks.HttpMethod:  # pylint: disable=invalid-name
        '''
        Provides an enumerator of HTTP methods. Use it for making clear import statements.
        '''

        return gtasks.HttpMethod

    def send_gtasks(
        self,
        queue: str,
        location: LocationClass,
        url: str,
        method: gtasks.HttpMethod,
        name: str | None = None
    ) -> str:
        '''
        Make a task in Google Tasks from data.

        Args:

            url (str): The URL for sending request to.

            queue (str): The queue name for making task in.

            location (LocationClass): Google Cloud region where Tasks queue is located.

            method (gtasks.HttpMethod): The HTTP method which Google Tasks should be used for
                doing the task.

            name (str | None, optional): Name of the new task in the queue. Will be assigned
                randomly if empty.

        Returns:
            Task name.
        '''

        client = gtasks.CloudTasksClient()
        parent = client.queue_path(str(gauth()[1]), location.value, queue)

        task = {
            "http_request": {
                "http_method": method.value,
                "headers": {"Content-type": "application/json"},
                "url": url,
                "body": json.dumps(self.dict()).encode()
            }
        }

        if name:
            task['name'] = client.task_path(str(gauth()[1]), location.value, queue, name)

        response = client.create_task(
            request={"parent": parent, "task": task}
        )

        return response.name
