import pathlib
import shutil

import aiohttp

__all__ = ("PersistFileCookieJar",)


class PersistFileCookieJar(aiohttp.CookieJar):
    """Cookie Jar that automatically updates cookie files in order to maintain auth persistance."""

    _SAVE_DIR: pathlib.Path = pathlib.Path.cwd() / "sessions"
    _path_checked = False

    def __init__(self, uid: int, **kwargs):
        if not self._path_checked:
            self.__class__._ensure_dir()
        super().__init__(**kwargs)
        self.uid: int = uid
        if self._file_path.exists():
            self.load(self._file_path)

    @property
    def _file_path(self) -> pathlib.Path:
        """File path for the pickled cookie file to be saved at."""
        return self._SAVE_DIR / f"{self.uid}.session"

    def update_cookies(self, *args, **kwargs) -> None:
        """Save cookie file on any cookie updates."""
        super().update_cookies(*args, **kwargs)
        self._ensure_dir()
        self.save(self._file_path)

    def _do_expiration(self) -> None:
        """Remove cookie file if session expires."""
        super()._do_expiration()
        if len(self._cookies) == 0:
            self._file_path.unlink(missing_ok=True)

    @classmethod
    def _ensure_dir(cls) -> None:
        """Creates the directory cookie files are to be saved if it doesn't exist."""
        if not cls._SAVE_DIR.exists():
            cls._SAVE_DIR.mkdir()
        cls._path_checked = True

    @classmethod
    def set_save_dir(cls, path: pathlib.Path):
        """Set a new directory for cookies to be saved in."""
        cls._SAVE_DIR = path
        cls._ensure_dir()

    @classmethod
    def clear_files(cls):
        """Delete all cookie files."""
        shutil.rmtree(cls._SAVE_DIR, ignore_errors=True)
        cls._ensure_dir()
