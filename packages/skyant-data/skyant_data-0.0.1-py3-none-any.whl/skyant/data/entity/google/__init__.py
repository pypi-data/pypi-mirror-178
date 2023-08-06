'''
Package contains classes for interacting with Google Cloud services.

Firestore:
    Saving & loading the data to/from [Google Firestore](https://cloud.google.com/firestore).

    [_skyant.data.entity.google.Firestore references_](references/google/Firestore.md)

Storage:
    The class Storage saves & loads the data to/from
        [Google Cloud Storage](https://cloud.google.com/storage).
    This class provides features for work with JSON & YAML formates now.

    [_skyant.data.entity.google.Storage references_](references/google/Storage.md)

Tasks:
    Tasks class sends a task to asynchronous queue
        [Google Cloud Tasks](https://cloud.google.com/tasks) with with the data in it.

    [_skyant.data.entity.google.Tasks references_](references/google/Tasks.md)

PubSub:
    Send a message to [Google PubSub topic](https://cloud.google.com/pubsub).

    [_skyant.data.entity.google.PubSub references_](references/google/PubSub.md)

'''

from ._firestore import Firestore
from ._storage import Blob
from ._tasks import Tasks
from ._pubsub import PubSub
