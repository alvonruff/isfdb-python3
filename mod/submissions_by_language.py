#!_PYTHONLOC
#
#     (C) COPYRIGHT 2023   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 751 $
#     Date: $Date: 2021-09-17 17:33:29 -0400 (Fri, 17 Sep 2021) $


from SQLparsing import *
from isfdblib import *
from common import Queue
import cgi


if __name__ == '__main__':

        form = cgi.FieldStorage()
        try:
                language_name = form['language'].value
        except:
                SESSION.DisplayError('Language name not specified')

        language_id = SQLGetLangIdByName(language_name)
        if not language_id:
                SESSION.DisplayError('Specified language is not supported by ISFDB')

        try:
                start = int(form['start'].value)
        except:
                start = 0

        PrintPreMod('Pending NewPub Submission - %s' % language_name)
        PrintNavBar()

        print ('<h3>Pending NewPub submissions - %s</h3>' % language_name)
        queue = Queue()
        queue.display_pending_for_language(language_name)

	PrintPostMod(0)

