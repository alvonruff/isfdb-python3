#
#    (C) COPYRIGHT 2019   ErsatzCulture
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 419 $
#     Date: $Date: 2019-10-20 10:54:53 -0400 (Wed, 15 May 2019) $
"""
Report on or remove records in the canonical_author table that point at
non-existent authors.

Usage:
  remove_orphaned_canonical_authors.py # Dry-run reporting by default
  remove_orphaned_canonical_authors.py -d # Actually delete the orphaned records

Background:
  https://sourceforge.net/p/isfdb/bugs/739/

"""

import getopt
from localdefs import (DBASEHOST, USERNAME, PASSWORD, DBASE, HTFAKE)
import MySQLdb
import sys

def Date_or_None(s):
        return s

def IsfdbConvSetup():
        import MySQLdb.converters
        IsfdbConv = MySQLdb.converters.conversions
        IsfdbConv[10] = Date_or_None
        return(IsfdbConv)


def print_usage():
        print('%s [-h] [-d]' % __file__)
        print('Report on or delete orphaned canonical_author records')
        print(' -d : Delete the orphaned records (default behaviour is dry-run/report only)')
        print(' -h : Print this help information')


BASE_QUERY = '''SELECT ca.ca_id, ca.title_id, ca.author_id
                FROM canonical_author ca
                LEFT OUTER JOIN authors a ON a.author_id = ca.author_id
                WHERE author_canonical IS NULL'''

PROTOCOL_PREFIX = 'http:/'
URL_BASE = '%s%s' % (PROTOCOL_PREFIX, HTFAKE)
TITLE_URL_FORMAT = URL_BASE + '/title.cgi?%d'
AUTHOR_URL_FORMAT = URL_BASE + '/ea.cgi?%d'

def report_orphaned_authors(db, print_to_screen=True):
        db.query(BASE_QUERY)
        result = db.store_result()
        record = result.fetch_row()
        i = 0
        orphaned_ca_ids = []
        while record:
                i += 1
                rec = record[0]
                if print_to_screen:
                        print('%d. canonical_author record with ca_id=%d is orphaned; '
                              'title URL is %s , (broken) author URL is/was %s' %
                              (i, rec[0],
                               TITLE_URL_FORMAT % (rec[1]),
                               AUTHOR_URL_FORMAT % (rec[2])))
                orphaned_ca_ids.append(rec[0])
                record = result.fetch_row()
        if not orphaned_ca_ids and print_to_screen:
                print('No orphaned records found in canonical_author')
        return orphaned_ca_ids


def delete_orphaned_authors(db):
        # I tried doing this in one hit as
        # DELETE FROM canonical_author WHERE ca_id in (SELECT ...)
        # but MySQL/MariaDB doesn't like it (ERROR 1093 (HY000), hence getting
        # the IDs and then doing the delete.
        ca_ids_to_delete = report_orphaned_authors(db, print_to_screen=False)
        if not ca_ids_to_delete:
                print('No orphaned records to delete!')
                return

        stringified_ids = ', '.join([str(z) for z in ca_ids_to_delete])

        query = 'DELETE FROM canonical_author WHERE ca_id in (%s);' % (stringified_ids)
        print('Executing %s' % (query))
        db.query(query)


if __name__ == '__main__':
        try:
                opts, _ = getopt.getopt(sys.argv[1:], 'dh')
        except getopt.GetoptError, err:
                print('Argument handling error: %s' % (err))
                sys.exit(1)
        opt_dict = dict(opts)
        if '-h' in opt_dict:
                print_usage()
                sys.exit(0)

        db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
        db.select_db(DBASE)
        if '-d' in opt_dict:
                delete_orphaned_authors(db)
        else:
                report_orphaned_authors(db)
        db.close()
