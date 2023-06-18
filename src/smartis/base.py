import logging
from http import HTTPStatus

from aiohttp import ClientSession, ClientConnectionError, web_exceptions as web_exp
import backoff

from . import messages 

logging.getLogger('backoff').addHandler(logging.StreamHandler())


class SmartisBase:
    """General properties and methods API Smartis."""
    default_domain_name = 'https://my.smartis.bi/api/'
    default_prefix_url = None
    max_time_backoff: int = 60

    def __init__(self, auth_token: str):
        self.auth_token = auth_token

    def get_default_prefix(self):
        if self.default_prefix_url is None:
            raise NotImplementedError(messages.ERROR_PREFIX_UNDEFINED)
        return self.default_prefix_url

    @backoff.on_exception(backoff.expo, 
                          (web_exp.HTTPRequestTimeout, ClientConnectionError),
                          max_time=max_time_backoff)
    async def _http_post(self, session: ClientSession, prefix_method: str,
                         payload: dict | None = None) -> dict:
        """Request post method with JSON body.
        
        - session - opened in aiohttp ClientSession,
        - prefix_method - method API Smartis
        - payload - request data
        """
        prefix_url = self.get_default_prefix()
        async with session.post(
            url=f'{self.default_domain_name}{prefix_url}/{prefix_method}',
            headers={'Authorization': f'Bearer {self.auth_token}'},
            json=payload if payload is not None else None,
        ) as response:
            data = await response.json()
            if response.status == HTTPStatus.OK:
                return data
            raise ValueError(f'{data}')
