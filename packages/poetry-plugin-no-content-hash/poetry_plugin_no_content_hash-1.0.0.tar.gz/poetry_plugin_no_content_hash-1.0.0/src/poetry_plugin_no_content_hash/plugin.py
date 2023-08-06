from typing import TYPE_CHECKING

from poetry.packages import Locker
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry

if TYPE_CHECKING:
    from cleo.io.io import IO


def _get_content_hash(self: Locker):
    return "0" * 64


Locker._get_content_hash = _get_content_hash


class NoContentHashPlugin(Plugin):
    def activate(self, poetry: Poetry, io: "IO"):
        poetry.locker._content_hash = poetry.locker._get_content_hash()
