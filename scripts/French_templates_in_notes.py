#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2023-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1.3 $
#     Date: $Date: 2017/05/28 02:28:03 $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

if __name__ == '__main__':

        query = """select p.pub_id, n.note_id, n.note_note from notes n, pubs p
             where p.note_id = n.note_id
             and n.note_note like \"%Acheve D'Imprimer%"\
             and n.note_note not like \"%{{Acheve D'Imprimer}}%\""""

        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        # num = CNX.DB_NUMROWS()
        count = 0
        while record:
                pub_id = record[0][0]
                note_id = record[0][1]
                current_note = record[0][2]
                new_note = current_note
                templatized_string = '{{%s}}' % ("Achev%s D'Imprimer" % chr(233))
                for substitute in ("Achev%s D'Imprimer" % chr(233),
                                   "Achev%s d'imprimer" % chr(233),
                                   "achev%s d'imprimer" % chr(233)):
                        new_note = new_note.replace(substitute, templatized_string)
                count += 1
                update = """update notes set note_note = '%s' where note_id = %d""" % (CNX.DB_ESCAPE_STRING(new_note), int(note_id))
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)
                record = CNX.DB_FETCHMANY()
        print(count)

        query = """select p.pub_id, n.note_id, n.note_note from notes n, pubs p
                   where p.note_id = n.note_id
                   and n.note_note like '%Depot Legal%'
                   and n.note_note not like '%{{Depot Legal}}%'"""
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        # num = CNX.DB_NUMROWS()
        count = 0
        while record:
                pub_id = record[0][0]
                note_id = record[0][1]
                current_note = record[0][2]
                new_note = current_note
                templatized_string = '{{%s}}' % ('D%sp%st L%sgal' % (chr(233), chr(244), chr(233)))
                for substitute in ('D%sp%st L%sgal' % (chr(233), chr(244), chr(233)),
                                   'D%sp%st l%sgal' % (chr(233), chr(244), chr(233)),
                                   'd%sp%st l%sgal' % (chr(233), chr(244), chr(233)),
                                   'd%spot legal' % chr(233),
                                   'dep%st legal' % chr(244),
                                   'dep%st legal' % chr(243),
                                   'Depot Legal',
                                   'depot legal',
                                   'Depot legal'):
                        new_note = new_note.replace(substitute, templatized_string)
                count += 1
                update = """update notes set note_note = '%s' where note_id = %d""" % (CNX.DB_ESCAPE_STRING(new_note), int(note_id))
                if debug == 0:
                        CNX.DB_QUERY(update)
                else:
                        print(update)
                record = CNX.DB_FETCHMANY()
        print(count)
        
