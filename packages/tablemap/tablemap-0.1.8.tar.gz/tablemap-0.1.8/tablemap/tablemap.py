# -*- coding: utf-8 -*-
"""A data wrangling tool which requires no knowledge of Pandas or SQL.
"""


import os
import signal
import sqlite3
import tempfile
from contextlib import contextmanager
from inspect import isgeneratorfunction
from itertools import chain, groupby
from pathlib import Path, PurePath


@contextmanager
def _connect(db):
    conn = sqlite3.connect(db)
    conn.row_factory = _dict_factory
    try:
        yield conn
    finally:
        # If users enter ctrl-c during the database commit,
        # db might be corrupted. (won't work anymore)
        with _delayed_keyboard_interrupts():
            conn.commit()
            conn.close()


@contextmanager
def _delayed_keyboard_interrupts():
    signal_received = []

    def handler(sig, frame):
        nonlocal signal_received
        signal_received = (sig, frame)
    # Do nothing but recording something has happened.
    old_handler = signal.signal(signal.SIGINT, handler)

    try:
        yield
    finally:
        # signal handler back to the original one.
        signal.signal(signal.SIGINT, old_handler)
        if signal_received:
            # do the delayed work
            old_handler(*signal_received)


class _InstructionContainer:
    """Holds instructions to modify a table by chaining methods,
    'map', 'by', 'merge' and 'concat'.

    This is a private class. Instead of directly creating an instance of
    this class, use Conn.__getitem__
    """

    def __init__(self, conn, tname):
        self._conn = conn
        self._insts = [{
            'cmd': 'fetch',
            'tname': tname
        }]

    def map(self, fn):
        self._insts.append({
            'cmd': 'map',
            'fn': fn
        })
        return self

    def by(self, *cols):
        self._insts.append({
            'cmd': 'by',
            'cols': cols
        })
        return self

    def merge(self, fn, other):
        self._insts.append({
            'cmd': 'merge',
            'fn': fn,
            'other': other
        })
        return self

    def concat(self, other):
        self._insts.append({
            'cmd': 'concat',
            'other': other
        })
        return self

    def iter(self):
        insts = self._insts
        # If the second instruction is 'by', combine it with the first
        # so the length of the instructions will be decreased by 1
        if len(insts) >= 2 and insts[0]['cmd'] == 'fetch'\
                and insts[1]['cmd'] == 'by':
            # as long as cmd str contains 'by', whatever naming is fine.
            insts[0]['cmd'] = 'fetch_by'
            insts[0]['cols'] = insts[1]['cols']
            insts = [insts[0]] + insts[2:]

        tname = insts[0]['tname']
        cols = insts[0].get('cols', None)

        def initgen():
            try:
                yield from _fetch(self._conn._dbconn, tname, cols)
            # in case self._conn._dbconn is either None or closed connection
            except (AttributeError, sqlite3.ProgrammingError):
                with _connect(self._conn._dbfile) as c:
                    self._conn._dbconn = c
                    yield from _fetch(c, tname, cols)

        # Stack of generator functions (generators)
        # Each generator hinges on the previous one.
        genfns = [initgen]

        for pinst, inst in zip(insts, insts[1:]):
            # Scan through the instructions and stack up 'genfns'
            # with generators
            if inst['cmd'] == 'map':

                def buildgen(pinst, inst):
                    fn = _fn2gen(inst['fn'])
                    pgen = genfns[-1]

                    def gen1():
                        for r in pgen():
                            yield from fn(r)

                    def gen2():
                        for _, rs in pgen():
                            yield from fn(list(rs))

                    return gen2 if 'by' in pinst['cmd'] else gen1

                genfns.append(buildgen(pinst, inst))

            elif inst['cmd'] == 'by':

                def buildgen(inst):
                    cols = inst['cols']
                    pgen = genfns[-1]

                    def gen():
                        try:
                            tmpdbfd, tmpdb = tempfile.mkstemp()
                            with _connect(tmpdb) as c:
                                _insert(c, 'temp', pgen())
                                yield from _fetch(c, 'temp', cols)
                        finally:
                            # must close the file descriptor to delete it
                            os.close(tmpdbfd)
                            if Path(tmpdb).is_file():
                                os.remove(tmpdb)
                    return gen

                genfns.append(buildgen(inst))

            elif inst['cmd'] == 'merge':
                if not 'by' in pinst['cmd']:
                    raise ValueError("Must be grouped by columns before merge")

                def buildgen(inst):
                    fn = _fn2gen(inst['fn'])
                    pgen = genfns[-1]

                    def gen():
                        yield from _step(fn, pgen(), _inst2iter(inst['other']))

                    return gen

                genfns.append(buildgen(inst))

            elif inst['cmd'] == 'concat':

                def buildgen(inst):
                    pgen = genfns[-1]

                    def gen():
                        for r in pgen():
                            yield r
                        for r in _inst2iter(inst['other']):
                            yield r
                    return gen

                genfns.append(buildgen(inst))

        yield from genfns[-1]()

    def list(self):
        return list(self.iter())


class Conn:
    """Connection to a SQL database file.

    Example:
        conn = Conn('sample.db')
    """

    def __init__(self, dbfile):
        # dbfile must be a filename(str), can't be :memory:
        if PurePath(dbfile).is_absolute():
            self._dbfile = dbfile
        else:
            self._dbfile = os.path.join(os.getcwd(), dbfile)

        self._dbconn = None

    def __getitem__(self, tname):
        return _InstructionContainer(self, tname)

    def __setitem__(self, tname, val):
        with _connect(self._dbfile) as c:
            self._dbconn = c
            _delete(c, tname)
            _insert(c, tname, _inst2iter(val))


def _insert_statement(name, d):
    """insert into foo values (:a, :b, :c, ...)

    Notice the colons.
    """
    keycols = ', '.join(":" + c.strip() for c in d)
    return "insert into %s values (%s)" % (name, keycols)


def _create_statement(tname, cols):
    """Create table if not exists foo (...)

    Note:
        Every type is numeric.
    """
    schema = ', '.join([col + ' ' + 'numeric' for col in cols])
    return "create table if not exists %s (%s)" % (tname, schema)


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def _keyfn(cols):
    if len(cols) == 1:
        col = cols[0]
        return lambda r: r[col]
    return lambda r: [r[col] for col in cols]


def _delete(c, tname):
    c.cursor().execute(f'drop table if exists {tname}')


def _insert(c, tname, rs):
    rs = iter(rs)
    try:
        r0 = next(rs)
    except StopIteration:
        raise ValueError(f"No row to insert in {tname}") from None
    else:
        cols = list(r0)

        c.cursor().execute(_create_statement(tname, cols))
        istmt = _insert_statement(tname, r0)
        c.cursor().executemany(istmt, chain([r0], rs))


def _fetch(c, tname, cols):
    if cols:
        query = f"select * from {tname} order by {','.join(cols)}"
        yield from groupby(c.cursor().execute(query), _keyfn(cols))
    else:
        query = f"select * from {tname}"
        yield from c.cursor().execute(query)


# ordinary function to generator function
def _fn2gen(f):
    def gen(*r):
        x = f(*r)
        if isinstance(x, dict):
            yield x
        elif x is not None:
            yield from x

    return f if isgeneratorfunction(f) else gen


def _step(fn, krs1, krs2):
    empty = object()
    try:
        k1, rs1 = next(krs1)
        k2, rs2 = next(krs2)
        while True:
            if k1 == k2:
                yield from fn(list(rs1), list(rs2))
                k1 = k2 = empty
                k1, rs1 = next(krs1)
                k2, rs2 = next(krs2)
            elif k1 < k2:
                yield from fn(list(rs1), [])
                k1 = empty
                k1, rs1 = next(krs1)
            else:
                yield from fn([], list(rs2))
                k2 = empty
                k2, rs2 = next(krs2)
    except StopIteration:
        # unconsumed
        if k1 is not empty:
            yield from fn(list(rs1), [])
        if k2 is not empty:
            yield from fn([], list(rs2))

        for _, rs1 in krs1:
            yield from fn(list(rs1), [])
        for _, rs2 in krs2:
            yield from fn([], list(rs2))


def _inst2iter(obj):
    return obj.iter() if isinstance(obj, _InstructionContainer) else iter(obj)
