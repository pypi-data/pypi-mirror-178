# pylint: disable=missing-docstring

from __future__ import annotations

import json
from enum import Enum

import yaml
from google.cloud import storage as gcs

from ...tools.file import SaveLoad
from ...tools.json import StringEncoder
from ...tools.e import UnknownType


class StorageClass(Enum):
    STANDARD = 'STANDARD'
    NEARLINE = 'NEARLINE'
    COLDLINE = 'COLDLINE'
    ARCHIVE = 'ARCHIVE'


class Blob(SaveLoad):
    '''
    Saving & loading files to/from [Google Cloud Storage](https://cloud.google.com/storage).
    '''

    @classmethod
    @property
    def GCSClass(cls) -> StorageClass:  # pylint: disable=invalid-name
        '''
        Enumerator of possibles Google Cloud Storage "Storage Classes", such as "standard",
            "archive", etc.

        [Origin documentation](https://cloud.google.com/storage/docs/storage-classes)
        '''

        return StorageClass

    def save_gcs(
        self,
        fullname: str,
        storage_class: StorageClass = StorageClass.STANDARD,
        ensure_ascii: bool = True,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False
    ) -> None:
        '''
        Save data to Google Cloud Storage. This method supports:
        - json
        - yaml

        Args:

            fullname: Full file name include bucket name & extension.

            storage_class: Google Storage Class to assign to file.

            encoding: File encoding.

            ensure_ascii: Keep or not non-ASCII characters.

            exclude_none: Keep or pass empty values. If True, file will be contains "NaN" values.

            exclude_unset: Write or ignore default values. If False default values won't be written.

        Raises:
            NotImplementedError: AVRO does not support now!
            UnknownType: Unknown file type!
        '''

        bucket_name, blob_name = self._prepare_gcs_uri(fullname)
        file_format = self._get_format(fullname)

        bucket = gcs.Client().get_bucket(bucket_name)
        data_src = self.dict(
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
            by_alias=by_alias
        )

        if file_format == 'json':

            data = json.dumps(
                data_src,
                ensure_ascii=ensure_ascii,
                cls=StringEncoder
            )
            content_type = 'application/json'

        elif file_format == 'yaml':
            data = yaml.dump(
                data_src,
                default_flow_style=False,
                allow_unicode=not ensure_ascii
            )
            content_type = 'application/yaml'

        elif file_format == 'avro':
            # TODO: Implement a procedure for saving avro file to Google Cloud Storage.
            raise NotImplementedError('AVRO doesn\'t support now!')

        else:
            raise UnknownType(blob_name)

        blob = bucket.blob(blob_name)
        blob.upload_from_string(data, content_type=content_type)
        blob.update_storage_class(storage_class.value)

    @classmethod
    def load_gcs(cls, fullname: str) -> Blob:
        '''
        Load the data from Google Cloud Storage. Function reads JSON & YAML files.

        Args:

            fullname: Full file name include bucket name & extension.

            encoding: File encoding.

        Raises:
            NotImplementedError: AVRO does not support now!
            UnknownType: Unknown file type!

        Returns:
            The instance of this class.
        '''

        bucket_name, blob_name = cls._prepare_gcs_uri(fullname)
        file_format = cls._get_format(fullname)

        bucket = gcs.Client().get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        if file_format == 'json':
            data = json.loads(blob.download_as_text())

        elif file_format == 'yaml':
            data = yaml.safe_load(blob.download_as_text())

        elif file_format == 'avro':
            # TODO: Implement a procedure for loading avro file from Google Cloud Storage.
            raise NotImplementedError('AVRO doesn\'t support now!')

        else:
            raise UnknownType(blob_name)

        cls._validate_schemas(data)

        return cls.parse_obj(data)
