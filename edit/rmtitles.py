#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff, Bill Longley and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 936 $
#     Date: $Date: 2022-06-16 17:55:50 -0400 (Thu, 16 Jun 2022) $


import cgi
import sys
from SQLparsing import *
from isfdb import *
from isfdblib import *
from isfdblib_help import *
from isfdblib_print import printtextarea
from library import *


###################################################################
# This function outputs a title record in table format
###################################################################
def printtitlerecord(content_item, index):

        print('<li>')
        title = content_item[0]
        contents = content_item[1]

        if title[TITLE_TTYPE] == 'COVERART':
                print('<input type="checkbox" value="%d" name="cover%d"> ' % (contents[PUB_CONTENTS_ID], index))
                authors = SQLTitleBriefAuthorRecords(title[TITLE_PUBID])
        elif title[TITLE_TTYPE] == 'REVIEW':
                print('<input type="checkbox" value="%d" name="review%d"> ' % (contents[PUB_CONTENTS_ID], index))
                authors = SQLReviewBriefAuthorRecords(title[TITLE_PUBID])
        elif title[TITLE_TTYPE] == 'INTERVIEW':
                print('<input type="checkbox" value="%d" name="interview%d"> ' % (contents[PUB_CONTENTS_ID], index))
                authors = SQLInterviewBriefAuthorRecords(title[TITLE_PUBID])
        else:
                print('<input type="checkbox" value="%d" name="title%d"> ' % (contents[PUB_CONTENTS_ID], index))
                authors = SQLTitleBriefAuthorRecords(title[TITLE_PUBID])

        page = contents[PUB_CONTENTS_PAGE]
        if page:
                print('%s - ' % (str(page)))
        
        line = '%s, %s' % (ISFDBLink('title.cgi', title[TITLE_PUBID], title[TITLE_TITLE]), title[TITLE_TTYPE])
        for author in authors:
                line += ', %s' % ISFDBLink('ea.cgi', author[0], author[1])
        print(line)

def CheckContainer(title, pubtype):
        if (title[TITLE_TTYPE] == 'EDITOR'):
                return 1
        elif (title[TITLE_TTYPE] == 'OMNIBUS') and (pubtype == 'OMNIBUS'):
                return 1
        elif (title[TITLE_TTYPE] == 'COLLECTION') and (pubtype == 'COLLECTION'):
                return 1
        elif (title[TITLE_TTYPE] == 'ANTHOLOGY') and (pubtype == 'ANTHOLOGY'):
                return 1
        elif (title[TITLE_TTYPE] == 'CHAPBOOK') and (pubtype == 'CHAPBOOK'):
                return 1
        elif (title[TITLE_TTYPE] == 'NONFICTION') and (pubtype == 'NONFICTION'):
                return 1
        else:
                return 0

if __name__ == '__main__':

        pub_id = SESSION.Parameter(0, 'int')
        publication = SQLGetPubById(pub_id)
        if not publication:
                SESSION.DisplayError('Record Does Not Exist')
        
        ##################################################################
        # Output the leading HTML stuff
        ##################################################################
        PrintPreSearch('Removal Editor')
        PrintNavBar('edit/rmtitles.cgi', pub_id)

        print('<div id="HelpBox">')
        print('<b>Help on removing titles: </b>')
        print('<a href="%s://%s/index.php/Help:Screen:RemoveTitles">Help:Screen:RemoveTitles</a><p>' % (PROTOCOL, WIKILOC))
        print('</div>')

        help = HelpGeneral()
        
        print('<form id="data" METHOD="POST" ACTION="/cgi-bin/edit/submitrm.cgi">')
        print('<p>')
        print('<div class="bold">Select items to remove from %s:</div>' % ISFDBLink('pl.cgi', pub_id, publication[PUB_TITLE]))
        print('<hr>')

        pubtype = publication[PUB_CTYPE]
        # Get the "reference" Title record for this publication, including EDITORs for MAGAZINEs/FANZINEs
        reference_id = SQLgetTitleReferral(pub_id, pubtype, 1)
        if int(reference_id) == 0:
                print('<div id="WarningBox">')
                print("""<h3>WARNING: Unable to locate the title reference for this publication.</h3>
                        Removing titles while in this state is dangerous. Check to make sure the publication
                        type is correct (collection, novel, anthology, etc.). Then come back and remove
                        the title in question.""")
                print('</div>')

        # Get the list of titles in this pub and sort them by page number
        pages = getPubContentList(pub_id)

        missing_contents = []
        container_contents = []
        cover_contents = []
        normal_contents = []
        review_contents = []
        interview_contents = []
        for content_item in pages:
                title_id = content_item[PUB_CONTENTS_TITLE]
                title = SQLloadTitle(title_id)
                if (len(title) == 0):
                        missing_contents.append(title_id)
                #If this title is the "reference" title for the pub, show it as a Container title
                elif int(title[TITLE_PUBID]) == int(reference_id):
                        container_contents.append((title, content_item))
                elif (title[TITLE_TTYPE] == 'COVERART'):
                        cover_contents.append((title, content_item))
                #Check whether this title is of the same "container" type as the publication record
                elif CheckContainer(title, pubtype) == 1:
                        container_contents.append((title, content_item))
                elif (title[TITLE_TTYPE] == 'REVIEW'):
                        review_contents.append((title, content_item))
                elif (title[TITLE_TTYPE] == 'INTERVIEW'):
                        interview_contents.append((title, content_item))
                else:
                        normal_contents.append((title, content_item))

        index = 1
        if missing_contents:
                print('<div id="ErrorBox">')
                print('<p><b>MISSING TITLES (please report to moderators):</b>')
                print('<ul>')
                for missing_item in missing_contents:
                        print('<li>%d</li>' % missing_item)
                print('</ul>')
                print('</div>')
                sys.exit(1)

        index = 1
        if cover_contents:
                print('<p><b>COVER ART:</b>')
                print('<ul>')
                for content_item in cover_contents:
                        printtitlerecord(content_item, index)
                        index += 1
                print('</ul>')

        index = 1
        if container_contents:
                print('<p><b>CONTAINER TITLES (exercise caution):</b>')
                print('<ul>')
                for content_item in container_contents:
                        printtitlerecord(content_item, index)
                        index += 1
                print('</ul>')

        if normal_contents:
                print('<p><b>REGULAR TITLES:</b>')
                print('<ul>')
                for content_item in normal_contents:
                        printtitlerecord(content_item, index)
                        index += 1
                print('</ul>')

        index = 1
        if review_contents:
                print('<p><b>REVIEWS:</b>')
                print('<ul>')
                for content_item in review_contents:
                        printtitlerecord(content_item, index)
                        index += 1
                print('</ul>')

        index = 1
        if interview_contents:
                print('<p><b>INTERVIEWS:</b>')
                print('<ul>')
                for content_item in interview_contents:
                        printtitlerecord(content_item, index)
                        index += 1
                print('</ul>')

        print('<p>')
        print('<hr>')
        print('<table border="0">')
        print('<tbody id="tagBody">')
        printtextarea('Note to Moderator', 'mod_note', help, '')
        print('</tbody>')
        print('</table>')
        print('<p>')
        print('<input name="pub_id" value="%d" type="HIDDEN">' % pub_id)
        print('<input type="SUBMIT" value="Submit Data">')
        print('</form>')
        print('<p>')

        PrintPostSearch(0, 0, 0, 0, 0, False)
