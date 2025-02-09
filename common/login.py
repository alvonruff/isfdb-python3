#
#     (C) COPYRIGHT 2005-2022   Al von Ruff, Ahasuerus and Uzume
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 995 $
#     Date: $Date: 2022-09-09 14:03:58 -0400 (Fri, 09 Sep 2022) $


import os
import string
import time
import md5
from localdefs import *
from isfdb import *
from Cookie import SimpleCookie
from SQLparsing import *
from library import ISFDBLink, ISFDBLinkNoName

####################################################################
# setCookies() sets the user_id, user_name, and user_token
####################################################################
def setCookies(user_id, user_name, user_token):
	os.environ['HTTP_COOKIE'] = 'isfdbUserID=%s; isfdbUserName=%s; isfdbToken=%s;' % (user_id, user_name, user_token)
        for domain in (HTMLHOST, HTMLHOST_ALT):
                setDomainCookies(domain, user_id, user_name, user_token)

def setDomainCookies(domain, user_id, user_name, user_token):
        if not domain:
                return
	print 'Set-Cookie: isfdbUserID=%s; path=/; domain=%s; expires="Fri, 08-Sep-2037 15:00:00"' % (user_id, domain)
	print 'Set-Cookie: isfdbUserName=%s; path=/; domain=%s; expires="Fri, 08-Sep-2037 15:00:00"' % (user_name, domain)
	print 'Set-Cookie: isfdbToken=%s; path=/; domain=%s; expires="Fri, 08-Sep-2037 15:00:00"' % (user_token, domain)

####################################################################
# clearCookies() clears user_id, user_name, and user_token
####################################################################
def clearCookies():
	os.environ['HTTP_COOKIE'] = ''
        for domain in (HTMLHOST, HTMLHOST_ALT):
                clearDomainCookies(domain)

def clearDomainCookies(domain):
        if not domain:
                return
	print 'Set-Cookie: isfdbUserID=x; path=/; domain=%s; expires="Fri, 08-Sep-1995 15:00:00"' % domain
	print 'Set-Cookie: isfdbUserName=x; path=/; domain=%s; expires="Fri, 08-Sep-1995 15:00:00"' % domain
	print 'Set-Cookie: isfdbToken=x; path=/; domain=%s; expires="Fri, 08-Sep-1995 15:00:00"' % domain


####################################################################
# getCookie() returns a cookie dictionary of the ISFDB cookie.
####################################################################
def getCookie():
	try:
		httpCookie = os.environ['HTTP_COOKIE']
	except:
		return 0
	cookie = SimpleCookie(httpCookie)
	return cookie


####################################################################
# Look at the cookies and create the tuple: (user_id, user_name, user_token)
####################################################################
def GetUserData():
	from SQLparsing import SQLgetUserName

	cookie = getCookie()
	if cookie == 0:
		return(0,0,0)

	try:
		id = cookie['isfdbUserID'].value
		token = cookie['isfdbToken'].value
	except:
		return(0,0,0)

	# If cookie expiration works properly, this should never happen, but we leave it
	# as a safety measure in case the cookie expiration does not parse (the values
	# change, but the cookies are still delivered).
	if id == 'x' and token == 'x':
		return(0,0,0)

	try:
		(name, persistent_token) = SQLgetUserNameAndToken(id)
		# If the token in the cookie doesn't match the token stored in the database
		# for this user ID, then something is wrong -- possible forged cookies
                if (name != '') and (token != persistent_token):
                        os.environ['HTTP_COOKIE'] = ''
        		return(0,0,0)
	except Exception, e:
		return(0,0,0)

	return(id, name, token)


####################################################################
# Emit the login page
####################################################################
def LoginPage(executable, argument):
	print '<h2>Login Page</h2>'
	print """If you do not have an ISFDB account, you can create a free one
                <a href="%s://%s/index.php?title=Special:Userlogin&amp;type=signup">here</a>.""" % (PROTOCOL, WIKILOC)
	print '<br>Note that the user name and password for editing the ISFDB are the same as those for the ISFDB wiki.'
	print '<p>'
	print '<h3>Note: The first letter of your user name should be always capitalized.</h3>'
	print '<form METHOD="POST" ACTION="/cgi-bin/submitlogin.cgi">'
	print '<table border="0">'
	print '<tbody>'
	print '<tr>'
	print '<td><b>User Name: </b></td>'
	print '<td><input type="text" name="login" size="25"></td>'
	print '</tr>'
	print '<tr>'
	print '<td><b>Password: </b></td>'
	print '<td><input type="password" name="password" size="25"></td>'
	print '</tr>'
	print '</tbody>'
	print '</table>'
	print '<div>'
	print '<input type="submit" value="submit">'
	print '<input NAME="executable" VALUE="' +executable+ '" TYPE="HIDDEN">'
	print '<input NAME="argument" VALUE="' +argument+ '" TYPE="HIDDEN">'
	print '</div>'
	print '</form>'

class User:
	def __init__(self):
		self.id = ''
		self.name = ''
		self.token = ''
		self.concise_display = ''
		# The default language is English (17) if none is specified
		self.default_language = 17
		self.display_all_languages = 'All'
		self.display_title_translations = 1
		self.covers_display = ''
		self.preferences_id = ''
		self.suppress_translation_warnings = ''
		self.suppress_bibliographic_warnings = ''
		self.cover_links_display = ''
		self.keep_spaces_in_searches = ''
		self.suppress_help_bubbles = ''
		self.languages = []
		self.suppress_awards = ''
		self.suppress_reviews = ''
		self.display_post_submission = ''
		self.moderator = 0
		self.bureaucrat = 0

	def load(self):
                (self.id, self.name, self.token) = GetUserData()
                if not self.id:
                        # If this is an unregistered user, retrieve translation
                        # preferences from cookies
                        cookie = getCookie()
                        if cookie == 0:
                                return
                        try:
                                self.display_all_languages = cookie['isfdbDisplayTranslations'].value
                        except:
                                return
                        return
                (self.concise_display, self.default_language, self.display_all_languages,
                 self.covers_display, self.suppress_translation_warnings,
                 self.suppress_bibliographic_warnings, self.cover_links_display,
                 self.keep_spaces_in_searches, self.suppress_help_bubbles,
                 self.suppress_awards, self.suppress_reviews,
                 self.display_post_submission, self.display_title_translations) = SQLLoadUserPreferences(self.id)
                self.languages = SQLLoadUserLanguages(self.id)
                self.preferences_id = SQLUserPreferencesId(int(self.id))

        def load_moderator_flag(self):
                if SQLisUserModerator(self.id):
                        self.moderator = 1

        def load_bureaucrat_flag(self):
                if SQLisUserBureaucrat(self.id):
                        self.bureaucrat = 1

        def translation_message(self, page_type, record_object):
                output = ''
                if not self.id:
                        if page_type == 'series':
                                cgi_script = 'pe'
                                record_id = record_object.series_id
                        else:
                                cgi_script = record_object.page_types[record_object.page_type]
                                record_id = record_object.au_id
                        if self.display_all_languages == 'All':
                                output += 'Showing all translations. '
                                output += ISFDBLinkNoName('%s.cgi' % cgi_script, '%d+None' % record_id,
                                                    'Never display translations',
                                                    False, 'class="button"')
                        else:
                                output += 'Not showing translations. '
                                output += ISFDBLinkNoName('%s.cgi' % cgi_script, '%d+All' % record_id,
                                                    'Always display translations',
                                                    False, 'class="button"')
                        output += ' Registered users can choose which translations are shown.'
                elif not self.suppress_translation_warnings:
                        if self.display_all_languages == 'All':
                                output += 'Showing all translations'
                        elif self.display_all_languages == 'None':
                                output += 'Not showing any translations'
                        elif self.display_all_languages == 'Selected':
                                output += 'Showing the following translations: '
                                if not self.languages:
                                        output += 'None'
                                else:
                                        display_languages = []
                                        for language_code in self.languages:
                                                display_languages.append(LANGUAGES[language_code])
                                        first = 1
                                        for language in sorted(display_languages):
                                                if not first:
                                                        output += ', '
                                                output += language
                                                first = 0
                        output += ' (can be changed in %s)' % ISFDBLink('mypreferences.cgi', '', 'My Preferences')
                if not output:
                        return output
                output = '<div class="translationmessage"><b>%s</b></div>' % output
                return output

        def translation_cookies(self, translations):
                # Ignore the URL-based translation parameter for logged in users because
                # they should be setting up Translation/User Preferences instead.
                if self.id:
                        return
                # Validate the translation parameter
                if translations not in ('All','None'):
                        return
                print 'Set-Cookie: isfdbDisplayTranslations=%s; path=/; domain=%s; expires="Fri, 08-Sep-2037 15:00:00"' % (translations, HTMLHOST)
                os.environ['HTTP_COOKIE'] = 'isfdbDisplayTranslations=%s;' % translations
                self.display_all_languages = translations

        def update_last_viewed_verified_pubs_DTS(self):
                # If the user is not logged in, there is nothing to update, so quit
                if not self.id:
                        return None
                return SQLUpdate_last_viewed_verified_pubs_DTS(int(self.id))

