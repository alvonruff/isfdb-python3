#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1099 $
#     Date: $Date: 2023-02-07 18:29:53 -0500 (Tue, 07 Feb 2023) $

        
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from pubClass import *
from titleClass import *
from SQLparsing import *
from login import *
from library import *
from navbar import *

        
if __name__ == '__main__':

        submission = Submission()
        submission.header = 'New Publication Submission'
        submission.cgi_script = 'newpub'
        submission.type = MOD_PUB_NEW

        new = pubs(db)
        new.cgi2obj('implied')
        if new.error:
                submission.error(new.error)

        if not submission.user.id:
                submission.error('', 1)

        changes = 0
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <NewPub>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % (db.escape_string(XMLescape(submission.user.name)))
        update_string += "    <Subject>%s</Subject>\n" % (db.escape_string(new.pub_title))
        
        if new.title_id:
                update_string += "    <Parent>%d</Parent>\n" % (int(new.title_id))

        if new.used_title:
                update_string += "    <Title>%s</Title>\n" % (db.escape_string(new.pub_title))

        if new.used_trans_titles:
                update_string += "    <TransTitles>\n"
                for trans_title in new.pub_trans_titles:
                        update_string += "      <TransTitle>%s</TransTitle>\n" % (db.escape_string(trans_title))
                update_string += "    </TransTitles>\n"

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
        if new.used_webpages:
                update_string += "    <PubWebpages>\n"
                for webpage in new.pub_webpages:
                        update_string += "         <PubWebpage>%s</PubWebpage>\n" % (db.escape_string(webpage))
                update_string += "    </PubWebpages>\n"
        if new.used_note:
                update_string += "    <Note>%s</Note>\n" % (db.escape_string(new.pub_note))

        #############################################################
        update_string += "    <Authors>\n"
        counter = 0
        while counter < new.num_authors:
                update_string += "      <Author>%s</Author>\n" % (db.escape_string(new.pub_authors[counter]))
                counter += 1
        update_string += "    </Authors>\n"

        if new.num_artists:
                update_string += "    <Artists>\n"
                counter = 0
                while counter < new.num_artists:
                        update_string += "      <Artist>%s</Artist>\n" % (db.escape_string(new.pub_artists[counter]))
                        counter += 1
                update_string += "    </Artists>\n"

        # Instantiate the Title class and perform validation of Title-specific fields
        newTitle = titles(db)
        # Copy the form value from the Pub object to the Title object
        newTitle.form = new.form
        # Copy the Publication type to the Title type in order to allow CHAPBOOK-specific validation
        newTitle.title_ttype = new.pub_ctype
        # Call the validation method of the Title class
        newTitle.validateOptional()
        if newTitle.error:
                submission.error(newTitle.error)

        if newTitle.title_synop:
                update_string += "    <Synopsis>%s</Synopsis>\n" % (db.escape_string(newTitle.title_synop))

        if newTitle.title_note:
                update_string += "    <TitleNote>%s</TitleNote>\n" % (db.escape_string(newTitle.title_note))

        if newTitle.title_language:
                update_string += "    <Language>%s</Language>\n" % (db.escape_string(newTitle.title_language))

        if newTitle.title_series:
                update_string += "    <Series>%s</Series>\n" % (db.escape_string(newTitle.title_series))

        if newTitle.title_seriesnum:
                update_string += "    <SeriesNum>%s</SeriesNum>\n" % (db.escape_string(newTitle.title_seriesnum))

        if newTitle.title_content:
                update_string += "    <ContentIndicator>%s</ContentIndicator>\n" % (db.escape_string(newTitle.title_content))

        if newTitle.title_jvn:
                update_string += "    <Juvenile>%s</Juvenile>\n" % (db.escape_string(newTitle.title_jvn))

        if newTitle.title_nvz:
                update_string += "    <Novelization>%s</Novelization>\n" % (db.escape_string(newTitle.title_nvz))

        if newTitle.title_non_genre:
                update_string += "    <NonGenre>%s</NonGenre>\n" % (db.escape_string(newTitle.title_non_genre))

        if newTitle.title_graphic:
                update_string += "    <Graphic>%s</Graphic>\n" % (db.escape_string(newTitle.title_graphic))

        if newTitle.used_webpages:
                update_string += "    <Webpages>\n"
                for webpage in newTitle.title_webpages:
                        update_string += "         <Webpage>%s</Webpage>\n" % (db.escape_string(webpage))
                update_string += "    </Webpages>\n"

        # Retrieve the Source and the Mod Note values from the "form" dictionary, which was
        # created by cgi.FieldStorage, because they are not either in the Pub or in the Title class

        if new.form.has_key('Source'):
                update_string += "    <Source>%s</Source>\n" % (db.escape_string(XMLescape(new.form['Source'].value)))

        if new.form.has_key('mod_note'):
                update_string += "    <ModNote>%s</ModNote>\n" % (db.escape_string(XMLescape(new.form['mod_note'].value)))

        # Get the Content data
        update_string += db.escape_string(new.xmlContent())

        update_string += "  </NewPub>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
