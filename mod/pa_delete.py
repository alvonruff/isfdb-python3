#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 677 $
#     Date: $Date: 2021-07-05 18:24:28 -0400 (Mon, 05 Jul 2021) $


from isfdb import *
from isfdblib import *
from common import *
from pubClass import *
from pubseriesClass import pub_series
from publisherClass import publishers
from titleClass import *
from SQLparsing import *
from library import *


def doError(message):
        print('<div id="ErrorBox">')
        print('<h3>Error: %s</h3>' % message)
        print('</div>')
        PrintPostMod()
        sys.exit(0)


def deleteAuthor(author_id, pub_id):
        ##############################################
        # STEP 1 - Delete the author entry for this
        #          publication from pub_authors
        ##############################################
        query = "delete from pub_authors where author_id=%d and pub_id=%d" % (author_id, pub_id)
        print("<li> ", query)
        db.query(query)

        ##############################################
        # STEP 2 - If the author still has an entry
        #          in one of the mapping tables, done
        ##############################################
        for i in ['canonical_author', 'pub_authors']:
                query = 'select COUNT(author_id) from %s where author_id=%d' % (i, author_id)
                print("<li> ", query)
                db.query(query)
                res = db.store_result()
                record = res.fetch_row()
                if record[0][0]:
                        return

        ##############################################
        # STEP 3 - If no record references the author,
        #          delete it
        ##############################################
        deleteFromAuthorTable(author_id)



if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Publication Delete - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")
        print("<ul>")

        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))

        if doc.getElementsByTagName('PubDelete'):
                merge = doc.getElementsByTagName('PubDelete')
                Record = GetElementValue(merge, 'Record')
                pub = pubs(db)
                pub.load(int(Record))
                if pub.error:
                        doError('Publication no longer exists. This submission should be hard-rejected.')

                ##########################################################
                # Delete Any Associated Note
                ##########################################################
                query = 'select note_id from pubs where pub_id=%d and note_id is not null' % int(Record)
                db.query(query)
                res = db.store_result()
                if res.num_rows():
                        rec = res.fetch_row()
                        note_id = rec[0][0]
                        update = "delete from notes where note_id=%d" % (note_id)
                        print("<li> ", update)
                        db.query(update)

                ##########################################################
                # Delete Any Stranded Authors
                ##########################################################
                query = """select a.author_id from authors a, pub_authors pa
                        where a.author_id=pa.author_id and pa.pub_id=%d""" % (int(Record))
                db.query(query)
                res = db.store_result()
                author = res.fetch_row()
                while author:
                        deleteAuthor(int(author[0][0]), int(Record))
                        author = res.fetch_row()

                #########################################
                # Find coverart records for this pub
                #########################################
                query = """select t.* from titles t, pub_content pc
                        where pc.pub_id=%d and pc.title_id=t.title_id""" % int(Record)
                db.query(query)
                res = db.store_result()
                titlerec = res.fetch_row()
                coverart_titles = []
                while titlerec:
                        if titlerec[0][TITLE_TTYPE] == 'COVERART':
                                coverart_titles.append(titlerec[0][TITLE_PUBID])
                        titlerec = res.fetch_row()

                ##########################################################
                # Delete pub/title map entries for this pub
                ##########################################################
                query = "delete from pub_content where pub_id=%d" % (int(Record))
                print("<li> ", query)
                db.query(query)

                # Delete COVERART titles for this title. The "delete" method
                # will check if any COVEART titles are used in another pub
                # and, if they are, will not delete them.
                for coverart_title in coverart_titles:
                        title = titles(db)
                        title.load(int(coverart_title))
                        title.delete()

                ##########################################################
                # Delete primary and secondary verifications for this pub
                ##########################################################
                query = "delete from primary_verifications where pub_id=%d" % int(Record)
                print("<li> ", query)
                db.query(query)
                query = "delete from verification where pub_id=%d" % int(Record)
                print("<li> ", query)
                db.query(query)

                # Delete transliterated titles 
                query = "delete from trans_pubs where pub_id=%d" % int(Record)
                print("<li> ", query)
                db.query(query)

                # Delete Web Pages
                query = "delete from webpages where pub_id=%d" % int(Record)
                print("<li> ", query)
                db.query(query)

                # Delete external identifiers
                query = "delete from identifiers where pub_id=%d" % int(Record)
                print("<li> ", query)
                db.query(query)

                # Delete the pub itself
                query = "delete from pubs where pub_id=%d" % int(Record)
                print("<li> ", query)
                db.query(query)

                # Delete Publication Series if there are no more pubs for it
                if pub.pub_series_id:
                        pubseries = pub_series(db)
                        pubseries.load(pub.pub_series_id)
                        pubseries.delete()

                # Delete Publisher if there are no more pubs for it
                if pub.pub_publisher_id:
                        publisher = publishers(db)
                        publisher.load(pub.pub_publisher_id)
                        publisher.delete()

                submitter = GetElementValue(merge, 'Submitter')
                markIntegrated(db, submission, Record)

        print("<p>")

        PrintPostMod(0)
