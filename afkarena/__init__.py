"""Simple API wrapper for the AFK Arena site https://cdkey.lilith.com/afk-global."""

import logging

from .player import Player

__all__ = ("Player", "PERSIST_COOKIES")


logging.getLogger(__name__).addHandler(logging.NullHandler())


PERSIST_COOKIES: bool = False
