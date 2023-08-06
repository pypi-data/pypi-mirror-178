#!/usr/bin/env python3
# Copyright © 2022 Mark Summerfield. All rights reserved.
# License: GPLv3

'''
A library supporting Tdb “Text DataBase” format.

Tdb “Text DataBase” format is a plain text human readable typed database
storage format.

Tdb provides a superior alternative to CSV. In particular, Tdb tables are
named and Tdb fields are strictly typed. Also, there is a clear distinction
between field names and data values, and strings respect whitespace
(including newlines) and have no problems with commas, quotes, etc.
Perhaps best of all, a single Tdb file may contain one—or more—tables.
'''

import datetime
import gzip
import io
import math
import pathlib
from xml.sax.saxutils import escape, unescape

import editabletuple

__version__ = '0.5.1'

DATE_SENTINAL = datetime.date(1808, 8, 8)
DATETIME_SENTINAL = datetime.datetime(1808, 8, 8, 8, 8, 8)
INT_SENTINAL = -1808080808
REAL_SENTINAL = -1808080808.0808


class Tdb:

    def __init__(self):
        self.tables = {}


    def load(self, filename_or_filelike):
        '''Reads the given file (or file-like stream) and replaces this
        Tdb's tables with those read in.'''
        close = False
        if isinstance(filename_or_filelike, (str, pathlib.Path)):
            filename_or_filelike = str(filename_or_filelike)
            opener = (gzip.open
                      if filename_or_filelike[-3:].lower().endswith('.gz')
                      else open)
            out = opener(filename_or_filelike, 'rt', encoding='utf-8')
            close = True
        else:
            out = filename_or_filelike
        try:
            self.loads(out.read())
        finally:
            if close:
                out.close()


    def loads(self, text):
        '''Reads the given text and replaces this Tdb's tables with those
        read in.'''
        self.tables = _read_tdb(text)


    def dump(self, filename_or_filelike, *, decimals=-1):
        '''Writes this Tdb's tables to the given file (or file-like
        stream).'''
        if not (1 <= decimals <= 19):
            decimals = -1
        close = False
        if isinstance(filename_or_filelike, (str, pathlib.Path)):
            filename_or_filelike = str(filename_or_filelike)
            if filename_or_filelike == '-':
                out = sys.stdout
            else:
                opener = (
                    gzip.open
                    if filename_or_filelike[-3:].lower().endswith('.gz')
                    else open)
                out = opener(filename_or_filelike, 'wt', encoding='utf-8')
            close = True
        else:
            out = filename_or_filelike
        try:
            _write_tdb(out, self.tables, decimals)
        finally:
            if close:
                out.close()


    def dumps(self, *, decimals=-1):
        '''Writes this Tdb's tables to a string which is then returned.'''
        out = io.StringIO()
        try:
            self.dump(out, decimals)
            return out.getvalue()
        finally:
            out.close()


def load(filename_or_filelike):
    '''Reads the given file (or file-like stream) and returns a Tdb with the
    tables that have been read in.'''
    db = Tdb()
    db.load(filename_or_filelike)
    return db


def loads(text):
    '''Reads the given text and returns a Tdb with the tables that have been
    read in.'''
    db = Tdb()
    db.loads(text)
    return db


def _read_tdb(text):
    tables = {}
    table = None
    lino = 1
    while text:
        c = text[0]
        if c == '\n':
            lino += 1
            text = text[1:]
        elif c == '[':
            text, table, lino = _read_meta(text[1:], lino)
            tables[table.name] = table
        else: # read records into the current table
            text, lino = _read_records(text, table, lino)
    return tables


def _read_meta(text, lino):
    found, text, lino = _find(text, '%', 'expected to find "%"', lino)
    table = Table()
    field_name = None
    for i, part in enumerate(found.split()):
        if i == 0:
            table.name = part
        elif i % 2 != 0:
            field_name = part
        else:
            table.fields_meta.append(MetaField(field_name, part))
    return text, table, lino + 1 # allow for %


def _read_records(text, table, lino):
    record = None
    old_column = -1
    column = 0
    columns = table.columns
    while text:
        if record is None:
            record = table.RecordClass()
            old_column = -1
            column = 0
        if column != old_column:
            kind = table.fields_meta[column].kind
        c = text[0]
        if c == '\n': # ignore whitespace
            text = text[1:]
            lino += 1
        elif c in ' \t\r': # ignore whitespace
            text = text[1:]
        elif c == '!':
            _handle_sentinel(kind, record, column, lino)
            text, column = _advance(text, column)
        elif c in 'FfNn':
            _handle_bool(kind, False, record, column, lino)
            text, column = _advance(text, column)
        elif c in 'TtYy':
            _handle_bool(kind, True, record, column, lino)
            text, column = _advance(text, column)
        elif c == '(':
            text, lino = _handle_bytes(kind, text[1:], record, column, lino)
            column += 1
        elif c == '<':
            text, lino = _handle_str(kind, text[1:], record, column, lino)
            column += 1
        elif c == '-':
            if kind == 'int':
                text, lino = _handle_int(text, record, column, lino)
            elif kind == 'real':
                text, lino = _handle_real(text, record, column, lino)
            else:
                raise Error(f'{lino}#expected an {kind}')
            column += 1
        elif c in '0123456789':
            if kind == 'int':
                text, lino = _handle_int(text, record, column, lino)
            elif kind == 'real':
                text, lino = _handle_real(text, record, column, lino)
            elif kind == 'date':
                text, lino = _handle_date(text, record, column, lino)
            elif kind == 'datetime':
                text, lino = _handle_datetime(text, record, column, lino)
            else:
                raise Error(f'{lino}#expected an {kind}')
            column += 1
        elif c == ']': # end of table
            if 0 < column < columns:
                raise Error(f'{lino}#incomplete record {column + 1}/'
                            f'{columns} fields')
            return _skip_ws(text[1:], lino)
        else:
            raise Error(f'{lino}#invalid character {c!r}')
        if column == columns:
            table.append(record)
            record = None
    return text, lino


def _advance(text, column):
    return text[1:], column + 1


def _handle_sentinel(kind, record, column, lino):
    if kind == 'date':
        record[column] = DATE_SENTINAL
    elif kind == 'datetime':
        record[column] = DATETIME_SENTINAL
    elif kind == 'int':
        record[column] = INT_SENTINAL
    elif kind == 'real':
        record[column] = REAL_SENTINAL
    else:
        raise Error(f'{lino}#{kind} fields don\'t allow sentinals')


def _handle_bool(kind, value, record, column, lino):
    if kind != 'bool':
        raise Error(f'{lino}#expected type {kind}, got a bool')
    record[column] = value


def _handle_bytes(kind, text, record, column, lino):
    if kind != 'bytes':
        raise Error(f'{lino}#expected type {kind}, got a bytes')
    found, text, lino = _find(text, ')', 'expected to find ")"', lino)
    record[column] = bytes.fromhex(found)
    return text, lino # skip )


def _handle_str(kind, text, record, column, lino):
    if kind != 'str':
        raise Error(f'{lino}#expected type {kind}, got a str')
    found, text, lino = _find(text, '>', 'expected to find ">"', lino)
    record[column] = unescape(found)
    return text, lino # skip >


def _handle_int(text, record, column, lino):
    text, found, lino = _scan(text, '-+0123456789', lino)
    try:
        record[column] = int(found)
        return text, lino
    except ValueError as err:
        raise Error(f'{lino}#invalid int: {found!r}: {err}')


def _handle_real(text, record, column, lino):
    text, found, lino = _scan(text, '-+0123456789.eE', lino)
    try:
        record[column] = float(found)
        return text, lino
    except ValueError as err:
        raise Error(f'{lino}#invalid real: {found!r}: {err}')


def _handle_date(text, record, column, lino):
    text, found, lino = _scan(text, '-0123456789', lino)
    try:
        record[column] = datetime.date.fromisoformat(found)
        return text, lino
    except ValueError as err:
        raise Error(f'{lino}#invalid date: {found!r}: {err}')


def _handle_datetime(text, record, column, lino):
    text, found, lino = _scan(text, '-0123456789T:', lino)
    try:
        record[column] = datetime.datetime.fromisoformat(found)
        return text, lino
    except ValueError as err:
        raise Error(f'{lino}#invalid datetime: {found!r}: {err}')


def _scan(text, valid, lino):
    text, lino = _skip_ws(text, lino)
    end = 0
    while end < len(text):
        c = text[end]
        if c not in valid:
            return text[end:], text[:end], lino
        end += 1
    raise Error(f'{lino}#unexpected end of data')


def _skip_ws(text, lino):
    end = 0
    while end < len(text):
        c = text[end]
        if c == '\n':
            lino += 1
        if c.isspace():
            end += 1
            continue
        return text[end:], lino
    return text, lino


def _find(text, what, message, lino):
    end = text.find(what)
    if end == -1:
        raise Error(f'{lino}#{message}')
    lino += text[:end].count('\n')
    return text[:end], text[end + 1:], lino


def _write_tdb(out, tables, decimals):
    for table_name, table in tables.items():
        out.write(f'[{table_name}')
        for meta in table.fields_meta:
            out.write(f' {meta.name} {meta.kind}')
        out.write('\n%\n')
        for record in table.records:
            sep = ''
            for column, value in enumerate(record):
                out.write(sep)
                sep = ' '
                kind = table.fields_meta[column].kind
                if kind == 'bool':
                    out.write('T' if value else 'F')
                elif kind == 'bytes':
                    out.write(f'({value.hex()})')
                elif kind == 'date':
                    if value == DATE_SENTINAL:
                        out.write('!')
                    else:
                        out.write(value.isoformat())
                elif kind == 'datetime':
                    if value == DATETIME_SENTINAL:
                        out.write('!')
                    else:
                        out.write(value.isoformat()[:19])
                elif kind == 'int':
                    if value == INT_SENTINAL:
                        out.write('!')
                    else:
                        out.write(str(value))
                elif kind == 'real':
                    if math.isclose(value, REAL_SENTINAL):
                        out.write('!')
                    elif decimals <= 0:
                        out.write(f'{value:g}')
                    else:
                        out.write(f'{value:.{decimals}f}')
                else: # str
                    out.write(f'<{escape(value)}>')
            out.write('\n')
        out.write(']\n')


class MetaField:

    def __init__(self, name, kind):
        self.name = name
        self.kind = kind


    def __repr__(self):
        return f'{self.__class__.__name__}({self.name!r}, {self.kind!r})'


class Table:

    def __init__(self):
        self.name = None
        self.fields_meta = []
        self.records = []
        self._RecordClass = None


    @property
    def RecordClass(self):
        if self._RecordClass is None:
            self._RecordClass = editabletuple.editabletuple(
                self.name, *[field.name for field in self.fields_meta])
        return self._RecordClass


    @property
    def columns(self):
        return len(self.fields_meta)


    def append(self, record):
        self.records.append(record)


    def __repr__(self):
        meta = '\n  '.join((str(m) for m in self.fields_meta))
        return f'{self.__class__.__name__}({self.name!r})\n  ' + meta


class Error(Exception):
    pass


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
        raise SystemExit('usage: tdb.py <infile.tdb> [outfile.tdb]')
    infile = sys.argv[1]
    outfile = '-' if len(sys.argv) == 2 else sys.argv[2]
    db = load(infile)
    db.dump(outfile)
