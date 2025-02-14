#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2015-2025   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 726 $
#     Date: $Date: 2021-08-31 11:23:49 -0400 (Tue, 31 Aug 2021) $


from SQLparsing import *
from common import *
from library import *
from login import *


class notes:
        def __init__(self):
                # The default display value is 'Note'; it may be
                # overriden later on for Synopses and possibly other records
                self.note_type ='Note'
                self.cgi_script = ''
                self.record_title = ''
                self.note_body = ''
                self.record_name = ''

        def Author(self, author_id):
                from authorClass import authors
                author = authors(db)
                author.load(author_id)
                self.cgi_script = 'ea'
                self.record_title = author.author_canonical
                self.note_body = author.author_note
                self.record_name = 'Author'

        def Title(self, title_id):
                from titleClass import titles
                title = titles(db)
                title.load(title_id)
                self.cgi_script = 'title'
                self.record_title = title.title_title
                self.note_body = title.title_note
                self.record_name = 'Title'

        def Synopsis(self, title_id):
                from titleClass import titles
                title = titles(db)
                title.load(title_id)
                self.note_type = 'Synopsis'
                self.cgi_script = 'title'
                self.record_title = title.title_title
                self.note_body = title.title_synop
                self.record_name = 'Title'

        def Series(self, series_id):
                from seriesClass import series
                ser = series(db)
                ser.load(series_id)
                self.cgi_script = 'pe'
                self.record_title = ser.series_name
                self.note_body = ser.series_note
                self.record_name = 'Series'

        def SeriesGrid(self, series_id):
                from seriesClass import series
                ser = series(db)
                ser.load(series_id)
                self.cgi_script = 'seriesgrid'
                self.record_title = ser.series_name
                self.note_body = ser.series_note
                self.record_name = 'Series grid'

        def Award(self, award_id):
                from awardClass import awards
                award = awards(db)
                award.load(award_id)
                self.cgi_script = 'award_details'
                self.record_title = award.award_title
                self.note_body = award.award_note
                self.record_name = 'Award'

        def AwardCat(self, award_cat_id):
                from awardcatClass import award_cat
                aw_cat = award_cat()
                aw_cat.award_cat_id = award_cat_id
                aw_cat.load()
                self.cgi_script = 'award_category'
                self.record_title = aw_cat.award_cat_name
                self.note_body = aw_cat.award_cat_note
                self.record_name = 'Award Category'

        def AwardType(self, award_type_id):
                from awardtypeClass import award_type
                aw_type = award_type()
                aw_type.award_type_id = award_type_id
                aw_type.load()
                self.cgi_script = 'awardtype'
                self.record_title = aw_type.award_type_name
                self.note_body = aw_type.award_type_note
                self.record_name = 'Award Type'

        def Publication(self, pub_id):
                from pubClass import pubs
                pub = pubs(db)
                pub.load(pub_id)
                self.cgi_script = 'pl'
                self.record_title = pub.pub_title
                self.note_body = pub.pub_note
                self.record_name = 'Publication'

        def Publisher(self, publisher_id):
                from publisherClass import publishers
                publisher = publishers(db)
                publisher.load(publisher_id)
                self.cgi_script = 'publisher'
                self.record_title = publisher.publisher_name
                self.note_body = publisher.publisher_note
                self.record_name = 'Publisher'

        def Pubseries(self, pubseries_id):
                from pubseriesClass import pub_series
                pubseries = pub_series(db)
                pubseries.load(pubseries_id)
                self.cgi_script = 'pubseries'
                self.record_title = pubseries.pub_series_name
                self.note_body = pubseries.pub_series_note
                self.record_name = 'Publication Series'


if __name__ == '__main__':

        record_type = SESSION.Parameter(0, 'str')
        record_id = SESSION.Parameter(1, 'int')
        note = notes()
        methodToCall = getattr(notes, record_type, None)
        if methodToCall is None:
                SESSION.DisplayError('Record Type Does Not Exist')
        methodToCall(note, record_id)
        if not note.note_body:
                SESSION.DisplayError('Record Does Not Exist')

        PrintHeader('Full %s for %s: %s' % (note.note_type, note.record_name, note.record_title))
        PrintNavbar('note', 0, 0, 'note.cgi', 0)

        print(FormatNote(note.note_body, note.note_type, 'full', record_id, record_type))
        print('<big>Back to %s</big>' % ISFDBLink('%s.cgi' % note.cgi_script, record_id, note.record_title, False, 'class="inverted"'))
        
        PrintTrailer('note', 0, 0)
