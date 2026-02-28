#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2013-2026   Ahasuerus, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1246 $
#     Date: $Date: 2026-02-09 07:23:57 -0500 (Mon, 09 Feb 2026) $


from isfdb import *
from common import PrintHeader, PrintNavbar, PrintTrailer
from library import ISFDBLink

def print_line(script, query_string, display_name):
        print('<li>%s' % ISFDBLink(script, query_string, display_name))
        

PrintHeader('ISFDB Statistics and Top Lists')
PrintNavbar('stats', 0, 0, 'stats-and-tops.cgi', 0)

print('<h4>Database Tables</h4>')
print('<ul>')

print_line('languages.cgi', '', 'Supported Languages')
print_line('verification_sources.cgi', '', 'Secondary Verification Sources')
print('</ul>')
print('<hr>')

print('The following lists are regenerated weekly')
print('<h4>Database Statistics</h4>')
print('<ul>')

print_line('stats.cgi', '4', 'Summary Database Statistics')
print_line('stats.cgi', '11', 'Submissions per Year')
print('</ul>')
print('<h4>Author Statistics</h4>')
print('<ul>')
print_line('authors_by_debut_year_table.cgi', '', 'Authors By Debut Year')
print_line('stats.cgi', '13', 'Most-Viewed Authors')
print('<li>Authors by Age:')
print('<ul>')
print_line('stats.cgi', '16', 'Oldest Living Authors')
print_line('stats.cgi', '17', 'Oldest Non-Living Authors')
print_line('stats.cgi', '18', 'Youngest Living Authors')
print_line('stats.cgi', '19', 'Youngest Non-Living Authors')
print('</ul>')
print('<li>Authors/Editors Ranked by Awards and Nominations:')
print('<ul>')
print_line('popular_authors_table.cgi', '0', 'All Authors and Editors')
print_line('popular_authors_table.cgi', '1', 'Novel Authors')
print_line('popular_authors_table.cgi', '2', 'Short Fiction Authors')
print_line('popular_authors_table.cgi', '3', 'Collection Authors')
print_line('popular_authors_table.cgi', '4', 'Anthology Editors')
print_line('popular_authors_table.cgi', '5', 'Non-Fiction Authors')
print_line('popular_authors_table.cgi', '6', 'Other Types Authors and Editors')
print('</ul>')
print('</ul>')

print('<h4>Language Statistics</h4>')
print('<ul>')
print_line('stats.cgi', '20', 'Authors by Working Language')
print_line('stats.cgi', '21', 'Titles by Language')
print('</ul>')

print('<h4>Title Statistics</h4>')
print('<ul>')
print_line('stats.cgi', '5', 'Titles by Year of First Publication')
print_line('stats.cgi', '7', 'Titles by Author Age')
print_line('stats.cgi', '8', 'Percent of Titles in Series by Year')
print_line('most_reviewed_table.cgi', '', 'Most-Reviewed Titles (in genre publications)')
print('<li>Titles Ranked by Awards and Nominations:')
print('<ul>')
print_line('most_popular_table.cgi', '0', 'All Titles')
print_line('most_popular_table.cgi', '1', 'Novels')
print_line('most_popular_table.cgi', '2', 'Short Fiction')
print_line('most_popular_table.cgi', '3', 'Collections')
print_line('most_popular_table.cgi', '4', 'Anthologies')
print_line('most_popular_table.cgi', '5', 'Non-Fiction')
print_line('most_popular_table.cgi', '6', 'Other Types')
print('</ul>')
print_line('stats.cgi', '12', 'Top Novels as Voted by ISFDB Users')
print_line('stats.cgi', '25', 'Top Short Fiction Titles as Voted by ISFDB Users')
print('<li>Most-Viewed Titles:')
print('<ul>')
print_line('stats.cgi', '14', 'Most-Viewed Novels')
print_line('stats.cgi', '15', 'Most-Viewed Short Fiction')
print('</ul>')
print('</ul>')

print('<h4>Publication Statistics</h4>')
print('<ul>')
print_line('stats.cgi', '6', 'Publications by Year')
print_line('stats.cgi', '9', 'Percent of Books by Type by Year')
print_line('stats.cgi', '10', 'Percent of Publications by Format by Year')
print('</ul>')
print('<h4>Top ISFDB Editors</h4>')
print('<ul>')
print_line('stats.cgi', '2', 'Top Verifiers')
print_line('stats.cgi', '1', 'Top Moderators')
print_line('stats.cgi', '22', 'Top Taggers')
print_line('stats.cgi', '23', 'Top Voters')
print_line('topcontrib.cgi', '', 'Top Contributors (All Submission Types)')
print('<ul>')
for sub_type in sorted(SUBMAP.keys()):
        if SUBMAP[sub_type][3]:
                print_line('topcontrib.cgi', sub_type, 'Top Contributors (%s)' % SUBMAP[sub_type][3])
print('</ul>')
print('</ul>')
print('<h4>Historical snapshots (not up to date)</h4>')
print('<ul>')
print('<li><a href="%s://%s/degrees.html">Author Communities</a> [as of 2005]' % (PROTOCOL, HTMLHOST))
print('<li><a href="%s://%s/agestuff.html">Award-Winning Titles by Author Age</a> [as of 2005]' % (PROTOCOL, HTMLHOST))
print('<li><a href="%s://%s/index.php/Annual_Page_Views_and_Database_Growth">Database Growth and Annual Page Views</a>' % (PROTOCOL, WIKILOC))
print('</ul>')
PrintTrailer('frontpage', 0, 0)
