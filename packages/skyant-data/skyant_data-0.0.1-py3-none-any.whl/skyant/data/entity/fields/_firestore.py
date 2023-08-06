# pylint: disable=missing-module-docstring

import re
from google.cloud.firestore import Client


class FirestoreRef(str):
    '''
    Field type for define a reference between a Firestore documents.

    Takes a string that represents a Firestore document path. During saving to the firestore
    this field will be converted to a firestore.DocumentReference and back through an uploading.
    '''

    phantom: bool = True

    @classmethod
    def validate(cls, path):  # pylint: disable=missing-docstring

        pattern = r'^[\w\@\-\_\.]+/([\w\@\-\_\.]+/[\w\@\-\_\.]+/)*[\w\@\-\_\.]+$'

        assert re.match(pattern, path), \
            f'Wrong "path" argument. Should match an regex expression:\n{pattern}'

        assert len(path.split('/')) % 2 == 0, \
            'A document path must contain odd elements!'

        assert True if cls.phantom else Client().document(path).get().exists, \
            f'The document {path} does not exist and phantom links is not allowed.'

        return path

    @classmethod
    def __get_validators__(cls):

        yield cls.validate
