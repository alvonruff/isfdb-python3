#
#     (C) COPYRIGHT 2009-2022   Al von Ruff, Ahasuerus, Bill Longley and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1039 $
#     Date: $Date: 2022-10-18 16:34:51 -0400 (Tue, 18 Oct 2022) $

from isfdb import *
from SQLparsing import *
from library import ISFDBLink

################################################################
# The functions found here are used across all ISFDB directories
# to display navigation-related messages and menu sections
################################################################

def PrintMessagesLink(userid, username):
	if SQLhasNewTalk(userid):
		# diff=cur causes the page to display in "diff" mode, with the
		# most recent change highlighted in a diff region at the top.
		print '<li><div class="newtalk"><a href="%s://%s/index.php/User_talk:%s">My Messages</a> (new)</div>' % (PROTOCOL, WIKILOC, username)
	else:
		print '<li><a href="%s://%s/index.php/User_talk:%s">My Messages</a>' % (PROTOCOL, WIKILOC, username)

def PrintWikiPointer(submitter):
	#If the count of Wiki edits is greater than X, then do not display the Wiki pointer
        if SQLWikiEditCount(submitter) > 100:
                return
	wikipointer = """<h1>Your submission must be approved by a moderator before it enters the database.</h1>
                        If the moderator has questions or comments about your submission,
                        they will be posted on your Wiki Talk page: """
	wikipointer += '<a href="%s://%s/index.php/User_talk:%s">' % (PROTOCOL, WIKILOC, submitter)
	wikipointer += '%s://%s/index.php/User_talk:%s</a>.' % (PROTOCOL, WIKILOC, submitter)
	wikipointer += " Please check this page frequently for comments or questions."
	print wikipointer
        return


# Display the Search box in the navigation bar
def PrintSearchBox(page, search_value = '', search_type = ''):
        from library import ISFDBLink, ISFDBText
        print '<div id="search">'
       	print '<a href="%s:/%s/index.cgi">' % (PROTOCOL, HTFAKE)
	if page == 'frontpage':
		print '<img src="%s://%s/isfdb_logo.jpg" width="129" height="85" alt="ISFDB logo">' % (PROTOCOL, HTMLHOST)
	else:
		print '<img src="%s://%s/isfdb.gif" width="130" height="77" alt="ISFDB logo">' % (PROTOCOL, HTMLLOC)
        print '</a>'
	print 'Search the database'
        print '<form method="get" action="%s:/%s/se.cgi" name="searchform" id="searchform">' % (PROTOCOL, HTFAKE)
	print '<p>'
	print '<input name="arg" id="searchform_arg" class="search" value="%s">' % ISFDBText(search_value)
	print '<select name="type" class="search">'
	options = ('Name', 'Fiction Titles', 'All Titles', 'Year of Title',
                   'Month of Title', 'Month of Publication', 'Series',
                   'Publication Series', 'Magazine', 'Publisher', 'ISBN',
                   'Tag', 'Award')
	for option in options:
                if option == search_type:
                        selected = ' selected="selected"'
                else:
                        selected = ''
                print '<option%s>%s</option>' % (selected, option)
        print '</select>'
        print '<input value="Go" type="submit" >'
        print '</form>'
        print '<p class="bottomlinks">'
        print ISFDBLink("adv_search_menu.cgi","","Advanced Search", argument='class="inverted"')
        print '</div>'
        return

#Display the Other Pages section in the navigation bar
def PrintOtherPages(choice):
	print '<div class="divider">'
	print 'Other Pages:'
	print '</div>'
	print '<ul class="navbar">'
	if choice != 'frontpage':
        	print '<li>%s' % ISFDBLink('index.cgi', '', 'Home Page')
	if choice == 'Moderator':
        	print '<li>%s' % ISFDBLink('mod/list.cgi', 'N', 'Moderator')
	print '<li><a href="%s://%s/index.php/Main_Page">ISFDB Wiki</a>' % (PROTOCOL, WIKILOC)
	print '<li><a href="%s://%s/index.php/ISFDB:FAQ">ISFDB FAQ</a>' % (PROTOCOL, WIKILOC)
        print '<li>%s' % ISFDBLink('calendar_menu.cgi', '', 'SF Calendar')
        print '<li>%s' % ISFDBLink('directory.cgi', 'author', 'Author Directory')
	print '<li>%s' % ISFDBLink('award_directory.cgi', '', 'Award Directory')
        print '<li>%s' % ISFDBLink('directory.cgi', 'publisher', 'Publisher Directory')
	print '<li>%s' % ISFDBLink('directory.cgi', 'magazine', 'Magazine Directory')
        print '<li>%s' % ISFDBLink('stats-and-tops.cgi', '', 'Statistics/Top Lists')
        print '<li>%s' % ISFDBLink('recent_activity_menu.cgi', '', 'Recent Activity')
        print '<li>%s' % ISFDBLink('edit/cleanup.cgi', '', 'Cleanup Reports')
	print '</ul>'
        return

def PrintLoggedIn(userid,username):
	print '<div class="divider">'
	print 'Logged In As'
	print '</div>'
	print '<ul class="navbar">'
	print '<li>', username
	print '<li>%s' % ISFDBLink('dologout.cgi', '', 'Log Out')
	print '<li><a href="%s://%s/index.php/Help:Navigation_Bar">Help Navigating</a>' % (PROTOCOL, WIKILOC)
	PrintMessagesLink( userid, username )
        print '<li>%s' % ISFDBLink('mypreferences.cgi', '', 'My Preferences')
        print '<li>%s' % ISFDBLink('myrecent.cgi', '0+I', 'My Recent Edits')
        print '<li>%s' % ISFDBLink('myrecent.cgi', '0+N', 'My Pending Edits')
        print '<li>%s' % ISFDBLink('myrecent.cgi', '0+R', 'My Rejected Edits')
        print '<li>%s' % ISFDBLink('myrecent.cgi', '0+P', 'My Errored Out Edits')
        print '<li>%s' % ISFDBLink('myvotes.cgi', '0+Vote', 'My Votes')
        print '<li>%s' % ISFDBLink('usertag.cgi', userid, 'My Tags')
        print '<li>%s' % ISFDBLink('my_verifications_menu.cgi', '', 'My Verifications')
        # Display a "New" message if this user has new changes to primary-verified publications
        if SQLChangedVerifications(userid):
                print ' <span class="inverted">New!</span>'
	print '</ul>'
        return

def PrintNotLoggedIn(executable,argument):
	print '<div class="divider">'
	print 'Not Logged In'
	print '</div>'
	print '<ul class="navbar">'
	print '<li>%s' % ISFDBLink('dologin.cgi', '%s+%s' % (str(executable), str(argument)), 'Log In')
	print '<li><a href="%s://%s/index.php/Help:Navigation_Bar">Help Navigating</a>' % (PROTOCOL, WIKILOC)
	print '</ul>'
        return
