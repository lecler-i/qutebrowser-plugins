"""buku integration into qutebrowser."""

import sys
import os

import buku

from qutebrowser.browser import urlmarks
from qutebrowser.utils import log, objreg
from qutebrowser.app import q_app

from .bookmark_manager import BookmarkManager
from .quickmark_manager import QuickmarkManager

bdb = buku.BukuDb()


def init():
    log.extensions.debug("Hooking Buku into Bookmarks...")

    bookmark_manager = BookmarkManager(buku=bdb, parent=q_app)
    objreg.register('bookmark-manager', bookmark_manager, True)

    log.extensions.debug("Hooking Buku into Quickmarks...")
    quickmark_manager = QuickmarkManager(buku=bdb, parent=q_app)
    objreg.register('quickmark-manager', quickmark_manager, True)
