'''
The module provides objects for sending and/or receiving data to REST interfaces. Thanks to this object
you can fast & simple communicate with the endpoint. All objects skyant.data.entity.* are inherited from
pydantic, so you can use the same BaseModel as API endpoint definition so and as client-side interface.

This solution makes the process of creating a Client-Server application more effective and minimizes
a debugging time.

General:
    The class General provides methods for interacting with any REST API endpoint.

    [_skyant.data.entity.rest.General references_](references/rest/General.md)
'''

from ._general import Rest as General
