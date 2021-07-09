import logging
import typing as t

import aiohttp

from . import cookiejar, errors

log = logging.getLogger(__name__)


class HTTPClient:
    """Manages the sending of HTTP requests to the AFK Arena CDKey website."""

    _BASE: str = "https://cdkey.lilith.com/api/"

    def __init__(self, player_id: int):
        self.id: int = player_id
        cookie_jar = cookiejar.PersistFileCookieJar(self.id)
        self.http_session: aiohttp.ClientSession = aiohttp.ClientSession(cookie_jar=cookie_jar)

    @property
    def _default_payload(self):
        """Essential payload data to be sent on every POST request."""
        return {"game": "afk", "uid": self.id}

    async def _post(self, endpoint: str, **data):
        """POST Request implementation with dynamic error handling."""
        payload = self._default_payload.copy()
        payload.update(data)
        log.debug(f"POST /{endpoint}:\nPayload={payload}")

        async with self.http_session.post(f"{self._BASE}{endpoint}", json=payload) as resp:
            try:
                data = await resp.json()
            except aiohttp.ContentTypeError:
                content = await resp.text()
                log.exception(f"Response content not able to be parsed as JSON:\n{content}")
                raise

        log.debug(f"POST /{endpoint}:\nPayload={payload}\nResponse={data}")

        if (info := data.get("info")) != "ok":
            exception = errors.RequestError.get_error(info)
            raise exception(info)

        return data.get("data")

    # public api

    async def verify(self, code: int) -> None:
        """Submit Verification Code to authenticate session."""
        await self._post("verify-afk-code", code=f"{code}")

    async def users(self) -> t.List[t.Dict[str, t.Union[int, str, bool]]]:
        """Retrieve available data on a player's linked accounts."""
        data = await self._post("users")
        return data.get("users", [])

    async def redeem_code(self, code: str, player_id: t.Optional[int] = None) -> None:
        """Redeem gift code for a single game account, defaulting to using session ID."""
        await self._post("cd-key/consume", type="cdkey_web", cdkey=code, uid=player_id or self.id)
