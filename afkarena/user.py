from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from .player import Player

__all__ = ("User",)


class User:
    """
    Represents a single in-game User account.

    A single Player can have multiple User accounts linked.
    """

    def __init__(self, data: t.Dict[str, t.Union[str, int, bool]], player: Player):
        self.player = player
        self.name: str = data["name"]
        self.id: int = data["uid"]
        self.server_id: int = data["svr_id"]
        self.level: int = data["level"]
        self.is_main: bool = data.get("is_main", False)

    def __repr__(self) -> str:
        return f"<User {self.name} ({self.id})>"

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

    async def redeem_code(self, code: str) -> None:
        """Redeem a gift code for this user account."""
        await self.player.http.redeem_code(code, self.id)
