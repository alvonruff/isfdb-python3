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
        CNX = MYSQL_CONNECTOR()
        update_string =  '<?xml version="1.0" encoding="' +UNICODE+ '" ?>\n'
        update_string += "<IsfdbSubmission>\n"
        update_string += "  <NewPub>\n"
        update_string += "    <Submitter>%s</Submitter>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(submission.user.name)))
        update_string += "    <Subject>%s</Subject>\n" % (CNX.DB_ESCAPE_STRING(new.pub_title))
        
        if new.title_id:
                update_string += "    <Parent>%d</Parent>\n" % (int(new.title_id))

        if new.used_title:
                update_string += "    <Title>%s</Title>\n" % (CNX.DB_ESCAPE_STRING(new.pub_title))

        if new.used_trans_titles:
                update_string += "    <TransTitles>\n"
                for trans_title in new.pub_trans_titles:
                        update_string += "      <TransTitle>%s</TransTitle>\n" % (CNX.DB_ESCAPE_STRING(trans_title))
                update_string += "    </TransTitles>\n"

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
        if new.used_webpages:
                update_string += "    <PubWebpages>\n"
                for webpage in new.pub_webpages:
                        update_string += "         <PubWebpage>%s</PubWebpage>\n" % (CNX.DB_ESCAPE_STRING(webpage))
                update_string += "    </PubWebpages>\n"
        if new.used_note:
                update_string += "    <Note>%s</Note>\n" % (CNX.DB_ESCAPE_STRING(new.pub_note))

        #############################################################
        update_string += "    <Authors>\n"
        counter = 0
        while counter < new.num_authors:
                update_string += "      <Author>%s</Author>\n" % (CNX.DB_ESCAPE_STRING(new.pub_authors[counter]))
                counter += 1
        update_string += "    </Authors>\n"

        if new.num_artists:
                update_string += "    <Artists>\n"
                counter = 0
                while counter < new.num_artists:
                        update_string += "      <Artist>%s</Artist>\n" % (CNX.DB_ESCAPE_STRING(new.pub_artists[counter]))
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
                update_string += "    <Synopsis>%s</Synopsis>\n" % (CNX.DB_ESCAPE_STRING(newTitle.title_synop))

        if newTitle.title_note:
                update_string += "    <TitleNote>%s</TitleNote>\n" % (CNX.DB_ESCAPE_STRING(newTitle.title_note))

        if newTitle.title_language:
                update_string += "    <Language>%s</Language>\n" % (CNX.DB_ESCAPE_STRING(newTitle.title_language))

        if newTitle.title_series:
                update_string += "    <Series>%s</Series>\n" % (CNX.DB_ESCAPE_STRING(newTitle.title_series))

        if newTitle.title_seriesnum:
                update_string += "    <SeriesNum>%s</SeriesNum>\n" % (CNX.DB_ESCAPE_STRING(newTitle.title_seriesnum))

        if newTitle.title_content:
                update_string += "    <ContentIndicator>%s</ContentIndicator>\n" % (CNX.DB_ESCAPE_STRING(newTitle.title_content))

        if newTitle.title_jvn:
                update_string += "    <Juvenile>%s</Juvenile>\n" % (CNX.DB_ESCAPE_STRING(newTitle.title_jvn))

        if newTitle.title_nvz:
                update_string += "    <Novelization>%s</Novelization>\n" % (CNX.DB_ESCAPE_STRING(newTitle.title_nvz))

        if newTitle.title_non_genre:
                update_string += "    <NonGenre>%s</NonGenre>\n" % (CNX.DB_ESCAPE_STRING(newTitle.title_non_genre))

        if newTitle.title_graphic:
                update_string += "    <Graphic>%s</Graphic>\n" % (CNX.DB_ESCAPE_STRING(newTitle.title_graphic))

        if newTitle.used_webpages:
                update_string += "    <Webpages>\n"
                for webpage in newTitle.title_webpages:
                        update_string += "         <Webpage>%s</Webpage>\n" % (CNX.DB_ESCAPE_STRING(webpage))
                update_string += "    </Webpages>\n"

        # Retrieve the Source and the Mod Note values from the "form" dictionary, which was
        # created by IsfdbFieldStorage(), because they are not either in the Pub or in the Title class

        if 'Source' in new.form:
                update_string += "    <Source>%s</Source>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(new.form['Source'].value)))

        if 'mod_note' in new.form:
                update_string += "    <ModNote>%s</ModNote>\n" % (CNX.DB_ESCAPE_STRING(XMLescape(new.form['mod_note'].value)))

        # Get the Content data
        update_string += CNX.DB_ESCAPE_STRING(new.xmlContent())

        update_string += "  </NewPub>\n"
        update_string += "</IsfdbSubmission>\n"

        submission.file(update_string)
