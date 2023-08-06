#!/usr/bin/env python3
#
# Bookmark management utility
#
# Copyright (C) 2015-2016 Arun Prakash Jana <engineerarun@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with buku.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import sqlite3
import re
import argparse
import webbrowser
import html.parser as HTMLParser
from http.client import HTTPConnection, HTTPSConnection
from urllib.parse import urljoin, quote, unquote
import gzip
import signal
import logging
import inspect
import atexit
import readline

# Globals
update = False          # Update a bookmark in DB
tagManual = None        # Tags for update command
titleManual = None      # Manually add a title offline
description = None      # Description of the bookmark
tagsearch = False       # Search bookmarks by tag
titleData = None        # Title fetched from a webpage
interrupted = False     # Received SIGINT
DELIMITER = ','         # Delimiter used to store tags in DB
_VERSION_ = '2.4'       # Program version

# Crypto globals
BLOCKSIZE = 65536
SALT_SIZE = 32
CHUNKSIZE = 0x80000     # Read/write 512 KB chunks

# Set up logging
logging.basicConfig(format='[%(levelname)s] %(message)s')
logger = logging.getLogger()


class BMHTMLParser(HTMLParser.HTMLParser):
    '''Class to parse and fetch the title from a HTML page, if available'''

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.inTitle = False
        self.data = ''
        self.lasttag = None

    def handle_starttag(self, tag, attrs):
        self.inTitle = False
        if tag == 'title':
            self.inTitle = True
            self.lasttag = tag

    def handle_endtag(self, tag):
        global titleData

        if tag == 'title':
            self.inTitle = False
            if self.data != '':
                titleData = self.data
                self.reset()  # We have received title data, exit parsing

    def handle_data(self, data):
        if self.lasttag == 'title' and self.inTitle:
            self.data = '%s%s' % (self.data, data)

    def error(self, message):
        pass


class BukuCrypt:
    ''' Class to handle encryption and decryption
    of the database file. Functionally a separate entity.

    Involves late imports in the static functions but it
    saves ~100ms each time. Given that encrypt/decrypt are
    not done automatically and any one should be called at
    a time, this doesn't seem to be an outrageous approach.
    '''

    @staticmethod
    def get_filehash(filepath):
        '''Get the SHA256 hash of a file

        Params: path to the file
        '''

        from hashlib import sha256

        with open(filepath, 'rb') as f:
            hasher = sha256()
            buf = f.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(BLOCKSIZE)

            return hasher.digest()

    @staticmethod
    def encrypt_file(iterations):
        '''Encrypt the bookmarks database file'''

        try:
            from getpass import getpass
            import struct
            from hashlib import sha256
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives.ciphers import (Cipher, modes,
                                                                algorithms)
        except Exception:
            logger.error('cryptography lib(s) missing')
            sys.exit(1)

        if iterations < 1:
            logger.error('Iterations must be >= 1')
            sys.exit(1)

        dbpath = os.path.join(BukuDb.get_dbdir_path(), 'bookmarks.db')
        encpath = '%s.enc' % dbpath
        if not os.path.exists(dbpath):
            logger.error('%s missing. Already encrypted?', dbpath)
            sys.exit(1)

        # If both encrypted file and flat file exist, error out
        if os.path.exists(dbpath) and os.path.exists(encpath):
            logger.error('Both encrypted and flat DB files exist!')
            sys.exit(1)

        password = ''
        password = getpass()
        passconfirm = getpass()
        if password == '':
            logger.error('Empty password')
            sys.exit(1)
        if password != passconfirm:
            logger.error('Passwords do not match')
            sys.exit(1)

        # Get SHA256 hash of DB file
        dbhash = BukuCrypt.get_filehash(dbpath)

        # Generate random 256-bit salt and key
        salt = os.urandom(SALT_SIZE)
        key = ('%s%s' % (password,
               salt.decode('utf-8', 'replace'))).encode('utf-8')
        for _ in range(iterations):
            key = sha256(key).digest()

        iv = os.urandom(16)
        encryptor = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        ).encryptor()
        filesize = os.path.getsize(dbpath)

        with open(dbpath, 'rb') as infile:
            with open(encpath, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(salt)
                outfile.write(iv)

                # Embed DB file hash in encrypted file
                outfile.write(dbhash)

                while True:
                    chunk = infile.read(CHUNKSIZE)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk = '%s%s' % (chunk, ' ' * (16 - len(chunk) % 16))

                    outfile.write(encryptor.update(chunk) +
                                  encryptor.finalize())

        os.remove(dbpath)
        print('File encrypted')
        sys.exit(0)

    @staticmethod
    def decrypt_file(iterations):
        '''Decrypt the bookmarks database file'''

        try:
            from getpass import getpass
            import struct
            from hashlib import sha256
            from cryptography.hazmat.backends import default_backend
            from cryptography.hazmat.primitives.ciphers import (Cipher, modes,
                                                                algorithms)
        except Exception:
            logger.error('cryptography lib(s) missing')
            sys.exit(1)

        if iterations < 1:
            logger.error('Decryption failed')
            sys.exit(1)

        dbpath = os.path.join(BukuDb.get_dbdir_path(), 'bookmarks.db')
        encpath = '%s.enc' % dbpath
        if not os.path.exists(encpath):
            logger.error('%s missing', encpath)
            sys.exit(1)

        # If both encrypted file and flat file exist, error out
        if os.path.exists(dbpath) and os.path.exists(encpath):
            logger.error('Both encrypted and flat DB files exist!')
            sys.exit(1)

        password = ''
        password = getpass()
        if password == '':
            logger.error('Decryption failed')
            sys.exit(1)

        with open(encpath, 'rb') as infile:
            origsize = struct.unpack('<Q',
                                     infile.read(struct.calcsize('Q')))[0]

            # Read 256-bit salt and generate key
            salt = infile.read(32)
            key = ('%s%s' % (password,
                   salt.decode('utf-8', 'replace'))).encode('utf-8')
            for _ in range(iterations):
                key = sha256(key).digest()

            iv = infile.read(16)
            decryptor = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=default_backend(),
            ).decryptor()

            # Get original DB file's SHA256 hash from encrypted file
            enchash = infile.read(32)

            with open(dbpath, 'wb') as outfile:
                while True:
                    chunk = infile.read(CHUNKSIZE)
                    if len(chunk) == 0:
                        break

                    outfile.write(decryptor.update(chunk) +
                                  decryptor.finalize())

                outfile.truncate(origsize)

        # Match hash of generated file with that of original DB file
        dbhash = BukuCrypt.get_filehash(dbpath)
        if dbhash != enchash:
            os.remove(dbpath)
            logger.error('Decryption failed')
            sys.exit(1)
        else:
            os.remove(encpath)
            print('File decrypted')


class BukuDb:

    def __init__(self, noninteractive=False, json=False, showOpt=0):
        conn, cur = BukuDb.initdb()
        self.conn = conn
        self.cur = cur
        self.noninteractive = noninteractive
        self.json = json
        self.showOpt = showOpt

    @staticmethod
    def get_dbdir_path():
        '''Determine the directory path where dbfile will be stored:
        if $XDG_DATA_HOME is defined, use it
        else if $HOME exists, use it
        else use the current directory
        '''

        data_home = os.environ.get('XDG_DATA_HOME')
        if data_home is None:
            if os.environ.get('HOME') is None:
                data_home = '.'
            else:
                data_home = os.path.join(os.environ.get('HOME'),
                                         '.local', 'share')

        return os.path.join(data_home, 'buku')

    @staticmethod
    def move_legacy_dbfile():
        '''Move database file from earlier path used in versions <= 1.8
        to new path. Errors out if both the old and new DB files exist.
        '''

        olddbpath = os.path.join(os.environ.get('HOME'), '.cache', 'buku')
        olddbfile = os.path.join(olddbpath, 'bookmarks.db')

        if not os.path.exists(olddbfile):
            return

        newdbpath = BukuDb.get_dbdir_path()
        newdbfile = os.path.join(newdbpath, 'bookmarks.db')

        if os.path.exists(newdbfile):
            logger.error('Both old (%s) and new (%s) DB files exist',
                         olddbfile, newdbfile)
            sys.exit(1)

        if not os.path.exists(newdbpath):
            os.makedirs(newdbpath)

        os.rename(olddbfile, newdbfile)
        print('Database was moved from old (%s) to new (%s) location.\n'
              % (olddbfile, newdbfile))

        os.rmdir(olddbpath)

    @staticmethod
    def initdb():
        '''Initialize the database connection. Create DB
        file and/or bookmarks table if they don't exist.
        Alert on encryption options on first execution.

        Returns: connection, cursor
        '''

        dbpath = BukuDb.get_dbdir_path()
        if not os.path.exists(dbpath):
            os.makedirs(dbpath)

        dbfile = os.path.join(dbpath, 'bookmarks.db')

        encpath = os.path.join(dbpath, 'bookmarks.db.enc')
        # Notify if DB file needs to be decrypted first
        if os.path.exists(encpath) and not os.path.exists(dbfile):
            logger.error('Unlock database first')
            sys.exit(1)

        # Show info on first creation
        if not os.path.exists(dbfile):
            print('DB file is being created. You should encrypt it later.')

        try:
            # Create a connection
            conn = sqlite3.connect(dbfile)
            conn.create_function('REGEXP', 2, regexp)
            cur = conn.cursor()

            # Create table if it doesn't exist
            cur.execute('CREATE TABLE if not exists bookmarks \
                        (id integer PRIMARY KEY, URL text NOT NULL UNIQUE, \
                        metadata text default \'\', tags text default \',\', \
                        desc text default \'\')')
            conn.commit()
        except Exception as e:
            _, _, linenumber, func, _, _ = inspect.stack()[0]
            logger.error('%s(), ln %d: %s', func, linenumber, e)
            sys.exit(1)

        # Add description column in existing DB (from version 2.1)
        try:
            query = 'ALTER TABLE bookmarks ADD COLUMN desc text default \'\''
            cur.execute(query)
            conn.commit()
        except Exception:
            pass

        return (conn, cur)

    def get_bookmark_by_index(self, index):
        '''Get a bookmark from database by its ID.
        Return data as a tuple. Return None if index not found.
        '''

        self.cur.execute('SELECT * FROM bookmarks WHERE id = ?', (index,))
        results = self.cur.fetchall()
        if len(results) == 0:
            return None
        else:
            return results[0]

    def get_bookmark_index(self, url):
        '''Check if URL already exists in DB

        Params: URL to search
        Returns: DB index if URL found, else -1
        '''

        self.cur.execute('SELECT id FROM bookmarks WHERE URL = ?', (url,))
        resultset = self.cur.fetchall()
        if len(resultset) == 0:
            return -1

        return resultset[0][0]

    def add_bookmark(self, url, title_manual=None, tag_manual=None,
                     desc=None, delayed_commit=False):
        '''Add a new bookmark

        :param url: url to bookmark
        :param tag_manual: string of comma-separated tags to add manually
        :param title_manual: string title to add manually
        :param desc: string description
        '''

        # Ensure that the URL does not exist in DB already
        id = self.get_bookmark_index(url)
        if id != -1:
            logger.error('URL [%s] already exists at index %d', url, id)
            return

        # Process title
        if title_manual is not None:
            meta = title_manual
        else:
            meta = network_handler(url)
            if meta == '':
                print('\x1B[91mTitle: []\x1B[0m\n')
            logger.debug('Title: [%s]', meta)

        # Process tags
        if tag_manual is None:
            tag_manual = DELIMITER
        else:
            if tag_manual[0] != DELIMITER:
                tag_manual = '%s%s' % (DELIMITER, tag_manual)
            if tag_manual[-1] != DELIMITER:
                tag_manual = '%s%s' % (tag_manual, DELIMITER)

        # Process description
        if desc is None:
            desc = ''

        try:
            query = 'INSERT INTO bookmarks(URL, metadata, tags, desc) \
                    VALUES (?, ?, ?, ?)'
            self.cur.execute(query, (url, meta, tag_manual, desc))
            if not delayed_commit:
                self.conn.commit()
            self.print_bookmark(self.cur.lastrowid)
        except Exception as e:
            _, _, linenumber, func, _, _ = inspect.stack()[0]
            logger.error('%s(), ln %d: %s', func, linenumber, e)

    def append_tag_at_index(self, index, tag_manual):
        ''' Append tags for bookmark at index

        :param index: int position of record, 0 for all
        :tag_manual: string of comma-separated tags to add manually
        '''

        if index == 0:
            resp = input('Append specified tags to ALL bookmarks? (y/n): ')
            if resp != 'y':
                return

            self.cur.execute('SELECT id, tags FROM bookmarks ORDER BY id ASC')
        else:
            self.cur.execute('SELECT id, tags FROM bookmarks WHERE id = ?',
                             (index,))

        resultset = self.cur.fetchall()
        query = 'UPDATE bookmarks SET tags = ? WHERE id = ?'
        for row in resultset:
            tags = '%s%s' % (row[1], tag_manual[1:])
            tags = parse_tags([tags])
            self.cur.execute(query, (tags, row[0],))

        self.conn.commit()

    def delete_tag_at_index(self, index, tag_manual):
        ''' Delete tags for bookmark at index

        :param index: int position of record, 0 for all
        :tag_manual: string of comma-separated tags to delete manually
        '''

        tags_to_delete = tag_manual.strip(DELIMITER).split(DELIMITER)

        if index == 0:
            resp = input('Delete specified tags from ALL bookmarks? (y/n): ')
            if resp != 'y':
                return

            query1 = "SELECT id, tags FROM bookmarks WHERE tags \
                     LIKE '%' || ? || '%' ORDER BY id ASC"
            query2 = 'UPDATE bookmarks SET tags = ? WHERE id = ?'
            for tag in tags_to_delete:
                self.cur.execute(query1, (tag,))
                resultset = self.cur.fetchall()

                for row in resultset:
                    tags = row[1]

                    tags = tags.replace('%s%s%s'
                                        % (DELIMITER, tag, DELIMITER,),
                                        DELIMITER)
                    self.cur.execute(query2, (parse_tags([tags]), row[0],))

                self.conn.commit()
        else:
            query = 'SELECT id, tags FROM bookmarks WHERE id = ?'
            self.cur.execute(query, (index,))
            resultset = self.cur.fetchall()

            query = 'UPDATE bookmarks SET tags = ? WHERE id = ?'
            for row in resultset:
                tags = row[1]

                for tag in tags_to_delete:
                    tags = tags.replace('%s%s%s' % (DELIMITER, tag,
                                        DELIMITER,), DELIMITER)

                self.cur.execute(query, (parse_tags([tags]), row[0],))
                self.conn.commit()

    def update_bookmark(self, index, url='', title_manual=None,
                        tag_manual=None, desc=None,
                        append_tag=False, delete_tag=False):
        ''' Update an existing record at index
        Update all records if index is 0 and url is not specified.
        URL is an exception because URLs are unique in DB.

        :param index: int position to update, 0 for all
        :param url: address
        :param tag_manual: string of comma-separated tags to add manually
        :param title_manual: string title to add manually
        :param desc: string description
        :return:
        '''

        arguments = []
        query = 'UPDATE bookmarks SET'
        to_update = False

        # Update URL if passed as argument
        if url != '':
            if index == 0:
                logger.error('All URLs cannot be same')
                return
            query = '%s URL = ?,' % query
            arguments += (url,)
            to_update = True

        # Update tags if passed as argument
        if tag_manual is not None:
            if append_tag:
                self.append_tag_at_index(index, tag_manual)
            elif delete_tag:
                self.delete_tag_at_index(index, tag_manual)
            else:
                query = '%s tags = ?,' % query
                arguments += (tag_manual,)
                to_update = True

        # Update description if passed as an argument
        if desc is not None:
            query = '%s desc = ?,' % query
            arguments += (desc,)
            to_update = True

        # Update title
        #
        # 1. if -t has no arguments, delete existing title
        # 2. if -t has arguments, update existing title
        # 3. if -t option is omitted at cmdline:
        #    if URL is passed, update the title from web using the URL
        # 4. if no other argument (url, tag, comment) passed,
        #    update title from web using DB URL
        meta = None
        if title_manual is not None:
            meta = title_manual
        elif url != '':
            meta = network_handler(url)
            if meta == '':
                print('\x1B[91mTitle: []\x1B[0m')
            logger.debug('Title: [%s]', meta)
        elif not to_update and not (append_tag or delete_tag):
            self.refreshdb(index)
            if index > 0:
                self.print_bookmark(index)
            return

        if meta is not None:
            query = '%s metadata = ?,' % query
            arguments += (meta,)
            to_update = True

        if not to_update:       # Nothing to update
            return

        if index == 0:  # Update all records
            resp = input('Update ALL bookmarks? (y/n): ')
            if resp != 'y':
                return

            query = query[:-1]
        else:
            query = '%s WHERE id = ?' % query[:-1]
            arguments += (index,)

        logger.debug('query: "%s", args: %s', query, arguments)

        try:
            self.cur.execute(query, arguments)
            self.conn.commit()
            if self.cur.rowcount == 1:
                self.print_bookmark(index)
            elif self.cur.rowcount == 0:
                logger.error('No matching index %s', index)
        except sqlite3.IntegrityError:
            logger.error('URL already exists')

    def refreshdb(self, index):
        '''Refresh ALL records in the database. Fetch title for each
        bookmark from the web and update the records. Doesn't udpate
        the record if title is empty.
        This API doesn't change DB index, URL or tags of a bookmark.

        :param index: index of record to update, or 0 for all records
        '''

        if index == 0:
            self.cur.execute('SELECT id, url FROM bookmarks ORDER BY id ASC')
        else:
            self.cur.execute('SELECT id, url FROM bookmarks WHERE id = ?',
                             (index,))

        resultset = self.cur.fetchall()
        query = 'UPDATE bookmarks SET metadata = ? WHERE id = ?'
        for row in resultset:
            title = network_handler(row[1])
            if title == '':
                print('\x1b[1mIndex %d: no title\x1b[21m\x1B[0m\n' % row[0])
                continue
            else:
                print('Title: [%s]' % title)

            self.cur.execute(query, (title, row[0],))
            print('Index %d updated\n' % row[0])
            if interrupted:
                logger.warning('^C pressed. Aborting DB refresh...')
                break

        self.conn.commit()

    def searchdb(self, keywords, all_keywords=False, delete=False, deep=False):
        '''Search the database for an entries with tags or URL
        or title info matching keywords and list those.

        :param keywords: keywords to search
        :param all_keywords: search any or all keywords
        :param delete: delete search results
        :param deep: search for matching substrings
        '''

        arguments = []
        placeholder = "'%' || ? || '%'"
        query = 'SELECT id, url, metadata, tags, desc FROM bookmarks WHERE'

        if all_keywords:  # Match all keywords in URL or Title
            for token in keywords:
                if not deep:
                    token = '\\b' + token + '\\b'
                    query = '%s (tags REGEXP ? OR URL REGEXP ? OR metadata \
                            REGEXP ? OR desc REGEXP ?) AND' % (query)
                else:
                    query = '%s (tags LIKE (%s) OR URL LIKE (%s) OR metadata \
                            LIKE (%s) OR desc LIKE (%s)) AND' \
                            % (query, placeholder, placeholder,
                               placeholder, placeholder)

                arguments += (token, token, token, token)
            query = query[:-4]
        else:  # Match any keyword in URL or Title
            for token in keywords:
                if not deep:
                    token = '\\b' + token + '\\b'
                    query = '%s tags REGEXP ? OR URL REGEXP ? OR metadata \
                            REGEXP ? OR desc REGEXP ? OR' % (query)
                else:
                    query = '%s tags LIKE (%s) OR URL LIKE (%s) OR metadata \
                            LIKE (%s) OR desc LIKE (%s) OR' \
                            % (query, placeholder, placeholder,
                               placeholder, placeholder)

                arguments += (token, token, token, token)
            query = query[:-3]

        query = '%s ORDER BY id ASC' % query

        logger.debug('query: "%s", args: %s', query, arguments)

        self.cur.execute(query, arguments)
        results = self.cur.fetchall()
        if len(results) == 0:
            return

        if not self.json:
            prompt(results, self.noninteractive, delete)
        else:
            print(format_json(results, showOpt=self.showOpt))

    def search_by_tag(self, tag, delete=False):
        '''Search and list bookmarks with a tag

        :param tag: tag to search
        '''

        query = "SELECT id, url, metadata, tags, desc FROM bookmarks \
                WHERE tags LIKE '%' || ? || '%' ORDER BY id ASC"
        logger.debug('query: "%s", args: %s', query, tag)

        self.cur.execute(query, (tag,))
        results = self.cur.fetchall()
        if len(results) == 0:
            return

        if not self.json:
            prompt(results, self.noninteractive, delete)
        else:
            print(format_json(results, showOpt=self.showOpt))

    def compactdb(self, index):
        '''When an entry at index is deleted, move the last
        entry in DB to index, if index is lesser.

        Params: index of deleted entry
        '''

        self.cur.execute('SELECT MAX(id) from bookmarks')
        results = self.cur.fetchall()
        # Return if the last index was just deleted
        if len(results) == 1 and results[0][0] is None:
            return

        query1 = 'SELECT id, URL, metadata, tags, \
                 desc FROM bookmarks WHERE id = ?'
        query2 = 'DELETE FROM bookmarks WHERE id = ?'
        query3 = 'INSERT INTO bookmarks(id, URL, metadata, \
                 tags, desc) VALUES (?, ?, ?, ?, ?)'

        for row in results:
            if row[0] > index:
                self.cur.execute(query1, (row[0],))
                results = self.cur.fetchall()
                for row in results:
                    self.cur.execute(query2, (row[0],))
                    self.conn.commit()
                    self.cur.execute(query3,
                                     (index, row[1], row[2], row[3], row[4],))
                    self.conn.commit()
                    print('Index %d moved to %d' % (row[0], index))

    def delete_bookmark(self, index, low=0, high=0, is_range=False):
        '''Delete a single record or remove the table if index is None

        Params: index to delete
        '''

        if is_range:
            try:
                query = 'DELETE from bookmarks where id BETWEEN ? AND ?'
                self.cur.execute(query, (low, high))
                self.conn.commit()
                print('Bookmarks from index %s to %s deleted' % (low, high))
            except IndexError:
                logger.error('Index out of bound')

            for index in range(low, high + 1):
                self.compactdb(index)
        elif index == 0:  # Remove the table
            resp = input('Remove ALL bookmarks? (y/n): ')
            if resp != 'y':
                print('No bookmarks deleted')
                return

            self.delete_all_bookmarks()
            print('All bookmarks deleted')
        else:  # Remove a single entry
            try:
                query = 'DELETE FROM bookmarks WHERE id = ?'
                self.cur.execute(query, (index,))
                self.conn.commit()
                if self.cur.rowcount == 1:
                    print('Removed index %d' % index)
                    self.compactdb(index)
                else:
                    logger.error('No matching index')
            except IndexError:
                logger.error('Index out of bound')

        return True

    def delete_all_bookmarks(self):
        '''Should only be called inside of delete_bookmark
        Drops the bookmark table if it exists
        '''

        self.cur.execute('DROP TABLE if exists bookmarks')
        self.conn.commit()

    def print_bookmark(self, index, empty=False):
        '''Print bookmark details at index or all bookmarks if index is 0
        Print only bookmarks with blank title or tag if empty is True
        Note: URL is printed on top because title may be blank

        Params: index to print (0 for all)
        empty flag to show only bookmarks with no title or tags
        '''

        if index == 0:  # Show all entries
            if not empty:
                self.cur.execute('SELECT * FROM bookmarks')
                resultset = self.cur.fetchall()
            else:
                qry = "SELECT * FROM bookmarks WHERE metadata = '' OR tags = ?"
                self.cur.execute(qry, (DELIMITER,))
                resultset = self.cur.fetchall()
                print('\x1b[1m%s records found\x1b[21m\n' % len(resultset))

            if not self.json:
                if self.showOpt == 0:
                    for row in resultset:
                        print_record(row)
                elif self.showOpt == 1:
                    for row in resultset:
                        print('%s\t%s' % (row[0], row[1]))
                elif self.showOpt == 2:
                    for row in resultset:
                        print('%s\t%s\t%s' % (row[0], row[1], row[3][1:-1]))
            else:
                print(format_json(resultset, showOpt=self.showOpt))
        else:  # Show record at index
            try:
                query = 'SELECT * FROM bookmarks WHERE id = ?'
                self.cur.execute(query, (index,))
                results = self.cur.fetchall()
                if len(results) == 0:
                    logger.error('No matching index')
                    return
            except IndexError:
                logger.error('Index out of bound')
                return

            if not self.json:
                for row in results:
                    if self.showOpt == 0:
                        print_record(row)
                    elif self.showOpt == 1:
                        print('%s\t%s' % (row[0], row[1]))
                    elif self.showOpt == 2:
                        print('%s\t%s\t%s' % (row[0], row[1], row[3][1:-1]))
            else:
                print(format_json(results, True, self.showOpt))

    def list_tags(self):
        '''Print all unique tags ordered alphabetically'''

        count = 1
        Tags = []
        uniqueTags = []
        query = 'SELECT DISTINCT tags FROM bookmarks ORDER BY tags'
        for row in self.cur.execute(query):
            tagset = row[0].strip(DELIMITER).split(DELIMITER)
            for tag in tagset:
                if tag not in Tags:
                    Tags += (tag,)

        if Tags[0] == '':
            uniqueTags = sorted(Tags[1:], key=str.lower)
        else:
            uniqueTags = sorted(Tags, key=str.lower)
        for tag in uniqueTags:
            print('%6d. %s' % (count, tag))
            count += 1

    def replace_tag(self, orig, new=None):
        '''Replace orig tags with new tags in DB for all records.
        Remove orig tag if new tag is empty.

        Params: original and new tags
        '''

        update = False
        delete = False
        newtags = DELIMITER

        orig = '%s%s%s' % (DELIMITER, orig, DELIMITER)
        if new is None:
            delete = True
        else:
            newtags = parse_tags(new)
            if newtags == DELIMITER:
                delete = True

        if orig == newtags:
            print('Tags are same.')
            return

        query = 'SELECT id, tags FROM bookmarks WHERE tags LIKE ?'
        self.cur.execute(query, ('%' + orig + '%',))
        results = self.cur.fetchall()

        query = 'UPDATE bookmarks SET tags = ? WHERE id = ?'
        for row in results:
            if not delete:
                # Check if tag newtags is already added
                if row[1].find(newtags) >= 0:
                    newtags = DELIMITER

            tags = row[1].replace(orig, newtags)
            tags = parse_tags([tags])
            self.cur.execute(query, (tags, row[0],))
            print('Index %d updated' % row[0])
            update = True

        if update:
            self.conn.commit()

    def browse_by_index(self, index):
        '''Open URL at index in browser

        Params: index
        '''

        query = 'SELECT URL FROM bookmarks WHERE id = ?'
        try:
            for row in self.cur.execute(query, (index,)):
                url = unquote(row[0])
                open_in_browser(url)
                return
            logger.error('No matching index')
        except IndexError:
            logger.error('Index out of bound')

    def export_bookmark(self, fp):
        '''Export bookmarks to a Firefox
        bookmarks formatted html file.

        Params: Path to file to export to
        '''

        import time

        if os.path.exists(fp):
            resp = input('%s exists. Overwrite? (y/n): ' % fp)
            if resp != 'y':
                return

        try:
            f = open(fp, mode='w', encoding='utf-8')
        except Exception as e:
            logger.error(e)
            return

        count = 0
        timestamp = int(time.time())
        self.cur.execute('SELECT * FROM bookmarks')
        resultset = self.cur.fetchall()

        f.write('''<!DOCTYPE NETSCAPE-Bookmark-file-1>

<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>

<DL><p>
    <DT><H3 ADD_DATE="%s" LAST_MODIFIED="%s" PERSONAL_TOOLBAR_FOLDER="true">Buku bookmarks</H3>
    <DL><p>
''' % (timestamp, timestamp))

        for row in resultset:
            entry = '        <DT><A HREF="%s" ADD_DATE="%s" LAST_MODIFIED="%s"' \
                    % (row[1], timestamp, timestamp)
            if row[3] != DELIMITER:
                entry = '%s TAGS="%s"' % (entry, row[3][1:-1])
            entry = '%s>%s</A>\n' % (entry, row[2])
            if row[4] != '':
                entry = '%s        <DD>%s\n' % (entry, row[4])

            f.write(entry)
            count += 1

        f.write('    </DL><p>\n</DL><p>')
        f.close()
        print('%s bookmarks exported' % count)

    def import_bookmark(self, fp):
        '''Import bookmarks from a html file.
        Supports Firefox, Google Chrome and IE imports

        Params: Path to file to import
        '''

        try:
            import bs4
            with open(fp, mode='r', encoding='utf-8') as f:
                soup = bs4.BeautifulSoup(f, 'html.parser')
        except ImportError:
            logger.error('Beautiful Soup not found')
            return
        except Exception as e:
            logger.error(e)
            return

        html_tags = soup.findAll('a')
        for tag in html_tags:
            # Extract comment from <dd> tag
            desc = None
            comment_tag = tag.findNextSibling('dd')
            if comment_tag:
                desc = comment_tag.text[0:comment_tag.text.find('\n')]

            self.add_bookmark(tag['href'], tag.string,
                              ('%s%s%s' % (DELIMITER, tag['tags'], DELIMITER))
                              if tag.has_attr('tags') else None, desc, True)

        self.conn.commit()
        f.close()

    def mergedb(self, fp):
        '''Merge bookmarks from another Buku database file

        Params: Path to file to merge
        '''

        try:
            # Connect to input DB
            if sys.version_info >= (3, 4, 4):
                # Python 3.4.4 and above
                connfp = sqlite3.connect('file:%s?mode=ro' % fp, uri=True)
            else:
                connfp = sqlite3.connect(fp)

            curfp = connfp.cursor()
        except Exception as e:
            logger.error(e)
            return

        curfp.execute('SELECT * FROM bookmarks')
        resultset = curfp.fetchall()
        for row in resultset:
            self.add_bookmark(row[1], row[2], row[3], row[4], True)

        self.conn.commit()

        try:
            curfp.close()
            connfp.close()
        except Exception:
            pass

    def close_quit(self, exitval=0):
        '''Close a DB connection and exit'''

        if self.conn is not None:
            try:
                self.cur.close()
                self.conn.close()
            except Exception:
                # ignore errors here, we're closing down
                pass
        sys.exit(exitval)


# Generic functions

def connect_server(url):
    '''Connect to a server and fetch the requested page data.
    Supports gzip compression.

    Params: URL to fetch
    Returns: connection, HTTP(S) GET response
    '''

    if url.find('%20') != -1:
        url = unquote(url).replace(' ', '%20')
    else:
        url = unquote(url)

    logger.debug('unquoted: %s', url)

    if url.find('https://') >= 0:  # Secure connection
        server = url[8:]
        marker = server.find('/')
        if marker > 0:
            url = server[marker:]
            server = server[:marker]
        else:  # Handle domain name without trailing /
            url = '/'
        urlconn = HTTPSConnection(server, timeout=30)
    elif url.find('http://') >= 0:  # Insecure connection
        server = url[7:]
        marker = server.find('/')
        if marker > 0:
            url = server[marker:]
            server = server[:marker]
        else:
            url = '/'
        urlconn = HTTPConnection(server, timeout=30)
    else:
        logger.warning('Not a valid HTTP(S) url')
        if url.find(':') == -1:
            logger.warning('Not a valid uri either')
        return (None, None)

    logger.debug('server [%s] rel [%s]', server, url)

    # Handle URLs passed with %xx escape
    try:
        url.encode('ascii')
    except Exception:
        url = quote(url)

    urlconn.request('GET', url, None, {
        'Accept-encoding': 'gzip',
        'DNT': '1',
    })
    return (urlconn, urlconn.getresponse())


def get_page_title(resp):
    '''Invoke HTML parser and extract title from HTTP response

    Params: GET response and invoke HTML parser
    '''

    data = None
    charset = resp.headers.get_content_charset()

    if resp.headers.get('Content-Encoding') == 'gzip':
        payload = resp.read()
        logger.debug('gzip response')
        data = gzip.decompress(payload)
    else:
        data = resp.read()

    if charset is None:
        logger.warning('Charset missing in response')
        charset = 'utf-8'

    logger.debug('charset: %s', charset)

    parser = BMHTMLParser()
    try:
        if charset == 'utf-8':
            parser.feed(data.decode(charset, 'replace'))
        else:
            parser.feed(data.decode(charset))
    except Exception as e:
        # Suppress Exception due to intentional self.reset() in HTMLParser
        if logger.isEnabledFor(logging.DEBUG) \
                and str(e) != 'we should not get here!':
            _, _, linenumber, func, _, _ = inspect.stack()[0]
            logger.error('%s(), ln %d: %s', func, linenumber, e)


def network_handler(url):
    '''Handle server connection and redirections

    Params: URL to fetch
    Returns: page title or empty string, if not found
    '''

    global titleData
    titleData = None
    urlconn = None
    retry = False

    try:
        urlconn, resp = connect_server(url)

        while True:
            if resp is None:
                break
            elif resp.status == 200:
                get_page_title(resp)
                break
            elif resp.status in [301, 302]:
                redirurl = urljoin(url, resp.getheader('location', ''))
                logger.debug('REDIRECTION: %s', redirurl)
                retry = False       # Reset retry, start fresh on redirection

                # gracefully handle Google blocks
                if redirurl.find('sorry/IndexRedirect?') >= 0:
                    logger.error('Connection blocked due to unusual activity')
                    break

                marker = redirurl.find('redirectUrl=')
                if marker != -1:
                    redirurl = redirurl[marker + 12:]

                # break same URL redirection loop
                if url == redirurl:
                    logger.error('Detected repeated redirection to same URL')
                    break

                url = redirurl
                urlconn.close()
                # Try with complete URL on redirection
                urlconn, resp = connect_server(url)
            elif resp.status == 403 and not retry:
                # Handle URLs in the form of
                # https://www.domain.com or
                # https://www.domain.com/
                # which fail when trying to fetch
                # resource '/', retry with full path

                urlconn.close()
                logger.debug('Received status 403: retrying...')
                # Remove trailing /
                if url[-1] == '/':
                    url = url[:-1]
                urlconn, resp = connect_server(url)
                retry = True
            else:
                logger.error('[%s] %s', resp.status, resp.reason)
                break
    except Exception as e:
        _, _, linenumber, func, _, _ = inspect.stack()[0]
        logger.error('%s(), ln %d: %s', func, linenumber, e)
    finally:
        if urlconn is not None:
            urlconn.close()
        if titleData is None:
            return ''
        return titleData.strip().replace('\n', '')


def parse_tags(keywords=None):
    '''Format and get tag string from tokens'''

    if keywords is None:
        return None

    tags = DELIMITER
    origTags = []
    uniqueTags = []

    # Cleanse and get the tags
    tagstr = ' '.join(keywords)
    marker = tagstr.find(DELIMITER)

    while marker >= 0:
        token = tagstr[0:marker]
        tagstr = tagstr[marker + 1:]
        marker = tagstr.find(DELIMITER)
        token = token.strip()
        if token == '':
            continue

        tags = '%s%s%s' % (tags, token, DELIMITER)

    tagstr = tagstr.strip()
    if tagstr != '':
        tags = '%s%s%s' % (tags, tagstr, DELIMITER)

    logger.debug('keywords: %s', keywords)
    logger.debug('parsed tags: [%s]', tags)

    if tags == DELIMITER:
        return tags

    origTags += tags.strip(DELIMITER).split(DELIMITER)
    for tag in origTags:
        if tag not in uniqueTags:
            uniqueTags += (tag, )  # Select unique tags

    # Sort the tags
    sortedTags = sorted(uniqueTags, key=str.lower)

    # Wrap with delimiter
    return '%s%s%s' % (DELIMITER, DELIMITER.join(sortedTags), DELIMITER)


def prompt(results, noninteractive=False, delete=False):
    '''Show each matching result from a search and prompt'''

    count = 0
    for row in results:
        count += 1
        print_record(row, count)

    if delete:
        resp = input('Delete the search results? (y/n): ')
        if resp != 'y'and resp != 'Y':
            return

        # delete records in reverse order
        pos = len(results) - 1
        while(pos >= 0):
            idx = results[pos][0]
            bdb.delete_bookmark(idx)
            pos = pos - 1

    # prompt and open
    else:
        if noninteractive:
            return

        while True:
            try:
                nav = input('Results, ranges (x-y,(a)ll) to open: ')
                if not nav:
                    nav = input('Results, ranges (x-y,(a)ll) to open: ')
                    if not nav:
                        # Quit on double enter
                        break
            except EOFError:
                return

            # open all results and re-prompt if 'a' is pressed
            if nav == 'a':
                for index in range(0, count):
                    try:
                        open_in_browser(unquote(results[index][1]))
                    except Exception as e:
                        _, _, linenumber, func, _, _ = inspect.stack()[0]
                        logger.error('%s(), ln %d: %s', func, linenumber, e)

                continue

            # iterate over whitespace separated indices
            for nav in (' '.join(nav.split())).split():
                if is_int(nav):
                    index = int(nav) - 1
                    if index < 0 or index >= count:
                        logger.error('Index out of bound')
                        continue
                    try:
                        open_in_browser(unquote(results[index][1]))
                    except Exception as e:
                        _, _, linenumber, func, _, _ = inspect.stack()[0]
                        logger.error('%s(), ln %d: %s', func, linenumber, e)
                elif '-' in nav and is_int(nav.split('-')[0]) \
                        and is_int(nav.split('-')[1]):
                    lower = int(nav.split('-')[0])
                    upper = int(nav.split('-')[1])
                    if lower > upper:
                        lower, upper = upper, lower
                    for index in range(lower-1, upper):
                        try:
                            open_in_browser(unquote(results[index][1]))
                        except Exception as e:
                            _, _, linenumber, func, _, _ = inspect.stack()[0]
                            logger.error('%s(), ln %d: %s',
                                         func, linenumber, e)
                else:
                    break


def print_record(row, count=0):
    '''Print a single DB record
    Handles differently for search and print (count = 0)
    '''

    # Print index and URL
    if count != 0:
        printstr = '\x1B[1m\x1B[93m%d. \x1B[0m\x1B[92m%s\x1B[0m  \
                   \x1B[1m[%s]\x1B[0m\n' % (count, row[1], row[0])
    else:
        printstr = '\x1B[1m\x1B[93m%d. \x1B[0m\x1B[92m%s\x1B[0m\n' \
                   % (row[0], row[1])

    # Print title
    if row[2] != '':
        printstr = '%s   \x1B[91m>\x1B[0m %s\n' % (printstr, row[2])

    # Print description
    if row[4] != '':
        printstr = '%s   \x1B[91m+\x1B[0m %s\n' % (printstr, row[4])

    # Print tags IF not default (DELIMITER)
    if row[3] != DELIMITER:
        printstr = '%s   \x1B[91m#\x1B[0m %s\n' % (printstr, row[3][1:-1])

    print(printstr)


def format_json(resultset, single=False, showOpt=0):
    '''Return results in Json format'''

    if not single:
        marks = []
        for row in resultset:
            if showOpt == 1:
                record = {'uri': row[1]}
            elif showOpt == 2:
                record = {'uri': row[1], 'tags': row[3][1:-1]}
            else:
                record = {'uri': row[1], 'title': row[2],
                          'description': row[4], 'tags': row[3][1:-1]}

            marks.append(record)
    else:
        marks = {}
        for row in resultset:
            if showOpt == 1:
                marks['uri'] = row[1]
            elif showOpt == 2:
                marks['uri'] = row[1]
                marks['tags'] = row[3][1:-1]
            else:
                marks['uri'] = row[1]
                marks['title'] = row[2]
                marks['description'] = row[4]
                marks['tags'] = row[3][1:-1]

    return json.dumps(marks, sort_keys=True, indent=4)


def is_int(string):
    '''Check if a string is a digit

    Params: string
    '''

    try:
        int(string)
        return True
    except Exception:
        return False


def open_in_browser(url):
    '''Duplicate stdin, stdout (to suppress showing errors
    on the terminal) and open URL in default browser

    Params: url to open
    '''

    url = url.replace('%22', '\"')

    _stderr = os.dup(2)
    os.close(2)
    _stdout = os.dup(1)
    os.close(1)
    fd = os.open(os.devnull, os.O_RDWR)
    os.dup2(fd, 2)
    os.dup2(fd, 1)
    try:
        webbrowser.open(url)
    except Exception as e:
        _, _, linenumber, func, _, _ = inspect.stack()[0]
        logger.error('%s(), ln %d: %s', func, linenumber, e)
    finally:
        os.close(fd)
        os.dup2(_stderr, 2)
        os.dup2(_stdout, 1)


def sigint_handler(signum, frame):
    '''Custom SIGINT handler'''

    global interrupted

    interrupted = True
    print('\nInterrupted.', file=sys.stderr)
    sys.exit(1)

signal.signal(signal.SIGINT, sigint_handler)


def regexp(expr, item):
    '''Perform a regular expression search'''

    return re.search(expr, item, re.IGNORECASE) is not None

# Custom Action classes for argparse


class CustomUpdateAction(argparse.Action):
    '''Class to capture if optional param 'update'
    is actually used, even if sans arguments
    '''

    def __call__(self, parser, args, values, option_string=None):
        global update

        update = True
        # NOTE: the following converts a None argument to an empty array []
        setattr(args, self.dest, values)


class CustomTagAction(argparse.Action):
    '''Class to capture if optional param 'tag'
    is actually used, even if sans arguments
    '''

    def __call__(self, parser, args, values, option_string=None):
        global tagManual

        tagManual = [DELIMITER, ]
        setattr(args, self.dest, values)


class CustomTitleAction(argparse.Action):
    '''Class to capture if optional param 'title'
    is actually used, even if sans arguments
    '''

    def __call__(self, parser, args, values, option_string=None):
        global titleManual

        titleManual = ''
        setattr(args, self.dest, values)


class CustomDescAction(argparse.Action):
    '''Class to capture if optional param 'comment'
    is actually used, even if sans arguments
    '''

    def __call__(self, parser, args, values, option_string=None):
        global description

        description = ''
        setattr(args, self.dest, values)


class CustomTagSearchAction(argparse.Action):
    '''Class to capture if optional param 'stag'
    is actually used, even if sans arguments
    '''

    def __call__(self, parser, args, values, option_string=None):
        global tagsearch

        tagsearch = True
        setattr(args, self.dest, values)


class ExtendedArgumentParser(argparse.ArgumentParser):
    '''Extend classic argument parser'''

    # Print additional help and info
    @staticmethod
    def print_extended_help(file=None):
        file.write('''
prompt keys:
  1-N                  open the Nth search result in web browser
                       ranges, space-separated result indices work
  double Enter         exit buku

symbols:
  >                    title
  +                    comment
  #                    tags

Version %s
Copyright (C) 2015-2016 Arun Prakash Jana <engineerarun@gmail.com>
License: GPLv3
Webpage: https://github.com/jarun/Buku
''' % _VERSION_)

    # Help
    def print_help(self, file=None):
        super(ExtendedArgumentParser, self).print_help(file)
        self.print_extended_help(file)


'''main starts here'''


# Handle piped input
def main(argv, pipeargs=None):
    if not sys.stdin.isatty():
        pipeargs.extend(argv)
        for s in sys.stdin.readlines():
            pipeargs.extend(s.split())

if __name__ == '__main__':
    pipeargs = []
    atexit.register(logging.shutdown)

    try:
        main(sys.argv, pipeargs)
    except KeyboardInterrupt:
        pass

    # If piped input, set argument vector
    if len(pipeargs) > 0:
        sys.argv = pipeargs

    # Setup custom argument parser
    argparser = ExtendedArgumentParser(
        description='A powerful command-line bookmark manager. Your mini web!',
        formatter_class=argparse.RawTextHelpFormatter,
        usage='''buku [OPTIONS] [KEYWORD [KEYWORD ...]]''',
        add_help=False
    )

    # General options group
    general_grp = argparser.add_argument_group(
        title='general options',
        description='''-a, --add URL [tags ...]
                     bookmark URL with comma-separated tags
-u, --update [...]   update fields of bookmark at DB indices
                     refresh all titles, if no arguments
                     refresh titles of bookmarks at indices,
                     if no edit options are specified
                     accepts indices and ranges
-d, --delete [...]   delete bookmarks. Valid inputs: either
                     a hyphenated single range (100-200),
                     OR space-separated indices (100 15 200)
                     delete search results with search options
                     delete all bookmarks, if no arguments
-h, --help           show this information and exit''')
    addarg = general_grp.add_argument
    addarg('-a', '--add', nargs='+', dest='addurl', metavar=('URL', 'tags'),
           help=argparse.SUPPRESS)
    addarg('-u', '--update', nargs='*', dest='update',
           action=CustomUpdateAction, metavar=('N', 'URL tags'),
           help=argparse.SUPPRESS)
    addarg('-d', '--delete', nargs='*', dest='delete', metavar='N',
           help=argparse.SUPPRESS)
    addarg('-h', '--help', dest='help', action='store_true',
           help=argparse.SUPPRESS)

    # Edit options group
    edit_grp = argparser.add_argument_group(
        title='edit options',
        description='''--url keyword        specify url, works with -u only
--tag [+|-] [...]    set comma-separated tags, works with -a, -u
                     clear tags, if no arguments
                     append specified tags, if preceded by '+'
                     remove specified tags, if preceded by '-'
-t, --title [...]    manually set title, works with -a, -u
                     if no arguments:
                     -a: do not set title, -u: clear title
-c, --comment [...]  description of the bookmark, works with
                     -a, -u; clears comment, if no arguments''')
    addarg = edit_grp.add_argument
    addarg('--url', nargs=1, dest='url', metavar='url', help=argparse.SUPPRESS)
    addarg('--tag', nargs='*', dest='tag', action=CustomTagAction,
           metavar='tag', help=argparse.SUPPRESS)
    addarg('-t', '--title', nargs='*', dest='title', action=CustomTitleAction,
           metavar='title', help=argparse.SUPPRESS)
    addarg('-c', '--comment', nargs='*', dest='desc', type=str,
           action=CustomDescAction, metavar='desc', help=argparse.SUPPRESS)

    # Search options group
    search_grp = argparser.add_argument_group(
        title='search options',
        description='''-s, --sany keyword [...]
                     search bookmarks for ANY matching keyword
-S, --sall keyword [...]
                     search bookmarks with ALL keywords
                     special keyword -
                     "blank": list entries with empty title/tag
--deep               match substrings ('pen' matches 'opened')
--st, --stag [...]   search bookmarks by tag
                     list tags alphabetically, if no arguments''')
    addarg = search_grp.add_argument
    addarg('-s', '--sany', nargs='+', metavar='keyword',
           help=argparse.SUPPRESS)
    addarg('-S', '--sall', nargs='+', metavar='keyword',
           help=argparse.SUPPRESS)
    addarg('--deep', dest='deep', action='store_true', help=argparse.SUPPRESS)
    addarg('--st', '--stag', nargs='*', dest='stag',
           action=CustomTagSearchAction, metavar='keyword',
           help=argparse.SUPPRESS)

    # Encryption options group
    crypto_grp = argparser.add_argument_group(
        title='encryption options',
        description='''-l, --lock [N]       encrypt DB file with N (> 0, default 8)
                     hash iterations to generate key
-k, --unlock [N]     decrypt DB file with N (> 0, default 8)
                     hash iterations to generate key''')
    addarg = crypto_grp.add_argument
    addarg('-k', '--unlock', nargs='?', dest='decrypt', type=int, const=8,
           metavar='N', help=argparse.SUPPRESS)
    addarg('-l', '--lock', nargs='?', dest='encrypt', type=int, const=8,
           metavar='N', help=argparse.SUPPRESS)

    # Power toys group
    power_grp = argparser.add_argument_group(
        title='power toys',
        description='''-e, --export file    export bookmarks to Firefox format html
-i, --import file    import bookmarks from html file; Firefox,
                     Google Chrome and IE formats supported
-m, --merge file     merge bookmarks from another buku database
-p, --print [N]      show details of bookmark at DB index N
                     show all bookmarks, if no arguments
-f, --format N       modify -p output
                     N=1: show only URL, N=2: show URL and tag
-r, --replace oldtag [newtag ...]
                     replace oldtag with newtag everywhere
                     delete oldtag, if no newtag
-j, --json           Json formatted output for -p, -s, -S, --st
--noprompt           do not show the prompt, run and exit
-o, --open N         open bookmark at DB index N in web browser
-z, --debug          show debug information and additional logs''')
    addarg = power_grp.add_argument
    addarg('-e', '--export', nargs=1, dest='export', metavar='file',
           help=argparse.SUPPRESS)
    addarg('-i', '--import', nargs=1, dest='imports', metavar='file',
           help=argparse.SUPPRESS)
    addarg('-m', '--merge', nargs=1, dest='merge', metavar='file',
           help=argparse.SUPPRESS)
    addarg('-p', '--print', nargs='?', dest='printindex', type=int, const=0,
           metavar='N', help=argparse.SUPPRESS)
    addarg('-f', '--format', dest='showOpt', type=int, default=0,
           choices=[1, 2], metavar='N', help=argparse.SUPPRESS)
    addarg('-r', '--replace', nargs='+', dest='replace',
           metavar=('oldtag', 'newtag'), help=argparse.SUPPRESS)
    addarg('-j', '--json', dest='jsonOutput', action='store_true',
           help=argparse.SUPPRESS)
    addarg('--noprompt', dest='noninteractive', action='store_true',
           help=argparse.SUPPRESS)
    addarg('-o', '--open', dest='openurl', type=int, metavar='N',
           help=argparse.SUPPRESS)
    addarg('-z', '--debug', dest='debug', action='store_true',
           help=argparse.SUPPRESS)

    # Show help and exit if no arguments
    if len(sys.argv) < 2:
        argparser.print_help(sys.stderr)
        sys.exit(1)

    # Parse the arguments
    args = argparser.parse_args()

    # Show help and exit if help requested
    if args.help:
        argparser.print_help(sys.stderr)
        sys.exit(0)

    # Assign the values to globals
    if tagManual is not None and len(args.tag) > 0:
        tagManual = args.tag
    if titleManual is not None and len(args.title) > 0:
        titleManual = ' '.join(args.title)
    if description is not None and len(args.desc) > 0:
        description = ' '.join(args.desc)
    if args.jsonOutput:
        import json
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('Version %s', _VERSION_)

    # Move pre-1.9 database to new location
    # BukuDb.move_legacy_dbfile()

    # Handle encrypt/decrypt options at top priority
    if args.encrypt is not None:
        BukuCrypt.encrypt_file(args.encrypt)

    if args.decrypt is not None:
        BukuCrypt.decrypt_file(args.decrypt)

    # Initialize the database and get handles
    bdb = BukuDb(args.noninteractive, args.jsonOutput, args.showOpt)

    # Add a record
    if args.addurl is not None:
        # Parse tags into a comma-separated string
        tags = DELIMITER
        keywords = args.addurl
        if tagManual is not None:
            if tagManual[0] == '+' and len(tagManual) == 1:
                pass
            elif tagManual[0] == '+':
                tagManual = tagManual[1:]
                # In case of add, args.addurl may have URL followed by tags
                # Add DELIMITER as url+tags may not end with comma
                keywords = args.addurl + [DELIMITER] + tagManual
            else:
                keywords = args.addurl + [DELIMITER] + tagManual

        if len(keywords) > 1:
            tags = parse_tags(keywords[1:])

        bdb.add_bookmark(args.addurl[0], titleManual, tags, description)

    # Update record
    if update:
        index_passed = None
        if len(args.update) == 0:
            index_passed = 0

        if args.url is not None:
            new_url = args.url[0]
        else:
            new_url = ''

        append = False
        delete = False
        if tagManual is not None:
            if (tagManual[0] == '+' or tagManual[0] == '-') \
                    and len(tagManual) == 1:
                logger.error('Please specify a tag')
                bdb.close_quit(1)
            elif tagManual[0] == '+':
                tagManual = tagManual[1:]
                append = True
            elif tagManual[0] == '-':
                tagManual = tagManual[1:]
                delete = True

        # Parse tags into a comma-separated string
        tags = parse_tags(tagManual)

        if index_passed is None:
            for idx in args.update:
                if is_int(idx):
                    bdb.update_bookmark(int(idx), new_url, titleManual, tags,
                                        description, append, delete)
                elif '-' in idx and is_int(idx.split('-')[0]) \
                        and is_int(idx.split('-')[1]):
                    lower = int(idx.split('-')[0])
                    upper = int(idx.split('-')[1])
                    if lower > upper:
                        lower, upper = upper, lower
                    for _id in range(lower, upper + 1):
                        bdb.update_bookmark(_id, new_url, titleManual, tags,
                                            description, append, delete)
        else:
            bdb.update_bookmark(index_passed, new_url, titleManual, tags,
                                description, append, delete)

    # Search URLs, titles, tags for any keyword and delete if wanted
    if args.sany is not None:
        bdb.searchdb(args.sany, False, (args.delete is not None), args.deep)

    # Search URLs, titles, tags with all keywords and delete if wanted
    elif args.sall is not None:
        if args.sall[0] == 'blank' and len(args.sall) == 1:
            bdb.print_bookmark(0, True)
        else:
            bdb.searchdb(args.sall, True, (args.delete is not None), args.deep)

    # Search bookmarks by tag and delete if wanted
    elif tagsearch:
        if len(args.stag) > 0:
            tag = '%s%s%s' % (DELIMITER, ' '.join(args.stag).strip(DELIMITER),
                              DELIMITER)
            bdb.search_by_tag(tag, (args.delete is not None))
        else:
            bdb.list_tags()

    # Just delete record(s)
    elif (args.delete is not None):
        if len(args.delete) == 0:
            bdb.delete_bookmark(0)
        elif len(args.delete) == 1 and '-' in args.delete[0]:
            vals = str(args.delete[0]).split('-')
            if len(vals) == 2 and is_int(vals[0]) and is_int(vals[1]):
                if int(vals[0]) == int(vals[1]):
                    bdb.delete_bookmark(int(vals[0]))
                elif int(vals[0]) < int(vals[1]):
                    bdb.delete_bookmark(0, int(vals[0]), int(vals[1]), True)
                else:
                    bdb.delete_bookmark(0, int(vals[1]), int(vals[0]), True)
            else:
                logger.error('Incorrect index or range')
                bdb.close_quit(1)
        else:
            ids = []
            # Select the unique indices
            for idx in args.delete:
                if idx not in ids:
                    ids += (idx,)

            try:
                # Index delete order - highest to lowest
                ids.sort(key=lambda x: int(x), reverse=True)
                for idx in ids:
                    bdb.delete_bookmark(int(idx))
            except ValueError as e:
                logger.error('Index should be numerical (>= 0)')

    # Print all records
    if args.printindex is not None:
        if args.printindex < 0:
            logger.error('Index must be >= 0')
            bdb.close_quit(1)
        bdb.print_bookmark(args.printindex)

    # Replace a tag in DB
    if args.replace is not None:
        if len(args.replace) == 1:
            bdb.replace_tag(args.replace[0])
        else:
            bdb.replace_tag(args.replace[0], args.replace[1:])

    # Export bookmarks
    if args.export is not None:
        bdb.export_bookmark(args.export[0])

    # Import bookmarks
    if args.imports is not None:
        bdb.import_bookmark(args.imports[0])

    # Merge a database file and exit
    if args.merge is not None:
        bdb.mergedb(args.merge[0])

    # Open URL in browser
    if args.openurl is not None:
        if args.openurl < 1:
            logger.error('Index must be >= 1')
            bdb.close_quit(1)
        bdb.browse_by_index(args.openurl)

    # Close DB connection and quit
    bdb.close_quit(0)
