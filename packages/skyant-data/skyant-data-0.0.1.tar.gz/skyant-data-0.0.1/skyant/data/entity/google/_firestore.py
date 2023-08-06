# pylint: disable=missing-docstring

from __future__ import annotations

from warnings import warn

from google.cloud import firestore
from pydantic import BaseModel

from ...tools.file import SaveLoad
from ..fields import FirestoreRef
from ...tools import e, w


class Firestore(SaveLoad):
    '''
    Class for saving & loading data to [Google Firestore](https://cloud.google.com/firestore).

    This class provide next additional features:
        - transparency creating references between documents;
        - transparency convert references to string after upload data;
        - manage multilinguals content (ROADMAP).
    '''

    @staticmethod
    def firestore_encoder(src: BaseModel | list, **kw) -> dict:
        '''
        Recursion function for looking for a FirestoreRef fields and convert them into
            firestore.References objects.

        Args:
            src: Pydantic BaseModel or inherited instance for encoding.

        Returns:
            dict: Dict with firestore.DocumentReference as field if source field in FirestoreRef.
        '''

        if isinstance(src, BaseModel):

            src_data = src.dict(**kw)
            keys4processing = src_data.keys()

            data = {}
            for key in keys4processing:

                field = src.__fields__[key]

                if issubclass(field.type_, FirestoreRef):
                    data[key] = firestore.Client().document(src_data[key])

                elif issubclass(src.__fields__[key].type_, (BaseModel, list)):
                    data[key] = Firestore.firestore_encoder(getattr(src, key), **kw)

                else:
                    data[key] = src_data[key]

        elif isinstance(src, list):

            data = [
                Firestore.firestore_encoder(i, **kw) for i in src
            ]

        else:
            data = src

        return data

    @staticmethod
    def firestore_decoder(src: dict) -> dict:
        '''
        This method convert all founded objects firestore.DocumentReference to string which
            represent path to the firestore document.

        Args:

            src: Dictionary from Google Firestore.

        Returns:

            dict: Dictionary with firestore.DocumentReference replaced with string.
        '''

        if isinstance(src, dict):

            data = {}

            for key, value in src.items():

                if isinstance(value, (dict, list)):
                    data[key] = Firestore.firestore_decoder(value)

                elif isinstance(value, firestore.DocumentReference):
                    data[key] = value.path

                else:
                    data[key] = value

        elif isinstance(src, list):

            data = [
                Firestore.firestore_decoder(i) for i in src
            ]

        else:
            data = src

        return data

    def save_firestore(
        self,
        path: str,
        overwrite: bool = False,
        raise_exists: bool = True,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False
    ) -> str | None:
        '''
        Save the data to the firestore with overwriting and/or creating the document.

        Args:

            path: The path for saving the data to.

            overwrite: Allow to overwrite the existing document. If True the existing document will be
                overwrites, if False and the document exist save command will be ignored.

            raise_exists: Require raise an exception in the document exist and overwrite is not allowed.
                If True will be raised an exception, if False will be send a warning.

            exclude_none: Keep or pass empty values. If True, file will be contains "NaN" values.

            exclude_unset: Write or ignore default values. If False default values won't be written.

        Raises:
            DocumentExists: If the document exists and overwrite is False.

        Returns:
            New's document ID if was provided path to collection or None.
        '''

        fs_client = firestore.Client()

        # FirestoreRef converted to str
        data = self.firestore_encoder(
            self,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none
        )

        if len(path.split('/')) % 2 != 0:  # were got the path to the collection
            return fs_client.collection(path).add(data)[1].id

        elif overwrite or not fs_client.document(path).get().exists:
            # path contains document and override allowed or document does\'t exists
            fs_client.document(path).set(data)

        else:

            if raise_exists:
                raise e.DocumentExists(path)
            else:
                warn(w.DocumentExists(path))

    @classmethod
    def load_firestore(cls, path: str) -> Firestore:
        '''
        Upload the data from the firestore and make an instance of current class.

        Args:
            path: Path to firestore document.

        Raises:
            DocumentIsnt: If you try to read a document that doesn't exist.

        Returns:
            An instance of skyant.data.entity.google.Firestore object.
        '''

        fs_client = firestore.Client()

        if not fs_client.document(path).get().exists:
            raise e.DocumentIsnt(path)

        data = cls.firestore_decoder(
            fs_client.document(path).get().to_dict()
        )
        cls._validate_schemas(data)

        return cls.parse_obj(data)
