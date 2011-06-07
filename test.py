#! /usr/bin/env python
"""Playing with hachoir to parse SQLite files
"""

import os
import sqlite3

from hachoir_core.field import Parser, CString, UInt8, UInt16, UInt32, String, Bytes
from hachoir_core.stream import StringInputStream, BIG_ENDIAN

DATA_FILE = 'example.dat'

class SQLite(Parser):
    """
    Offset	Size	Description
    0	16	 The header string: "SQLite format 3\000"
    16	2	 The database page size in bytes. Must be a power of two between 512 and 32768 inclusive, or the value 1 representing a page size of 65536.
    18	1	 File format write version. 1 for legacy; 2 for WAL.
    19	1	 File format read version. 1 for legacy; 2 for WAL.
    20	1	 Bytes of unused "reserved" space at the end of each page. Usually 0.
    21	1	 Maximum embedded payload fraction. Must be 64.
    22	1	 Minimum embedded payload fraction. Must be 32.
    23	1	 Leaf payload fraction. Must be 32.
    24	4	 File change counter.
    28	4	 Size of the database file in pages. The "in-header database size".
    32	4	 Page number of the first freelist trunk page.
    36	4	 Total number of freelist pages.
    40	4	 The schema cookie.
    44	4	 The schema format number. Supported schema formats are 1, 2, 3, and 4.
    48	4	 Default page cache size.
    52	4	 The page number of the largest root b-tree page when in auto-vacuum or incremental-vacuum modes, or zero otherwise.
    56	4	 The database text encoding. A value of 1 means UTF-8. A value of 2 means UTF-16le. A value of 3 means UTF-16be.
    60	4	 The "user version" as read and set by the user_version pragma.
    64	4	 True (non-zero) for incremental-vacuum mode. False (zero) otherwise.
    68	24	 Reserved for expansion. Must be zero.
    92	4	 The version-valid-for number.
    96	4	SQLITE_VERSION_NUMBER
    """

    endian = BIG_ENDIAN

    def createFields(self):
        yield String(self, 'HeaderString', 16)
        yield UInt16(self, 'PageSize')
        yield UInt8(self, 'WriteVersion')
        yield UInt8(self, 'ReadVersion')
        yield UInt8(self, 'ReservedSpace')
        yield UInt8(self, 'MaxEmbeddedPayloadFraction')
        yield UInt8(self, 'MinEmbeddedPayloadFraction')
        yield UInt8(self, 'LeafPayloadFraction')
        yield UInt32(self, 'FileChangeCounter')
        yield UInt32(self, 'SizeInPages')
        yield UInt32(self, 'FirstFreelistPage')
        yield UInt32(self, 'FreelistTotal')
        yield UInt32(self, 'SchemaCookie')
        yield UInt32(self, 'SchemaFormatNumber')
        yield UInt32(self, 'DefaultPageCacheSize')
        yield UInt32(self, 'MagicPageNumber')
        yield UInt32(self, 'TextEncoding')
        yield UInt32(self, 'UserVersion')
        yield UInt32(self, 'IncrementalVacuumMode')
        yield Bytes(self, 'ReservedForExpansion', 24)
        yield UInt32(self, 'VersionValidFor')
        yield UInt32(self, 'SqliteVersion')

def createFile():
    conn = sqlite3.connect(DATA_FILE)

    c = conn.cursor()

    # Create table
    c.execute('''create table stocks
    (date text, trans text, symbol text,
     qty real, price real)''')

    # Insert a row of data
    c.execute("""insert into stocks
              values ('2006-01-05','BUY','RHAT',100,35.14)""")

    # Save (commit) the changes
    conn.commit()

    # We can also close the cursor if we are done with it
    c.close()

def main():
    if not os.path.exists(DATA_FILE):
        createFile()
    stream = StringInputStream(open(DATA_FILE).read(100))
    root = SQLite(stream)
    for field in root:
      print "%s) %s=%s" % (field.address, field.name, field.display)




if __name__ == '__main__':
    main()


# vim: set tabstop=8 softtabstop=4 shiftwidth=4 expandtab:
