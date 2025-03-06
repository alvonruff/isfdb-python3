from __future__ import print_function
#
#     (C) COPYRIGHT 2004-2025 Al von Ruff, Bill Longley, Kevin Pulliam (kevin.pulliam@gmail.com), Ahasuerus, Jesse Weinstein <jesse@wefu.org>, Uzume and Dirk Stoecker
#     ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1196 $
#     Date: $Date: 2024-11-23 16:35:37 -0500 (Sat, 23 Nov 2024) $


import cgi
import string
import sys
from isfdb import *
from login import *
from library import *
from navbar import *
from SQLparsing import *

editDEBUG = 1

def displayError(message, title = '', cgi_script = '', record_id = 0):
        if title:
                PrintPreSearch(title)
        if cgi_script != '':
                if cgi_script == 0:
                        PrintNavBar(0, 0)
                else:
                        PrintNavBar("edit/%s.cgi" % cgi_script, record_id)
        print('<div id="WarningBox">')
        print("<h3>Error: %s.</h3>" % message)
        print('</div>')
        PrintPostSearch(0, 0, 0, 0, 0)
        sys.exit(0)

def XMLunescape2(input):
        retval = str.replace(str(input), "&rsquo;", "'")
        retval = str.replace(retval, "&quot;", '"')
        retval = str.strip(retval)
        retval = str.rstrip(retval)
        return retval

def escape_string(input):
        retval = str.replace(str(input), "'", "&rsquo;")
        retval = str.replace(retval, '"', "&quot;")
        retval = str.replace(retval, '  ', ' ')
        retval = str.replace(retval, "<", "&lt;")
        retval = str.replace(retval, ">", "&gt;")
        retval = str.replace(retval, "\\r\\n", "")
        return retval

def escape_quotes(input):
        if input:
                return str.strip(repr(input+'"')[1:-2])
        else:
                return ''

def escape_spaces(input):
        return str.replace(input, ' ', '%20')

def unescape_spaces(input):
        return str.replace(input, '%20', ' ')


##################################################################
# Create an SQL search query substring
##################################################################

Query_DT_List = ['author_birthdate', 'author_deathdate']
Query_EQ_List = ['pub_tag', 'pub_ptype', 'pub', 'pubs', 'ttype']
Query_LL_List = ['pub_price', 'pub_pages']
Query_RL_List = ['pub_title', 'pub_author', 'pub_year', 'pub_publisher', 'pub_isbn', 
                'pub_coverart', 'pub_bcoverart', 'author_legalname', 
                'author_birthplace', 'author_pseudos', 'title_series', 'title_superseries',
                'author_canonical', 'title_title']

def makequery(entry, use):
        if use in Query_DT_List:
                return "%s >= '%s-00-00' and %s < '%s-00-00'" % (use, entry[0:4], use, int(entry[0:4])+1)
        elif use in Query_EQ_List:
                return use+" = '"+entry+"'"
        elif use in Query_LL_List:
                return use+" like '%"+entry+"'"
        elif use in Query_RL_List:
                return use+" like '%"+entry+"%'"
        else:
                print("BAD QUERY USE:", use)
                return ''


##################################################################
# These routines start and end the HTML page
##################################################################
def PrintPreSearch(title):
        PrintHTMLHeaders(title)

        print('<script type="text/javascript" src="%s://%s/isfdb_main.js"></script>' % (PROTOCOL, HTMLLOC))
        # Include the JavaScript file with the general purpose JS functions that support editing
        print('<script type="text/javascript" src="%s://%s/edit_js.js"></script>' % (PROTOCOL, HTMLLOC))

        if title in ('Publication Editor', 'Add Publication', 'New Novel', 'New Magazine',
                     'New Anthology', 'New Collection', 'New Omnibus', 'New Nonfiction',
                     'New Fanzine', 'New Chapbook', 'Clone Publication', 'Import/Export Contents',
                     'Delete Publication'):
                JSscript('edit_pub')
                JSscript('edit_title')
        elif title in ('Title Editor', 'Make Variant Title', 'Add Variant Title'):
                JSscript('edit_title')
        elif title == 'Author Editor':
                JSscript('edit_author')
        elif title == 'Award Editor':
                JSscript('edit_award')
                JSscript('edit_author')
                JSscript('edit_title')
        elif ('New Award Category for' in title) or title in ('Award Type Editor',
                                                            'Award Editor for a Title',
                                                            'Add New Award Type',
                                                            'Award Category Editor'):
                JSscript('edit_award')
        elif title in ('Publisher Editor', 'Publication Series Editor', 'Series Editor'):
                JSscript('edit_other')

        print('</div>')
        # The "<noscript>" part will only be executed if Javascript is not enabled on the browser side
        print('<noscript><h1>Your browser does not support JavaScript. Javascript is required to edit ISFDB.')
        print('%s to return to browsing ISFDB.</h1></noscript>' % ISFDBLink('index.cgi', '', 'Click here'))

def JSscript(script_name):
        print('<script type="text/javascript" src="%s://%s/%s.js"></script>' % (PROTOCOL, HTMLLOC, script_name))

def getSubmitter():
        (userid, username, usertoken) = GetUserData()
        return username

##################################################
#
#        3 versions of function PrintUserInfo appear in 3 different locations
#        See /mod/isfdblib.py for Moderator PrintUserInfo function
#        see /biblio/common.py for Regular PrintUserInfo function
#
##################################################
def PrintUserInfo(userid, username):
        if username:
                PrintLoggedIn(userid, username)
        else:
                PrintNotLoggedIn(0,0)
        return

#######################################################
#
#        Function appears in three different locations
#        Edit NavBar function.
#        See /mod/isfdblib.py for Moderator NavBar function
#        see /biblio/common.py for Regular NavBar function
#
#######################################################
def PrintNavBar(executable, arg):
        (userid, username, usertoken) = GetUserData()

        print('<div id="nav">')
        #Print the search box from module navbar
        PrintSearchBox('')
        PrintUserInfo(userid, username)
        PrintOtherPages('Moderator')
        print('</div>')
        
        print('<div id="main2">')
        dbStatus = SQLgetDatabaseStatus()
        if dbStatus == 0:
                print("<h3>The ISFDB database is currently offline. Please check back in a few minutes.</h3>")
                PrintPostSearch(0, 0, 0, 0, 0)
                sys.exit(0)
        
        onlineVersion = SQLgetSchemaVersion()
        if onlineVersion != SCHEMA_VER:
                print("<h3>Warning: database schema mismatch (%s vs %s)</h3>" % (onlineVersion, SCHEMA_VER))
        if (username == 0) and (editDEBUG == 0):
                print('<h2>Login required to edit</h2>')
                print("""Note that you have to %s and the ISFDB wiki separately.
                        Your database user name is the same as your Wiki user name.
                        Your database password is the same as your Wiki
                        password.""" % ISFDBLink('dologin.cgi', '%s+%s' % (executable, arg), 'login to the ISFDB database'))
                PrintPostSearch(0, 0, 0, 0, 0, 0)
                sys.exit(0)
        moderator_flag = SQLisUserModerator(userid)
        editStatus = SQLgetEditingStatus()
        if editStatus == 0:
                print('<h2>Editing facilities are currently offline</h2>')
                PrintPostSearch(0, 0, 0, 0, 0, 0)
                sys.exit(0)
        elif editStatus == 2:
                if moderator_flag == 0:
                        print('<h2>Editing facilities have been temporarily restricted to moderators only.</h2>')
                        PrintPostSearch(0, 0, 0, 0, 0, 0)
                        sys.exit(0)
        if SQLisUserBlocked(userid):
                print('<h2>This ISFDB account is currently blocked and unable to edit data.</h2>')
                PrintPostSearch(0, 0, 0, 0, 0, 0)
                sys.exit(0)
        if ((moderator_flag ==0)
            and (SESSION.cgi_script not in ('vote', 'verify', 'submit_primary_verification',
                                        'submitver', 'edittags', 'cleanup', 'cleanup_report',
                                        'find_dups', 'find_pub_dups', 'keygen'))
            and (SQLWikiEditCount(username) < SESSION.new_editor_threshold)
            and (SQLCountPendingSubsForUser(userid) > SESSION.max_new_editor_submissions)):
                print("""<h2>You currently have %d pending submissions, more than the limit for new editors.
                             You will need to wait for the moderators to process your submissions
                             before you can create new ones. Posting Wiki responses to moderator questions
                             will eventually remove the "new editor" flag from your account, at which
                             point you will be able to have more pending submissions at the same time.
                             If you believe that this message is in error, please post on the
                             Community Portal.</h2>""" % SQLCountPendingSubsForUser(userid))
                PrintPostSearch(0, 0, 0, 0, 0, 0)
                sys.exit(0)

def PrintPostSearch(executable=0, records=0, subsequent=0, printed=0, mergeform=0, tableclose=True):
        if tableclose:
                print('</table>')
        if mergeform:
                print('<hr>')
                print('<p>')
                print('<input TYPE="SUBMIT" VALUE="Merge Selected Records">')
                print('</form>')
        if printed == 100:
                print('<hr>')
                print(ISFDBLink('edit/%s.cgi' % executable, subsequent, '[Records: %s]' % records))

        if len(SESSION.SQLlog) > 0:
                print('<div class="VerificationBox">')
                print('<h2>Debug SQL Log:</h2>')
                SQLoutputLog()
                print("</div>")

        print('</div>')
        print('<div id="bottom">')
        print(COPYRIGHT)
        print('<br>')
        print(ENGINE)
        print('</div>')
        print('</div>')
        print('</body>')
        print('</html>')

def PrintTitle(title):
        print("Content-type: text/html; charset=%s\n" % (UNICODE))
        print("<html>\n")
        print("<head><title>%s</title></head>\n" % (title))
        print("<body>\n")

def PrintDuplicateTitleRecord(record, bgcolor, authors):
        if bgcolor:
                print('<tr align=left class="table1">')
        else:
                print('<tr align=left class="table2">')

        print('<td><INPUT TYPE="checkbox" NAME="merge" VALUE="' +str(record[TITLE_PUBID])+ '"></td>')
        print("<td>" +record[TITLE_YEAR][:4]+ "</td>")
        print("<td>" +record[TITLE_TTYPE]+ "</td>")
        if record[TITLE_STORYLEN]:
                print("<td>" +record[TITLE_STORYLEN]+ "</td>")
        else:
                print("<td> </td>")

        # Print variant information
        if record[TITLE_PARENT]:
                print("<td>Variant</td>")
        else:
                print("<td> </td>")

        # Print this title's language
        if record[TITLE_LANGUAGE]:
                print("<td>%s</td>" % (LANGUAGES[int(record[TITLE_LANGUAGE])]))
        else:
                print("<td> </td>")

        print("<td>%s</td>" % ISFDBLink('title.cgi', record[TITLE_PUBID], record[TITLE_TITLE]))

        print("<td>")
        for author in authors:
                print(ISFDBLink('ea.cgi', author[0], author[1]))
        print("</td>")

        print("<td>")
        if record[TITLE_NOTE]:
                note = SQLgetNotes(record[TITLE_NOTE])
                print(FormatNote(note, '', 'edit'))
        else:
                print("&nbsp;")
        print("</td>")

        print("</tr>")

def PrintDuplicateTableColumns():
        print('<table class="generic_table">')
        print('<tr class="generic_table_header">')
        print('<th>Merge</th>')
        print('<th>Year</th>')
        print('<th>Type</th>')
        print('<th>Length</th>')
        print('<th>Variant</th>')
        print('<th>Language</th>')
        print('<th>Title</th>')
        print('<th>Authors</th>')
        print('<th>Note</th>')
        print('</tr>')

def CheckOneTitleForDuplicates(title):
        possible_duplicates = ISFDBPossibleDuplicates(title)
        if not possible_duplicates:
                return 0

        print('<form METHOD="POST" ACTION="/cgi-bin/edit/tv_merge.cgi">')
        PrintDuplicateTableColumns()
        title_authors = SQLTitleBriefAuthorRecords(title[TITLE_PUBID])
        PrintDuplicateTitleRecord(title, 0, title_authors)

        for target in possible_duplicates:
                target_title = target[0]
                target_authors = target[1]
                PrintDuplicateTitleRecord(target_title, 0, target_authors)

        print('</table>')
        print('<p>')
        print('<input TYPE="SUBMIT" VALUE="Merge Selected Records">')
        print('</form>')
        print('<p>')
        return 1

class Submission:
        def __init__(self):
                self.header = ''
                self.cgi_script = 0
                self.type = 0
                self.user = User()
                self.user.load()

        def file(self, update_string):
                import viewers
                update = """insert into submissions(sub_state, sub_type, sub_data, sub_time, sub_submitter)
                            values('N', %d, '%s', NOW(), %d)""" % (self.type, update_string, int(self.user.id))
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(update)
                submission_id = CNX.DB_INSERT_ID()

                # If the user is a moderator or a self-approver and there is no override preference,
                # redirect to the review/approval page
                if not self.user.display_post_submission:
                        if SQLisUserModerator(self.user.id) or SQLisUserSelfApprover(self.user.id):
                                location = "mod/submission_review.cgi?%s" % submission_id
                                ISFDBLocalRedirect(location)
                
                PrintPreSearch(self.header)
                PrintNavBar(self.cgi_script, 0)

                PrintWikiPointer(self.user.name)
                print('<h1>Submitting the following changes:</h1>')
                function_name = SUBMAP[self.type][5]
                if SUBMAP[self.type][0] == 0:
                        getattr(viewers, function_name)(submission_id)
                else:
                        viewers.SubmissionViewer(function_name, submission_id)
                
                # If the user is a moderator or a self-approver, allow going to the approval page
                if SQLisUserModerator(self.user.id) or SQLisUserSelfApprover(self.user.id):
                        print('<br>Moderate %s' % ISFDBLink('mod/submission_review.cgi', submission_id, 'submission'))
                PrintPostSearch(0, 0, 0, 0, 0, 0)
        
        def error(self, error = '', record_id = 0):
                displayError(error, self.header, self.cgi_script, record_id)

        def CheckField(self, newUsed, oldUsed, newField, oldField, tag, multi):
                update = 0
                changes = 0
                update_string = ''

                ######################################################################
                # If a field is and was being used, update it only if it's different
                ######################################################################
                if newUsed and oldUsed:
                        if multi:
                                update = compare_lists(newField, oldField)
                        else:
                                if newField != XMLescape(oldField):
                                        update = 1

                ######################################################################
                # If a field is being used, but wasn't before, update it
                ######################################################################
                elif newUsed and (oldUsed == 0):
                        update = 1

                ######################################################################
                # If a field is not being used, but it was before, update it
                ######################################################################
                elif (newUsed == 0) and oldUsed:
                        newField = ""
                        update = 1

                if update:
                        CNX = MYSQL_CONNECTOR()
                        if multi:
                                update_string = "    <%ss>\n" % (tag)
                                for field in newField:
                                        update_string += "      <%s>%s</%s>\n" % (tag, CNX.DB_ESCAPE_STRING(field), tag)
                                update_string += "    </%ss>\n" % (tag)
                        else:
                                update_string = "    <%s>%s</%s>\n" % (tag, CNX.DB_ESCAPE_STRING(newField), tag)

                        changes = 1
                return (changes, update_string)

def compare_lists(newField, oldField):
        # Compare two lists of values. Return 1 if there are different elements, 0 otherwise.
        # The elements in the first list are XML-escaped while the elements in the second
        # list are not XML-escaped.
        
        if len(newField) != len(oldField):
                return 1
        
        for subvalue in oldField:
                if XMLescape(subvalue) not in newField:
                        return 1

        for subvalue in newField:
                if XMLunescape(subvalue) not in oldField:
                        return 1
        return 0

def debugSubmission():
        PrintPreSearch("Submission Debug")
        PrintNavBar(0, 0)
