#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2008-2026   Al von Ruff, Bill Longley, Ahasuerus and Klaus Elsbernd
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1260 $
#     Date: $Date: 2026-02-18 08:27:14 -0500 (Wed, 18 Feb 2026) $


from isfdb import *
from common import *
from isfdblib import *
from SQLparsing import *
from publisherClass import publishers
from library import *
from xml.dom import minidom
from xml.dom import Node


def doColumn(KeepId, merge, label, column):
        # Retrieve the ID of the publisher whose data will be used for this field
        selected_id = GetElementValue(merge, label)
        if not selected_id:
                return
        # If the editor chose to use the to-be-kept publisher's data for this
        # field, then there is no need to move the data and this function is done
        if selected_id == KeepId:
                return

        # Retrieve the current value of this field for the to-be-kept publisher;
        # it will be used later (currently for Notes only)
        query = "select %s from publishers where publisher_id=%d" % (column, int(KeepId))
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        old_value = record[0][0]
        
        # Retrieve the current value for this field for the publisher whose data
        # the editor chose to use for this field
        query = "select %s from publishers where publisher_id=%d" % (column, int(selected_id))
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        new_value = record[0][0]
        
        # Update the to-be-kept publisher with the retrieved data
        if new_value:
                update = "update publishers set %s='%s' where publisher_id=%d" % (column, CNX.DB_ESCAPE_STRING(str(new_value)), int(KeepId))
        else:
                update = "update publishers set %s=NULL where publisher_id=%d" % (column, int(KeepId))
        print("<li> ", update)
        CNX.DB_QUERY(update)

        if label == 'Note':
                # Delete the Note record that was originally associated with the to-be-kept publisher (if exists)
                if old_value:
                        update = "delete from notes where note_id=%d" % int(old_value)
                        print("<li> ", update)
                        CNX.DB_QUERY(update)
                
                # Blank out the note ID in the to-be-dropped publisher record so that when
                # it is deleted later on, the deletion process won't try to delete the Note record
                update = "update publishers set %s=NULL where publisher_id=%d" % (column, int(selected_id))
                print("<li> ", update)
                CNX.DB_QUERY(update)

def PublisherMerge(doc, merge):
        KeepId = GetElementValue(merge, 'KeepId')

        # Update all fields in the to-be-kept publisher record with any
        # data that the editor chose to copy from the to-be-dropped
        # publishers
        doColumn(KeepId, merge, 'Publisher', 'publisher_name')
        doColumn(KeepId, merge, 'Note',         'note_id')

        # Load the data for the publisher that we will keep
        keep_publisher = publishers(db)
        keep_publisher.load(KeepId)

        # Load the IDs of the publishers that we will drop
        dropped_ids = []
        for dropid in doc.getElementsByTagName('DropId'):
                dropped_ids.append(int(dropid.firstChild.data))

        CNX = MYSQL_CONNECTOR()
        for dropped_id in dropped_ids:
                # Repoint all publications from this to-be-dropped publisher to the to-be-kept publisher
                update = "update pubs set publisher_id=%d where publisher_id=%d" % (int(KeepId), dropped_id)
                print("<li> ", update)
                CNX.DB_QUERY(update)

                # Load the current data for the to-be-dropped publisher
                drop_publisher = publishers(db)
                drop_publisher.load(dropped_id)

                for webpage in drop_publisher.publisher_webpages:
                        # If this web page is not already associated with the publisher that we will keep,
                        # then insert it into the table for the to-be-kept publisher
                        if webpage not in keep_publisher.publisher_webpages:
                                update = """insert into webpages(publisher_id, url)
                                values(%d, '%s')""" % (int(KeepId), CNX.DB_ESCAPE_STRING(webpage))
                                CNX.DB_QUERY(update)
                                print("<li> ", update)

                for publisher_trans_name in drop_publisher.publisher_trans_names:
                        # If this transliterated name is not already associated with the publisher that we will keep,
                        # then insert it into the table for the to-be-kept publisher
                        if publisher_trans_name not in keep_publisher.publisher_trans_names:
                                update = """insert into trans_publisher(publisher_id, trans_publisher_name)
                                values(%d, '%s')""" % (int(KeepId), CNX.DB_ESCAPE_STRING(publisher_trans_name))
                                CNX.DB_QUERY(update)
                                print("<li> ", update)
                # Delete the to-be-dropped publisher
                drop_publisher.delete()
        return KeepId

if __name__ == '__main__':

        submission = SESSION.Parameter(0, 'int')

        PrintPreMod('Publisher Merge - SQL Statements')
        PrintNavBar()

        if NotApprovable(submission):
                sys.exit(0)

        print("<h1>SQL Updates:</h1>")
        print("<hr>")
        print("<ul>")

        KeepId = ''
        xml = SQLloadXML(submission)
        doc = minidom.parseString(XMLunescape2(xml))
        if doc.getElementsByTagName('PublisherMerge'):
                merge = doc.getElementsByTagName('PublisherMerge')
                if merge:
                        KeepId = PublisherMerge(doc, merge)
                        submitter = GetElementValue(merge, 'Submitter')
                        markIntegrated(db, submission, KeepId)
        if not KeepId:
                print('<div id="ErrorBox">')
                print('<h3>Error: Publisher ID not specified</h3>')
                print('</div>')
                PrintPostMod()
                sys.exit(0)

        print(ISFDBLinkNoName('publisher.cgi', KeepId, 'View Publisher', True))
        print(ISFDBLinkNoName('edit/editpublisher.cgi', KeepId, 'Edit Publisher', True))
        print('<hr>')

        PrintPostMod(0)
