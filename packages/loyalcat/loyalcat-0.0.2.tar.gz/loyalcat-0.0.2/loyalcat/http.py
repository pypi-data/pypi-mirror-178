import json
from typing import Any, Generic, Literal, NewType, Self, TypeVar, TypeVarTuple
import aiohttp

from loyalcat.types.endpoints import ENDPOINTS
from loyalcat.utils import insert_params

R = TypeVar('R')


class Route:
    def __init__(
        self,
        method: Literal['GET', 'POST'],
        path: ENDPOINTS,
        params: dict[str, Any] | None = None,
    ):
        self.path: str = insert_params(path, params) if params else path
        self.method: str = method


async def json_or_text(response: aiohttp.ClientResponse):
    text = await response.text(encoding='utf-8')

    try:
        if 'application/json' in response.headers['Content-Type']:
            return json.loads(text)
    except KeyError:
        pass


class HttpClient:
    def __init__(self) -> None:
        self.session: aiohttp.ClientSession
        self.url = 'https://loyalcat.akarinext.org'

    def create_session(self) -> Self:
        self.session = aiohttp.ClientSession(
            headers={'Content-type': 'application/json'},
        )
        return self

    async def request(self, route: Route, body: dict[str, Any] | None = None) -> R:
        async with self.session.request(
            route.method, self.url + route.path, json=body
        ) as res:
            data = await json_or_text(res)
            if 300 > res.status >= 200:
                return data  # type: ignore
            else:
                raise Exception(data, res.status)

