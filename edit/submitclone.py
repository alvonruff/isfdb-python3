#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1061 $
#     Date: $Date: 2022-12-27 13:43:52 -0500 (Tue, 27 Dec 2022) $

        
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from pubClass import *
from SQLparsing import *
from login import *
from library import *
from navbar import *
        

if __name__ == '__main__':

        submission = Submission()
        submission.header = 'Publication Clone/Import/Export Submission'
        submission.cgi_script = 'clonepub'
        submission.type = MOD_PUB_CLONE

        new = pubs(db)
        new.cgi2obj('ignore')
        if new.error:
                submission.error(new.error)

        if 'child_id' in new.form:
                record = int(new.form['child_id'].value)
        else:
                record = 0

        cloned_pub_id = int(new.form['pub_id'].value)

        if not submission.user.id:
                submission.error()
        
        changes = 0
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <NewPub>\n"
        if record:
                update_string += "    <ClonedTo>%d</ClonedTo>\n" % (record)
        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(new.pub_title))
        
        if new.title_id:
                update_string += "    <Parent>%s</Parent>\n" % (db.escape_string(new.title_id))

        if cloned_pub_id:
                update_string += "    <ClonedPubID>%d</ClonedPubID>\n" % cloned_pub_id

        if new.used_title:
                update_string += "    <Title>%s</Title>\n" % (db.escape_string(new.pub_title))

        if new.used_trans_titles:
                update_string += "    <TransTitles>\n"
                for trans_title in new.pub_trans_titles:
                        update_string += "      <TransTitle>%s</TransTitle>\n" % (db.escape_string(trans_title))
                update_string += "    </TransTitles>\n"

        # Web pages
        if new.used_webpages:
                update_string += "    <Webpages>\n"
                for webpage in new.pub_webpages:
                        update_string += "         <Webpage>%s</Webpage>\n" % (db.escape_string(webpage))
                update_string += "    </Webpages>\n"

        if new.used_tag:
                update_string += "    <Tag>%s</Tag>\n" % (db.escape_string(new.pub_tag))
        if new.used_year:
                update_string += "    <Year>%s</Year>\n" % (db.escape_string(new.pub_year))
        if new.used_publisher:
                update_string += "    <Publisher>%s</Publisher>\n" % (db.escape_string(new.pub_publisher))
        if new.used_series:
                update_string += "    <PubSeries>%s</PubSeries>\n" % (db.escape_string(new.pub_series))
        if new.used_series_num:
                update_string += "    <PubSeriesNum>%s</PubSeriesNum>\n" % (db.escape_string(new.pub_series_num))
        if new.used_pages:
                update_string += "    <Pages>%s</Pages>\n" % (db.escape_string(new.pub_pages))
        if new.used_ptype:
                update_string += "    <Binding>%s</Binding>\n" % (db.escape_string(new.pub_ptype))
        if new.used_ctype:
                update_string += "    <PubType>%s</PubType>\n" % (db.escape_string(new.pub_ctype))
        if new.used_isbn:
                update_string += "    <Isbn>%s</Isbn>\n" % (db.escape_string(new.pub_isbn))
        if new.used_catalog:
                update_string += "    <Catalog>%s</Catalog>\n" % (db.escape_string(new.pub_catalog))

        if new.identifiers:
                update_string += new.xmlIdentifiers()

        if new.used_price:
                update_string += "    <Price>%s</Price>\n" % (db.escape_string(new.pub_price))
        if new.used_image:
                update_string += "    <Image>%s</Image>\n" % (db.escape_string(new.pub_image))
        if new.used_note:
                update_string += "    <Note>%s</Note>\n" % (db.escape_string(new.pub_note))
        if 'mod_note' in new.form:
                update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(new.form['mod_note'].value)))

        if 'Source' in new.form:
                update_string += "    <Source>%s</Source>\n" % (db.escape_string(XMLescape(new.form['Source'].value)))

        #############################################################
        update_string += "    <Authors>\n"
        counter = 0
        while counter < new.num_authors:
                update_string += "      <Author>%s</Author>\n" % (db.escape_string(new.pub_authors[counter]))
                counter += 1
        update_string += "    </Authors>\n"

        update_string += db.escape_string(new.xmlCloneContent())

        update_string += "  </NewPub>\n"
        update_string += "</IsfdbSubmission>\n"
        
        submission.file(update_string)
