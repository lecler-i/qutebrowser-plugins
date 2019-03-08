from PyQt5.QtCore import pyqtSignal, QUrl, QObject
from qutebrowser.browser import urlmarks
from qutebrowser.utils import (message, usertypes, qtutils, urlutils,
                               standarddir, objreg, log)
from qutebrowser.api import cmdutils
import functools
import html
from collections import OrderedDict


class BukuRecordMap(OrderedDict):
    def __init__(self, buku):
        super().__init__(self)
        self.buku = buku

    def _fetch(self):
        self.clear()
        #  self.entries = collections.OrderedDict()
        for entry in self.buku.search_by_tag("qutebrowser,quickmark"):
            self[entry[1]] = entry[2]

    def __getitem__(self, i):
        self._fetch()
        return OrderedDict.__getitem__(self, i)

    def values(self):
        self._fetch()
        return OrderedDict.values(self)

    def items(self):
        self._fetch()
        return OrderedDict.items(self)


class QuickmarkManager(urlmarks.UrlMarkManager):
    def __init__(self, buku, parent=None):
        super().__init__(parent)
        self.buku = buku
        self.marks = BukuRecordMap(self.buku)

    def _init_lineparser(self):
        self._lineparser = []

    def _init_savemanager(self, save_manager):
        pass

    def _parse_line(self, entry):
        pass

    def get(self, name):
        try:
            index = list(self.marks.values()).index(name)
            key = list(self.marks.keys())[index]
        except ValueError:
            raise urlmarks.DoesNotExistError(
                "Quickmark '{}' not found!".format(name))
        return QUrl(key)

    def get_by_qurl(self, url):
        if url.toString() not in self.marks:
            raise urlmarks.DoesNotExistError(
                "Quickmark for '{}' does not exist!".format(name))
        try:
            url = urlutils.fuzzy_url(url, do_search=False)
        except urlutils.InvalidUrlError as e:
            raise urlmarks.InvalidUrlError(
                "Invalid URL for quickmark {}: {}".format(url, str(e)))
        return url

    def delete(self, key):
        record_id = self.buku.get_rec_id(key)
        if record_id is not -1:
            self.buku.delete_rec(record_id)
        else:
            raise urlmarks.DoesNotExistError(
                "Bookmark '{}' does not exist".format(key))

    @cmdutils.register(instance='quickmark-manager')
    def add(self, url, name):
        if not name:
            message.error("Can't set mark with empty name!")
            return
        if not url:
            message.error("Can't set mark with empty URL!")
            return

        def set_mark():
            """Really set the quickmark."""
            self.buku.add_rec(
                url,
                title_in=name,
                tags_in="qutebrowser,quickmark",
                fetch=False)
            log.misc.debug("Added quickmark {} for {}".format(name, url))

        if name in self.marks:
            message.confirm_async(
                title="Override existing quickmark?",
                yes_action=set_mark, default=True, url=url)
        else:
            set_mark()

    def prompt_save(self, url):
        """Prompt for a new quickmark name to be added and add it.

        Args:
            url: The quickmark url as a QUrl.
        """
        if not url.isValid():
            urlutils.invalid_url_error(url, "save quickmark")
            return
        urlstr = url.toString(QUrl.RemovePassword | QUrl.FullyEncoded)
        message.ask_async(
            "Add quickmark:", usertypes.PromptMode.text,
            functools.partial(self.add, urlstr),
            text="Please enter a quickmark name for<br/><b>{}</b>".format(
                html.escape(url.toDisplayString())), url=urlstr)
