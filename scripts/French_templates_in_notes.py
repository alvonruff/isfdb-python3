#!_PYTHONLOC
#
#     (C) COPYRIGHT 2023   Ahasuerus
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
import MySQLdb
from localdefs import *

def Date_or_None(s):
        return s

def IsfdbConvSetup():
        import MySQLdb.converters
        IsfdbConv = MySQLdb.converters.conversions
        IsfdbConv[10] = Date_or_None
        return(IsfdbConv)


if __name__ == '__main__':

        db = MySQLdb.connect(DBASEHOST, USERNAME, PASSWORD, conv=IsfdbConvSetup())
        db.select_db(DBASE)

        query = """select p.pub_id, n.note_id, n.note_note from notes n, pubs p
             where p.note_id = n.note_id
             and n.note_note like \"%Acheve D'Imprimer%"\
             and n.note_note not like \"%{{Acheve D'Imprimer}}%\""""
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        num = result.num_rows()
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
                update = """update notes set note_note = '%s' where note_id = %d""" % (db.escape_string(new_note), int(note_id))
                db.query(update)
                record = result.fetch_row()
        print count

        query = """select p.pub_id, n.note_id, n.note_note from notes n, pubs p
                   where p.note_id = n.note_id
                   and n.note_note like '%Depot Legal%'
                   and n.note_note not like '%{{Depot Legal}}%'"""
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        num = result.num_rows()
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
                update = """update notes set note_note = '%s' where note_id = %d""" % (db.escape_string(new_note), int(note_id))
                db.query(update)
                record = result.fetch_row()
        print count
        
