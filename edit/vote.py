#!_PYTHONLOC
#
#     (C) COPYRIGHT 2006-2025   Al von Ruff and Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 650 $
#     Date: $Date: 2021-06-19 13:31:03 -0400 (Sat, 19 Jun 2021) $


from isfdb import *
from isfdblib import *
from library import *
from SQLparsing import *
from login import *

if __name__ == '__main__':
        title_id = SESSION.Parameter(0, 'int')
        title_title = SQLgetTitle(title_id)
        if not title_title:
                SESSION.DisplayError('Record Does Not Exist')

        PrintPreSearch("Title Vote")
        PrintNavBar(0, 0)

        query = "select COUNT(vote_id) from votes where title_id='%d'" % (title_id)
        db.query(query)
        result = db.store_result()
        record = result.fetch_row()
        total_votes = int(record[0][0])

        if total_votes:
                counter = 1
                ratings = []
                ratings.append(0)
                while counter < 11:
                        query = "select COUNT(rating) from votes where title_id='%d' and rating='%d'" % (title_id, counter)
                        db.query(query)
                        result = db.store_result()
                        if result.num_rows() > 0:
                                record = result.fetch_row()
                                if record[0][0]:
                                        ratings.append(int(record[0][0]))
                                else:
                                        ratings.append(0)
                        else:
                                ratings.append(0)
                        counter += 1
        else:
                ratings = [0,0,0,0,0,0,0,0,0,0,0]

        counter = 1
        total_ratings = 0
        total_votes = 0
        max_ratings = 0
        while counter < 11:
                if ratings[counter]:
                        total_ratings += ratings[counter] * counter
                        total_votes += ratings[counter]
                if ratings[counter] > max_ratings:
                        max_ratings = ratings[counter]
                counter += 1

        title = SQLloadTitle(title_id)
        print 'User Ratings for <b>%s</b>' % ISFDBLink("title.cgi", title_id, title[TITLE_TITLE])
        print '<p>'

        if total_votes == 1:
                print "1 user has given an average vote of %2.2f / 10" % (float(total_ratings)/float(total_votes))
        elif total_votes > 1:
                print "%d users have given an average vote of %2.2f / 10" % (total_votes,  float(total_ratings)/float(total_votes))
        else:
                print "No votes have been recorded for this title"

        print '<table class="generic_table">'
        print '<tr>'
        print '<th>Rating</th>'
        print '<th>Votes</th>'
        print '<th>Percentage</th>'
        print '</tr>'
        counter = 1
        while counter < 11:
                if total_votes:
                        percent = 100.0 * (float(ratings[counter]) /  float(total_votes))
                else:
                        percent = 0.0
                print '<tr>'
                print '<td>%d</td>' % counter
                print '<td>%d</td>' % ratings[counter]
                print '<td>%2.2f</td>' % percent
                print '</tr>'
                counter += 1
        print '</table>'

        (userid, username, usertoken) = GetUserData()
        userid = int(userid)
        query = "select rating from votes where title_id=%d and user_id=%d" % (title_id, userid)
        db.query(query)
        result = db.store_result()
        if result.num_rows() > 0:
                record = result.fetch_row()
                user_vote = record[0][0]
        else:
                user_vote = 0

        print '<p>Select a number 0-10 to indicate your rating of this work:'
        print '<ul>'
        print "<li>0 - <b>Remove your previous vote</b>."
        print "<li>1 - Extremely poor. One of the worst titles ever written. Couldn't be any worse."
        print '<li>2 - Very bad, with minor redeeming characteristics.'
        print '<li>3 - Bad.'
        ###########################
        print '<li>4 - Below average.'
        print '<li>5 - Slightly below average.'
        print '<li>6 - Slightly above average.'
        print '<li>7 - Above average.'
        ###########################
        print '<li>8 - Good; recommended.'
        print '<li>9 - Very good, but not quite perfect.'
        print "<li>10 - Excellent. One of the best titles ever written. Couldn't be any better."
        print '</ul>'

        if user_vote:
                print '<br><p>Your current vote: <b>%d</b>' % user_vote
        else:
                print '<br><p>Your vote:'
        print '<form method="POST" action="/cgi-bin/edit/submitvote.cgi">'
        print '<p>'
        print '<select name="vote">'
        counter = 0
        while counter < 11:
                if counter == user_vote:
                        print '<option selected="selected">%d</option>' % counter
                else:
                        print '<option>%d</option>' % counter
                counter += 1
        print '</select>'
        print '<input name="title_id" value="%d" type="HIDDEN">' % (title_id)
        print '<input type="SUBMIT" value="Submit Vote">'
        print '</form>'

        PrintPostSearch(0, 0, 0, 0, 0, 0)
