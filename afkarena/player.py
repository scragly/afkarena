from __future__ import annotations

import typing as t
from collections import defaultdict

from aiohttp import CookieJar

from . import errors, http
from .user import User

__all__ = ("Player",)


class Player:
    """
    Represents a Player.

    A Player can have multiple in-game Users linked to their account.
    """

    def __init__(self, uid: int, *, cookie_jar: t.Optional[CookieJar] = None):
        self.id: int = uid
        self.http = http.HTTPClient(uid, cookie_jar=cookie_jar)
        self.users: t.Optional[t.Dict[int, User]] = None
        self.main: t.Optional[User] = None
        self.authenticated: bool = False

    def __repr__(self) -> str:
        if self.users is None:
            linked = "UNVERIFIED"
        elif (count := len(self.users)) == 1:
            linked = f"{count} user"
        else:
            linked = f"{count} users"
        return f"<Player {self.id} ({linked})>"

    def __str__(self) -> str:
        name = self.users[self.id].name if self.users else "Unverified Player"
        return f"{name} ({self.id})"

    async def verify(self, auth_code: int):
        """Verify user account using in-game authentication code."""
        await self.http.verify(auth_code)
        self.authenticated = True
        return self

    async def get_user(self, uid: int):
        """Get a specific user account linked to this Player."""
        if self.users is None:
            await self.fetch_users()

        try:
            return self.users.get(uid)
        except errors.AuthExpired:
            self.authenticated = False
            raise

    async def fetch_users(self) -> t.Set[User]:
        """Retrieve all linked User accounts."""
        try:
            data = await self.http.users()
        except errors.AuthExpired:
            self.authenticated = False
            raise

        users = set()
        for user_data in data:
            user = User(user_data, self)
            users.add(user)
            if self.users is None:
                self.users = dict()
            self.users[user.id] = user
            if user.is_main:
                self.main = user

        return users

    async def redeem_codes(self, *codes: str) -> t.Dict[str, t.Union[t.List[str], t.DefaultDict[User, str]]]:
        """Redeem multiple gift codes for all linked User accounts."""
        if not self.authenticated:
            await self.fetch_users()

        invalid_codes = []
        expired_codes = []
        used_codes = defaultdict(list)
        successful_codes = defaultdict(list)

        for user in self.users.values():
            for code in codes:
                if code in invalid_codes or code in expired_codes:
                    continue
                try:
                    await user.redeem_code(code)
                except errors.CodeInvalid:
                    invalid_codes.append(code)
                except errors.CodeExpired:
                    expired_codes.append(code)
                except errors.CodeUsed:
                    used_codes[user].append(code)
                else:
                    successful_codes[user].append(code)

        return {
            "invalid": invalid_codes,
            "expired": expired_codes,
            "used": used_codes,
            "success": successful_codes,
        }
