from qutebrowser.browser import urlmarks
from collections import OrderedDict


class BukuRecordMap(OrderedDict):
    def __init__(self, buku):
        super().__init__(self)
        self.buku = buku

    def _fetch(self):
        self.clear()
        for entry in self.buku.get_rec_all():
            self[entry[1]] = entry[2]

    def __getitem__(self, i):
        self._fetch()
        return OrderedDict.__getitem__(self, i)

    def items(self):
        self._fetch()
        return OrderedDict.items(self)


class BookmarkManager(urlmarks.UrlMarkManager):
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

    def delete(self, key):
        record_id = self.buku.get_rec_id(key)
        if record_id is not -1:
            self.buku.delete_rec(record_id)
        else:
            raise urlmarks.DoesNotExistError(
                "Bookmark '{}' does not exist".format(key))

    def add(self, url, title, *, toggle=False):
        if not url.isValid():
            errstr = urlutils.get_errstring(url)
            raise urlmakrks.InvalidUrlError(errstr)
        # TODO Should escape the url

        self.buku.add_rec(
            url.toString(),
            title_in=title,
            tags_in="qutebrowser",
            fetch=False)
        return True
