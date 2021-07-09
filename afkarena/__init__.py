"""Simple API wrapper for the AFK Arena site https://cdkey.lilith.com/afk-global."""

import logging

from .player import Player


__all__ = ("Player",)


logging.getLogger(__name__).addHandler(logging.NullHandler())
