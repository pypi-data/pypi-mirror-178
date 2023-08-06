# pylint: disable=missing-module-docstring

from abc import ABC
from json import loads
from pathlib import Path

from jsonschema import exceptions as jsonschema_ex
from jsonschema import validate
from pydantic import BaseModel


class SaveLoad(BaseModel, ABC):
    '''
    Abstract class for supporting save & load (serialization and deserialization) in children classes.
    '''

    @classmethod
    @property
    def formats(cls) -> dict:
        '''
        Dict of allowed formats.
        '''

        return {
            'json': ['json'],
            'yaml': ['yaml', 'yml'],
            'avro': ['avro']
        }

    @classmethod
    @property
    def extensions(cls) -> list[str]:
        '''
        List of extensions from all allowed formats.
        '''

        extensions = []
        for allowed_ext in SaveLoad.formats.values():
            extensions.extend(allowed_ext)
        return extensions

    @classmethod
    def _validate_schemas(cls, data: dict) -> None:
        '''
        Verify provided data by JSON schema from pydantic model.

        Args:

        data (dict):
            Data for validation as dictionary object.
        '''

        try:
            validate(data, loads(cls.schema_json()))
        except jsonschema_ex.ValidationError as err:
            raise ValueError(
                # pylint: disable=line-too-long
                f'Data isn\'t valid. Please see schema definition for details. \n Technical details:\n {err.message}'
            ) from err

    @staticmethod
    def _prepare_path(path: str, make_parent: bool = False, lower_suffix: bool = False) -> (str, str, str):
        '''
        Prepares a path for saving file & verify extension.
        This method:
            - verify extension & revert it to lower case (if lower_suffix == True)
            - can create the parent directory (if make == True)

        Args:

        path (str):
            The full path to the file.

        make_parent (bool, optional), default False:
            Flag to make the parent directory with all hyerarchy.

        lower_suffix (bool, optional), default False:
            Flsg to convert file extension to lower case.

        Returns:

        str:
            Path to parent directory.
        str:
            File name.
        str:
            File extension.
        '''

        suffix = SaveLoad._get_suffix(path)

        parent = Path(path).parent
        if make_parent:
            Path(parent).mkdir(parents=True, exist_ok=True)

        filename = path.split('/')[-1].replace(suffix, '')
        suffix = suffix[1:].lower() if lower_suffix else suffix[1:]

        return str(parent), filename, suffix

    @staticmethod
    def _prepare_gcs_uri(path: str, lower_suffix: bool = False) -> (str, str):
        '''
        Prepares a path\'s data for saving file & verify extension.
        This method verify extension & revert it to lower case (if lower_suffix == True)

        Args:

        path (str):
            The full path to the file.

        lower_suffix (bool, optional), default False:
            Flsg to convert file extension to lower case.

        Returns:

        str:
            Bucket name.
        str:
            Full blob name with extension.
        '''

        assert path[:5] == 'gs://', 'The fullname argument have to contains schema "gs://"!'

        suffix = SaveLoad._get_suffix(path)
        bucket = path.split('/')[2]
        filename = path.split('/', 3)[-1].replace(suffix, '')

        # suffix with dot needs to previouse line
        suffix = suffix[1:].lower() if lower_suffix else suffix[1:]

        blob_name = f'{filename}.{suffix}'

        return bucket, blob_name

    @staticmethod
    def _get_suffix(path: str, only_verify: bool = False) -> str | None:
        '''
        Gettin & verifing file extension. This function revert the extension WITH DOT (ex.: .ext)!
        The extension will be got from the path and compared with the values in FORMATS dictionary.

        Args:

        path (str):
            The full path to the file.

        only_verify (bool), default False:
            If True, only verify that the extension is allowed & return None.

        Returns:

        str:
            File extension with dot or None if only_verify == True.
        '''

        suffix = Path(path).suffix
        if suffix[1:].lower() not in SaveLoad.extensions:
            raise ValueError(f'File have to have one extension from: {SaveLoad.formats.keys()}!')
        if not only_verify:
            return suffix

    @staticmethod
    def _get_format(path: str) -> str:
        '''
        Get a typical format by file extension from FORMATS dictionary.
        I the dictionary format is represented as keys.

        Args:

        path (str):
            The full path to the file.

        Returns:

        str:
            Typical file format as lovercase extension string. Example: json, yaml...
        '''

        suffix = SaveLoad._get_suffix(path)
        formats = [k for k, v in SaveLoad.formats.items() if suffix[1:] in v]
        # pylint: disable=line-too-long
        assert len(formats) == 1, f'Extension {suffix} uses more that one format! PLease verify the FORMATS dist!'
        return formats[0]
