#!_PYTHONLOC
#
#     (C) COPYRIGHT 2004-2021   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended serieslication of such source code.
#
#     Version: $Revision: 713 $
#     Date: $Date: 2021-08-27 10:38:44 -0400 (Fri, 27 Aug 2021) $

	
import cgi
import sys
import MySQLdb
from isfdb import *
from isfdblib import *
from seriesClass import *
from SQLparsing import *
from login import *
from library import ISFDBLocalRedirect

def DoError(message):
	PrintPreSearch("Vote Submission")
	PrintNavBar(0, 0)
        print "<h3>ERROR: %s</h3>" % message
        PrintPostSearch(0, 0, 0, 0, 0)
        sys.exit(0)
	
if __name__ == '__main__':

	
        sys.stderr = sys.stdout
        form = cgi.FieldStorage()

        try:
                title_id = int(form['title_id'].value)
		title_title = SQLgetTitle(title_id)
		if not title_title:
                        raise
	except:
                DoError('Title ID not specified or invalid')

        try:
                vote = int(form['vote'].value)
                if vote < 0 or vote > 10:
                        raise
	except:
                DoError('Vote not submitted or invalid')

	(userid, username, usertoken) = GetUserData()
	userid = int(userid)
	if not userid:
                DoError('You must be logged in in order to vote')

        # If the submitted vote was 0, then delete this user's vote
        if vote == 0:
                delete = "delete from votes where title_id=%d and user_id=%d" % (title_id, userid)
                db.query(delete)
        else:
                # Check to see if this user has already voted for this title
                query = "select * from votes where title_id=%d and user_id=%d" % (title_id, userid)
                db.query(query)
                result = db.store_result()
                if result.num_rows() > 0:
                        record = result.fetch_row()
                        record_id = record[0][0]
                        update = "update votes set rating=%d where vote_id=%d" % (vote, record_id)
                        db.query(update)
                else:
                        insert = "insert into votes(title_id, user_id, rating) values(%d, %d, %d)" % (title_id, userid, vote)
                        db.query(insert)

        ISFDBLocalRedirect('title.cgi?%d' % int(title_id))
