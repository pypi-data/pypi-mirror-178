# pylint: disable=missing-docstring

from __future__ import annotations

import requests

from ...tools.file import SaveLoad


__all__ = [
    'Rest'
]


def prep_header(user_header: dict) -> dict:
    '''
    Function prepare the header for sent a request.

    Args:

        user_header (dict): User provided headers as a dictionary.

    Returns:

        dict: Prepared header.
    '''

    return user_header.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    })


class Rest(SaveLoad):
    '''
    Class for interacting with REST endpoint.

    Class contains "send_\\*" methods of instance for sending a data & methods of class "load_\\*"
    for get data and make instance.
    '''

    def send_post(
        self,
        url: str,
        headers: dict = None,
        query: dict = None,
        cookies: dict = None,
        auth: tuple = None,
        exclude_none: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        by_alias: bool = True,
        timeout: int = 10,
        json_only: bool = True,
        **kw
    ) -> requests.Response | dict:
        '''
        Send the data as a body of POST request.

        Args:

            url (str): Valid URL (schema://host:port/path) for sending request to.

                For example: https://skyant.dev/something/path

            headers (dict, optional): (dict, optional): HTTP headers for attaching to a POST request.

                Please be sure that headers "Accept" & "Content-Type" will be attached automatically.

            query (dict, optional): A query string for request url as a dictionary.

            cookies (dict, optional): Cookies for attaching to the request.

            auth (tuple, optional): Authentication tokens.

            exclude_none (bool, optional): Defines what does needs do with empty entity in data.

            exclude_unset (bool, optional): Defines what does needs do with entity in data
                which value is default value.

            by_alias: Flag for using alias instead of python name of entity; by default FastAPI uses alias.

            exclude_defaults: Ignore fields if value is equal default.

        Returns:
            Response object.
        '''

        full_header = prep_header(headers)

        resp = requests.post(
            url,
            data=self.dict(
                exclude_unset=exclude_unset,
                exclude_none=exclude_none,
                exclude_defaults=exclude_defaults,
                by_alias=by_alias
            ),
            headers=full_header,
            params=query,
            cookies=cookies,
            auth=auth,
            timeout=timeout,
            **kw
        )

        return resp.json if json_only else resp

    @classmethod
    def load_get(
        cls,
        url: str,
        headers: dict = None,
        query: dict = None,
        cookies: dict = None,
        auth: tuple = None,
        timeout: int = 10,
        **kw
    ) -> Rest | None:
        '''
        Class method which send a GET request to a server and make a instances of class from respond.

        Args:

            url (str): Valid URL (schema://host:port/path) for sending request to.

                For example: https://skyant.dev/something/path

            headers (dict, optional): HTTP headers for attaching to a POST request.

                Please be sure that headers "Accept" & "Content-Type" will be attached automatically.

            query (dict, optional): A query string for request url as a dictionary.

            cookies (dict, optional): Cookies for attaching to the request.

            auth (tuple, optional): Authentication tokens.

        Returns:

            An instance of pydantic.BaseModel what was made from a received data or None
                if respond is Empty.
        '''

        full_header = prep_header(headers)

        data = requests.get(
            url, headers=full_header, params=query, cookies=cookies, auth=auth, timeout=timeout, **kw
        ).json()
        cls._validate_schemas(data)

        return cls.parse_obj(data)

    @classmethod
    def load_post(
        cls,
        url: str,
        data: dict = None,
        headers: dict = None,
        query: dict = None,
        cookies: dict = None,
        auth: tuple = None,
        timeout: int = 10,
        **kw
    ) -> Rest | None:
        '''
        Class method which send a POST request to a server and make a instance of class from respond.

        Args:

            url (str): Valid URL (schema://host:port/path) for sending request to.

                For example: https://skyant.dev/something/path

            data (dict, optional): Dictionary for sending as a body to the url.

            headers (dict, optional): HTTP headers for attaching to a POST request.

                Please be sure that headers "Accept" & "Content-Type" will be attached automatically.

            query (dict, optional): A query string for request url as a dictionary.

            cookies (dict, optional): Cookies for attaching to the request.

            auth (tuple, optional): Authentication tokens.

        Returns:
            An instance of pydantic.BaseModel what was made from a received data or None
                if respond is Empty.
        '''

        full_header = prep_header(headers)

        data = requests.post(
            url,
            data=data,
            headers=full_header,
            params=query,
            cookies=cookies,
            auth=auth,
            timeout=timeout,
            **kw
        ).json()
        cls._validate_schemas(data)

        return cls.parse_obj(data)
