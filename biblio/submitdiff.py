#!_PYTHONLOC
#
#     (C) COPYRIGHT 2005-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 991 $
#     Date: $Date: 2022-09-07 18:27:14 -0400 (Wed, 07 Sep 2022) $

        
import cgi
import sys
from login import *
from SQLparsing import *
from common import *


def DoError(message):
        print '<h3>%s</h3>' % message
        PrintTrailer('pubdiff', 0, 0)
        sys.exit(0)
        
if __name__ == '__main__':

        PrintHeader("Publication Comparison")
        PrintNavbar('pubdiff', 0, 0, 0, 0)

        form = cgi.FieldStorage()

        pub_ids = {}
        try:
                for key in form.keys():
                        # Retrieve and save all pub IDs
                        if key.startswith('pub'):
                                key_value = int(key.split('pub')[1])
                                pub_id = int(form[key].value)
                                pub_ids[key_value] = pub_id
        except:
                DoError('Invalid Publication ID specified')

        # If the user selected fewer than 2 pubs, display an error message and abort
        if len(pub_ids.keys()) < 2:
                DoError('You must select at least 2 publications to compare')

        pubs = []
        for key_value in sorted(pub_ids.keys()):
                pub = SQLGetPubById(pub_ids[key_value])
                pubs.append(pub)

        titles_dict = {}
        title_bodies = {}
        pages = {}
        for pub in pubs:
                pub_id = int(pub[PUB_PUBID])
                title_bodies[pub_id] = SQLloadTitlesXBT(pub_id)
                # Build a dictionary with a list of pub IDs for each title ID
                for title in title_bodies[pub_id]:
                        title_id = int(title[TITLE_PUBID])
                        title_bodies[title_id] = title
                        if title_id not in titles_dict:
                                titles_dict[title_id] = []
                        titles_dict[title_id].append(pub_id)
                # Get page numbers and put them in a 2-level dictionary
                pub_content = SQLGetPubContentList(pub_id)
                if pub_id not in pages:
                        pages[pub_id] = {}
                for pc in pub_content:
                        title_id = pc[PUB_CONTENTS_TITLE]
                        page_number = pc[PUB_CONTENTS_PAGE]
                        pages[pub_id][title_id] = page_number

        print '<table class="pub_comparison_table">'
        # Publication title
        print '<tr>'
        print '<th>Pub. Title:</th>'
        for pub in pubs:
                pub_id = int(pub[PUB_PUBID])
                pub_title = pub[PUB_TITLE]
                pub_date = pub[PUB_YEAR]
                print '<th>%s</th>' % ISFDBLink('pl.cgi', pub_id, pub_title)
        print '</tr>'

        # Publication Date
        print '<tr>'
        print '<th>Pub. Date:</th>'
        for pub in pubs:
                pub_date = pub[PUB_YEAR]
                print '<td>%s</td>' % pub_date
        print '</tr>'

        # Publisher
        print '<tr>'
        print '<th>Publisher:</th>'
        for pub in pubs:
                print '<td>'
                publisher_id = pub[PUB_PUBLISHER]
                if publisher_id:
                        publisher_data = SQLGetPublisher(publisher_id)
                        publisher_name = publisher_data[PUBLISHER_NAME]
                        print ISFDBLink('publisher.cgi', publisher_id, publisher_name)
                else:
                        print '&nbsp;'
                print '</td>'
        print '</tr>'

        # Publication Note
        print '<tr>'
        print '<th>Pub. Note:</th>'
        for pub in pubs:
                note_id = pub[PUB_NOTE]
                note_data = SQLgetNotes(note_id)
                print '<td>'
                print note_data
                print '</td>'
        print '</tr>'

        # Cover images
        print '<tr>'
        print '<th>Pub. Cover:</th>'
        for pub in pubs:
                pub_image = ISFDBHostCorrection(pub[PUB_IMAGE])
                print '<td>'
                if not pub_image:
                        print '&nbsp;'
                else:
                        print '<img src="%s" height="250" alt="cover image"><br>' % (pub_image.split("|")[0])
                print '</td>'
        print '</tr>'

        # Contents titles
        for title_id in titles_dict:
                title = title_bodies[title_id]
                title_title = title[TITLE_TITLE]
                title_type = title[TITLE_TTYPE]
                print '<tr>'
                print '<td>&nbsp;</td>'
                for pub in pubs:
                        pub_id = int(pub[PUB_PUBID])
                        if pub_id not in titles_dict[title_id]:
                                print '<td class="pub_comparison_title_not_found">-</td>'
                                continue
                        print '<td>'
                        if pages[pub_id][title_id]:
                                print '<b>%s</b> ' % pages[pub_id][title_id]
                        print '%s %s by ' % (ISFDBLink('title.cgi', title_id, title_title), title_type)

                        authors = SQLTitleBriefAuthorRecords(title_id)
                        counter = 0
                        for author in authors:
                                if counter:
                                        print " <b>and</b> "
                                displayAuthorById(author[0], author[1])
                                counter += 1
                        print '</td>'
                print '</tr>'

        print '<tr>'
        print '<td>&nbsp;</td>'
        for pub in pubs:
                pub_id = int(pub[PUB_PUBID])
                pub_title = pub[PUB_TITLE]
                print '<td>'
                print ISFDBLink('edit/editpub.cgi', pub_id, 'Edit %s' % pub_title, True)
                print '</td>'
        print '</tr>'
        print '</table>'

        PrintTrailer('login', 0, 0)
        sys.exit(0)
