from qutebrowser.browser import urlmarks
import collections


class BukuRecordMap:
    def __init__(self, buku):
        self.entries = collections.OrderedDict()
        self.buku = buku

    def __getitem__(self, i):
        return self.entries[i]

    def items(self):
        self.entries = collections.OrderedDict()
        for entry in self.buku.get_rec_all():
            self.entries[entry[1]] = entry[2]
        return self.entries.items()


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
