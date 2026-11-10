"""Regression tests for saving KDE configuration directories.

The GTK/GNOME glue is stubbed so the pure-Python save path can run without a
desktop session.
"""
import ctypes
import importlib.util
import os
import shutil
import sys
import tempfile
import types
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"

DE_CONFIG = None
_SAVED_MODULES = {}


def _install_stubs():
    names = ("gi", "gi.repository", "savedesktop", "savedesktop.globals")
    for name in names:
        _SAVED_MODULES[name] = sys.modules.get(name)

    gi = types.ModuleType("gi")
    gi_repo = types.ModuleType("gi.repository")

    class GLib:
        class UserDirectory:
            DIRECTORY_DESKTOP = 0

        @staticmethod
        def get_user_special_dir(_which):
            return tempfile.gettempdir()

    gi_repo.GLib = GLib
    gi.repository = gi_repo
    sys.modules["gi"] = gi
    sys.modules["gi.repository"] = gi_repo

    globals_mod = types.ModuleType("savedesktop.globals")
    globals_mod.home = Path.home()
    globals_mod.environment = {"de_name": "KDE Plasma", "dirs": []}
    globals_mod.settings = {}
    savedesktop = types.ModuleType("savedesktop")
    savedesktop.__path__ = [str(SRC)]
    savedesktop.globals = globals_mod
    sys.modules["savedesktop"] = savedesktop
    sys.modules["savedesktop.globals"] = globals_mod


def setUpModule():
    global DE_CONFIG
    _install_stubs()
    spec = importlib.util.spec_from_file_location("de_config", SRC / "core" / "de_config.py")
    DE_CONFIG = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(DE_CONFIG)


def tearDownModule():
    for name, module in _SAVED_MODULES.items():
        if module is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = module


def _lock(path):
    """Keep `path` unreadable until the returned handle is released."""
    if os.name == "nt":
        GENERIC_READ = 0x80000000
        OPEN_EXISTING = 3
        handle = ctypes.windll.kernel32.CreateFileW(
            str(path), GENERIC_READ, 0, None, OPEN_EXISTING, 0x80, None
        )
        if handle == -1:
            raise OSError(f"cannot open {path} with an exclusive lock")
        return handle
    os.chmod(path, 0)
    return None


def _unlock(handle, path):
    if os.name == "nt":
        ctypes.windll.kernel32.CloseHandle(handle)
    else:
        os.chmod(path, 0o600)


@unittest.skipIf(
    os.name != "nt" and hasattr(os, "geteuid") and os.geteuid() == 0,
    "root can read mode-0 files",
)
class KdeConfigDataDirsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="savedesktop-kde-test-"))
        self.home = self.tmp / "home"
        self.config = self.home / ".config"
        self.data = self.home / ".local" / "share"
        self.work = self.tmp / "work"
        self.config.mkdir(parents=True)
        self.data.mkdir(parents=True)
        self.work.mkdir()
        self._handles = []
        self._old_cwd = os.getcwd()
        os.chdir(self.work)
        self._old_home = DE_CONFIG.home
        DE_CONFIG.home = self.home

    def tearDown(self):
        for handle, path in self._handles:
            _unlock(handle, path)
        DE_CONFIG.home = self._old_home
        os.chdir(self._old_cwd)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _lock_file(self, path):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("busy")
        self._handles.append((_lock(path), path))

    def _save(self):
        save = DE_CONFIG.Save.__new__(DE_CONFIG.Save)
        save.save_kde_config_data_dirs()

    def test_unreadable_entry_does_not_abort_save(self):
        (self.config / "kde-readable").mkdir()
        (self.config / "kde-readable" / "appletsrc").write_text("ok")
        (self.config / "kudu").mkdir()
        (self.config / "kudu" / "readable.txt").write_text("fine")
        self._lock_file(self.config / "kudu" / "locked.db")

        self._save()

        self.assertTrue((self.work / "DE/xdg-config/kde-readable/appletsrc").exists())
        self.assertTrue((self.work / "DE/xdg-config/kudu/readable.txt").exists())
        self.assertFalse((self.work / "DE/xdg-config/kudu/locked.db").exists())

    def test_kdeconnect_is_still_skipped(self):
        (self.config / "kdeconnect").mkdir()
        (self.config / "kdeconnect" / "config").write_text("private")

        self._save()

        self.assertFalse((self.work / "DE/xdg-config/kdeconnect").exists())

    def test_missing_source_dirs_are_ignored(self):
        self._save()

        self.assertEqual(list((self.work / "DE/xdg-config").iterdir()), [])


if __name__ == "__main__":
    unittest.main()
