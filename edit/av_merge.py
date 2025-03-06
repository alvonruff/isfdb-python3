#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1070 $
#     Date: $Date: 2023-01-05 17:56:54 -0500 (Thu, 05 Jan 2023) $


from isfdb import *
from isfdblib import *
from SQLparsing import *
from authorClass import authors

def Compare(field1, field2, fieldname):
        print('<tr class="generic_table_header">')
        if field1 != field2:
                print('<td class="drop">')
                print("<b>" +fieldname+ " Conflict:</b><br>")
                print('<INPUT TYPE="radio" NAME="' +fieldname+ '" VALUE="1" CHECKED>')
                if fieldname == 'author_note':
                        print(field1)
                else:
                        print(ISFDBText(field1))
                print('<br>')
                print('<INPUT TYPE="radio" NAME="' +fieldname+ '" VALUE="2">')
                if fieldname == 'author_note':
                        print(field2)
                else:
                        print(ISFDBText(field2))
        else:
                print('<td class="keep">')
                print("<b>Merged " +fieldname+ ": </b>", ISFDBText(field1))
        print('</td>')
        print('</tr>')

def Merge2(field1, field2, fieldname):
        print('<tr class="generic_table_header">')
        print('<td class="keep">')
        print('<b>Merged %s </b><br>' % fieldname)
        # Combine the two lists in a set, which removes duplicates, then print all values
        for value in set(field1 + field2):
                if value:
                        print(ISFDBText(value))
                        print('<br>')
        print('</td>')
        print('</tr>')

def SelectionError():
        print("<h2>Error: You need to select exactly two records to merge.</h2>")
        PrintPostSearch(0, 0, 0, 0, 0)
        sys.exit(0)


if __name__ == '__main__':
        ##################################################################
        # Output the leading HTML stuff
        ##################################################################
        PrintPreSearch("Merge Results")
        PrintNavBar(0, 0)

        ##################################################################
        # Gather the form input
        ##################################################################
        sys.stderr = sys.stdout
        form = IsfdbFieldStorage()
        if 'merge' in form:
                try:
                        recno1 = int(form['merge'][0].value)
                except:
                        SelectionError()
                try:
                        recno2 = int(form['merge'][1].value)
                except:
                        SelectionError()
                too_many_args = 0
                try:
                        recno3 = int(form['merge'][2].value)
                        too_many_args = 1
                except:
                        pass
                if too_many_args:
                        SelectionError()
                print("<h2>Merging Records %d and %d</h2>" % (recno1, recno2))
                print("<hr>")
        else:
                SelectionError()

        record1 = authors(db)
        record1.load(recno1)
        if not record1.author_id:
                SelectionError("Record %d no longer exists.</b>" % recno1)

        record2 = authors(db)
        record2.load(recno2)
        if not record2.author_id:
                SelectionError("Record %d no longer exists.</b>" % recno2)

        print('<form METHOD="POST" ACTION="/cgi-bin/edit/as_merge.cgi">')
        print('<table class="generic_table">')

        Compare(record1.author_canonical,   record2.author_canonical, "author_canonical")
        Merge2(record1.author_trans_names, record2.author_trans_names, "trans_names")
        Compare(record1.author_legalname,   record2.author_legalname, "author_legalname")
        Merge2(record1.author_trans_legal_names, record2.author_trans_legal_names, "trans_legal_names")
        Compare(record1.author_lastname,    record2.author_lastname,  "author_lastname")
        Compare(record1.author_birthplace,  record2.author_birthplace,"author_birthplace")
        Compare(record1.author_birthdate,   record2.author_birthdate, "author_birthdate")
        Compare(record1.author_deathdate,   record2.author_deathdate, "author_deathdate")
        Compare(record1.author_image,       record2.author_image,     "author_image")
        Compare(record1.author_language,    record2.author_language,  "author_language")
        Merge2(record1.author_emails,       record2.author_emails,    "author_emails")
        Merge2(record1.author_webpages,     record2.author_webpages,  "author_webpages")
        Compare(record1.author_note,        record2.author_note,      "author_note")
        print('</table>')
        print('<p>')

        print('<input NAME="record1" VALUE="%d" TYPE="HIDDEN">' % (recno1))
        print('<input NAME="record2" VALUE="%d" TYPE="HIDDEN">' % (recno2))
        print('<input TYPE="SUBMIT" VALUE="Complete Merge">')
        print('</form>')

        PrintPostSearch(0, 0, 0, 0, 0, 0)
