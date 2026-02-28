#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2026   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1259 $
#     Date: $Date: 2026-02-15 16:59:31 -0500 (Sun, 15 Feb 2026) $

        
import cgi
import sys
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
        CNX = MYSQL_CONNECTOR()
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <NewPub>\n"
        if record:
                update_string += "    <ClonedTo>%d</ClonedTo>\n" % (record)
        update_string += "    <Submitter>%s</Submitter>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name)))
        update_string += "    <Subject>%s</Subject>\n" % (CNX.DB_ESCAPE_STRING(new.pub_title))
        
        if new.title_id:
                update_string += "    <Parent>%s</Parent>\n" % (CNX.DB_ESCAPE_STRING(new.title_id))

        if cloned_pub_id:
                update_string += "    <ClonedPubID>%d</ClonedPubID>\n" % cloned_pub_id

        if new.used_title:
                update_string += "    <Title>%s</Title>\n" % (CNX.DB_ESCAPE_STRING(new.pub_title))

        if new.used_trans_titles:
                update_string += "    <TransTitles>\n"
                for trans_title in new.pub_trans_titles:
                        update_string += "      <TransTitle>%s</TransTitle>\n" % (CNX.DB_ESCAPE_STRING(trans_title))
                update_string += "    </TransTitles>\n"

        # Web pages
        if new.used_webpages:
                update_string += "    <Webpages>\n"
                for webpage in new.pub_webpages:
                        update_string += "         <Webpage>%s</Webpage>\n" % (CNX.DB_ESCAPE_STRING(webpage))
                update_string += "    </Webpages>\n"

        if new.used_tag:
                update_string += "    <Tag>%s</Tag>\n" % (CNX.DB_ESCAPE_STRING(new.pub_tag))
        if new.used_year:
                update_string += "    <Year>%s</Year>\n" % (CNX.DB_ESCAPE_STRING(new.pub_year))
        if new.used_publisher:
                update_string += "    <Publisher>%s</Publisher>\n" % (CNX.DB_ESCAPE_STRING(new.pub_publisher))
        if new.used_series:
                update_string += "    <PubSeries>%s</PubSeries>\n" % (CNX.DB_ESCAPE_STRING(new.pub_series))
        if new.used_series_num:
                update_string += "    <PubSeriesNum>%s</PubSeriesNum>\n" % (CNX.DB_ESCAPE_STRING(new.pub_series_num))
        if new.used_pages:
                update_string += "    <Pages>%s</Pages>\n" % (CNX.DB_ESCAPE_STRING(new.pub_pages))
        if new.used_ptype:
                update_string += "    <Binding>%s</Binding>\n" % (CNX.DB_ESCAPE_STRING(new.pub_ptype))
        if new.used_ctype:
                update_string += "    <PubType>%s</PubType>\n" % (CNX.DB_ESCAPE_STRING(new.pub_ctype))
        if new.used_isbn:
                update_string += "    <Isbn>%s</Isbn>\n" % (CNX.DB_ESCAPE_STRING(new.pub_isbn))
        if new.used_catalog:
                update_string += "    <Catalog>%s</Catalog>\n" % (CNX.DB_ESCAPE_STRING(new.pub_catalog))

        if new.identifiers:
                update_string += new.xmlIdentifiers()

        if new.used_price:
                update_string += "    <Price>%s</Price>\n" % (CNX.DB_ESCAPE_STRING(new.pub_price))
        if new.used_image:
                update_string += "    <Image>%s</Image>\n" % (CNX.DB_ESCAPE_STRING(new.pub_image))
        if new.used_note:
                update_string += "    <Note>%s</Note>\n" % (CNX.DB_ESCAPE_STRING(new.pub_note))
        if 'mod_note' in new.form:
                update_string += "    <ModNote>%s</ModNote>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(new.form['mod_note'].value)))

        if 'Source' in new.form:
                update_string += "    <Source>%s</Source>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(new.form['Source'].value)))

        #############################################################
        update_string += "    <Authors>\n"
        counter = 0
        while counter < new.num_authors:
                update_string += "      <Author>%s</Author>\n" % (CNX.DB_ESCAPE_STRING(new.pub_authors[counter]))
                counter += 1
        update_string += "    </Authors>\n"

        update_string += CNX.DB_ESCAPE_STRING(new.xmlCloneContent())

        update_string += "  </NewPub>\n"
        update_string += "</IsfdbSubmission>\n"
        
        submission.file(update_string)
