#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2024   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 848 $
#     Date: $Date: 2022-02-24 20:07:27 -0500 (Thu, 24 Feb 2022) $

import os
import sys
import shutil
import string
from operator import itemgetter
from library import *
from SQLparsing import *
from shared_cleanup_lib import elapsedTime

class Output():
        def __init__(self):
                self.data = ''
                self.elapsed = elapsedTime()
                self.last_count = float(0)

        def start(self, new_line):
                self.data = '%s\n' % new_line

        def append(self, new_line):
                self.data += '%s\n' % new_line

        def subheader(self, subheader):
                self.data += '<h3>%s</h3>\n' % subheader

        def file(self, report_id, report_param):
                delete = 'delete from reports where report_id = %d and report_param = %d' % (report_id, report_param)
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(delete)
                insert = """insert into reports (report_id, report_param, report_data)
                        VALUES(%d, %d, "%s")""" % (report_id, report_param, CNX.DB_ESCAPE_STRING(self.data))
                CNX.DB_QUERY(insert)

        def report(self, method_name):
                method = getattr(self, method_name)
                method()
                self.elapsed.print_elapsed(method_name)

        def LastUserActivity(self, user_id):
                if WikiExists():
                        return SQLLastUserActivity(user_id)
                else:
                        return '&nbsp;'

        def outputGraph(self, height, startyear, xscale, yscale, years, maximum, results):
                xoffset = 15
                yoffset = 10

                self.append('<svgcode width="%d" height="%d" version="1.1">' % (xoffset+40+(years*xscale), height+30+yoffset))
                self.append('<svg width="100%%" height="%dpx" version="1.1" xmlns="https://www.w3.org/2000/svg">' % (height+30+yoffset))

                ###################################################
                # Output the grid and labels - Horizontal Lines
                ###################################################
                y = 0
                increment = maximum/4
                value = increment * 4
                while y <= height:
                        self.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="svg1"/>' % (xoffset, y+yoffset, xoffset+5+(years*xscale), y+yoffset))
                        self.append('<text x="%d" y="%d" font-size="10">%d</text>' % (xoffset+10+(years*xscale), y+5+yoffset, value))
                        value -= increment
                        y = y + 50

                ###################################################
                # Output the grid and labels - Vertical Lines
                ###################################################
                x = 0
                while x < years:
                        self.append('<line x1="%d" y1="%d" x2="%d" y2="%d" class="svg1"/>' % (xoffset+(xscale*x), yoffset, xoffset+(xscale*x), height+10+yoffset))
                        self.append('<text x="%d" y="%d" font-size="10">%d</text>' % ((xscale*x)-12+xoffset, height+20+yoffset, x+startyear))
                        x += 10

                ###################################################
                # Output the data
                ###################################################
                for line_color in results:
                        index = 0
                        last = (0, 0)
                        while index < years:
                                if index:
                                        self.append('<line x1="%d"' % (xoffset+(xscale * last[0])))
                                        self.append(' y1="%d"' % (yoffset+(int(yscale * float(last[1])))))
                                        self.append(' x2="%d"' % (xoffset+(xscale * results[line_color][index][0])))
                                        self.append(' y2="%d"' % (yoffset+(int(yscale * float(maximum-results[line_color][index][1])))))
                                        self.append('class="svg%s"/>' % line_color)
                                last = (results[line_color][index][0], maximum-results[line_color][index][1])
                                index += 1

                self.append('</svg>')
                self.append('</svgcode>')

        def topModerators(self):
                self.start('<h2>Top ISFDB Moderators</h2>')
                self.append('<p>')
                self.append('<table class="generic_table">')
                self.append('<tr align=left class="table1">')
                self.append('<th>Moderator</th>')
                self.append('<th>Total</th>')
                self.append('<th>Others</th>')
                self.append('<th>Self</th>')
                self.append('<th>Last User Activity</th>')

                query = """select sub_reviewer, count(*) as total,
                        sum(case when sub_reviewer <> sub_submitter then 1 else 0 end)
                        from submissions
                        where sub_state='I'
                        and sub_reviewer != 0
                        group by sub_reviewer
                        order by total desc"""
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()

                color = 0
                while record:
                        user_id = record[0][0]
                        user_name = SQLgetUserName(user_id)
                        if color:
                                self.append('<tr align=left class="table1">')
                        else:
                                self.append('<tr align=left class="table2">')
                        self.append('<td>%s</td>' % WikiLink(user_name))
                        self.append('<td>%d</td>' % (record[0][1]))
                        self.append('<td>%d</td>' % (record[0][2]))
                        self.append('<td>%d</td>' % (record[0][1] - record[0][2]))
                        last_user_activity = self.LastUserActivity(user_id)
                        self.append('<td>%s</td>' % last_user_activity)
                        self.append('</tr>')
                        color = color ^ 1
                        record = CNX.DB_FETCHMANY()
                self.append('</table><p>')
                self.file(1, 0)

        def topVerifiers(self):
                details = {}
                primary = {}
                secondary = {}
                total = {}
                headers = {}

                # Primary verifications
                query = """select distinct count(pv.user_id), u.user_name
                        from primary_verifications pv, mw_user u
                        where exists(select 1 from pubs where pubs.pub_id = pv.pub_id)
                        and pv.user_id = u.user_id
                        group by pv.user_id"""
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                while record:
                        count = record[0][0]
                        user = record[0][1]
                        total[user] = total.get(user, 0) + count
                        primary[user] = primary.get(user, 0) + count
                        record = CNX.DB_FETCHMANY() 

                # Secondary verifications
                query = """select distinct r.reference_label, count(v.user_id), u.user_name
                        from verification v, mw_user u, reference r
                        where v.ver_status='1'
                        and exists(select 1 from pubs where pubs.pub_id=v.pub_id)
                        and v.user_id=u.user_id
                        and v.reference_id=r.reference_id
                        group by v.user_id, v.reference_id"""
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                while record:
                        source = record[0][0]
                        count = record[0][1]
                        user = record[0][2]
                        if user not in details:
                                details[user] = {}
                        if source not in details[user]:
                                details[user][source] = 0
                        details[user][source] += count
                        if source not in headers:
                                headers[source] = 0
                        total[user] = total.get(user, 0) + count
                        secondary[user] = secondary.get(user, 0) + count
                        record = CNX.DB_FETCHMANY() 

                self.start('<table cellpadding="1" class="publications">')
                self.append('<tr class="generic_table_header">')
                self.append('<th class="verifiers_user">User</th>')
                self.append('<th>Total</th>')
                self.append('<th>Primary</th>')
                self.append('<th>Secondary</th>')
                for header in sorted(headers):
                        self.append('<th>%s</th>' % header)
                self.append('</tr>')
                color = 0
                for user in sorted(total, key=total.get, reverse=True):
                        if total[user] < 10:
                                break
                        if color:
                                self.append('<tr align=left class="table1">')
                        else:
                                self.append('<tr align=left class="table2">')
                        self.append('<td>%s</td>' % WikiLink(user))

                        self.append('<td>%s</td>' % total.get(user, '&nbsp;'))

                        self.append('<td>%s</td>' % primary.get(user, '&nbsp;'))

                        self.append('<td>%s</td>' % secondary.get(user, '&nbsp;'))

                        for header in sorted(headers):
                                if user in details and header in details[user]:
                                        self.append('<td>%d</td>' % details[user][header])
                                else:
                                        self.append('<td>&nbsp;</td>')
                        self.append('</tr>')
                        color = color ^ 1

                        # This is unused
                        #record = CNX.DB_FETCHMANY()
                self.append('</table>')
                self.file(2, 0)

        def contributorStatistics(self):
                query = """select distinct sub_submitter,count(sub_submitter) as xx
                        from submissions
                        where sub_state='I'
                        group by sub_submitter
                        order by xx desc"""
                self.oneTypeContributorStatistics(query, 0)

                for sub_type in sorted(SUBMAP.keys()):
                        if SUBMAP[sub_type][3]:
                                query = """select distinct sub_submitter, count(sub_submitter) as xx
                                        from submissions
                                        where sub_state='I'
                                        and sub_type='%s'
                                        group by sub_submitter
                                        order by xx desc""" % (sub_type)
                                self.oneTypeContributorStatistics(query, sub_type)

        def oneTypeContributorStatistics(self, query, sub_type):
                self.start('<table class="generic_table">')
                self.append('<tr class="table1">')
                self.append('<th>User</th>')
                self.append('<th>Count</th>')
                self.append('<th>Privileges</th>')
                self.append('<th>Last User Activity</th>')
                self.append('</tr>')

                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()

                color = 0
                while record:
                        user_id = record[0][0]
                        count = record[0][1]
                        # Stop once we have reached the first user with fewer than 10 contributions
                        if count <10:
                                break
                        user_name = SQLgetUserName(user_id)
                        privileges = SQLUserPrivileges(user_id)
                        if color:
                                self.append('<tr align=left class="table1">')
                        else:
                                self.append('<tr align=left class="table2">')
                        self.append('<td>%s</td>' % WikiLink(user_name))
                        self.append('<td>%d</td>' % count)
                        self.append('<td>%s</td>' % privileges)
                        last_user_activity = self.LastUserActivity(user_id)
                        self.append('<td>%s</td>' % last_user_activity)
                        self.append('</tr>')
                        color = color ^ 1
                        record = CNX.DB_FETCHMANY()
                self.append('</table><p>')
                self.file(3, sub_type)

        def summaryLine(self, field, table, display):
                CNX = MYSQL_CONNECTOR()
                query = "select count(%s) from %s" % (CNX.DB_ESCAPE_STRING(field), CNX.DB_ESCAPE_STRING(table))
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHONE()
                self.append("<li><b>%s:</b> %d" % (display, record[0][0]))
                self.last_count = float(record[0][0])

        def summaryStatistics(self):
                self.start("<ul>")

                self.summaryLine('author_id', 'authors', ISFDBLink('directory.cgi', 'author', 'Authors'))
                self.summaryLine('pub_id', 'pubs', 'Publications')

                self.append("<ul>")
                query = "select distinct pub_ctype, count(pub_ctype) from pubs group by pub_ctype order by CAST(pub_ctype as CHAR)"
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                while record:
                        self.append("<li>%s: %d" % (record[0][0], record[0][1]))
                        record = CNX.DB_FETCHMANY()
                self.append("</ul>")

                query = "select count(distinct pub_id) from primary_verifications"
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHONE()
                self.append("<li><b>Verified Publications:</b> %d (%2.2f%%)" % (record[0][0], (100.0 * float(record[0][0]))/self.last_count))

                self.summaryLine('publisher_id', 'publishers', ISFDBLink('directory.cgi', 'publisher', 'Publishers'))
                self.summaryLine('pub_series_id', 'pub_series', 'Publication Series')
                self.summaryLine('title_id', 'titles', 'Titles')

                self.append("<ul>")
                query = "select distinct title_ttype, count(title_ttype) from titles group by title_ttype order by CAST(title_ttype as CHAR)"
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                while record:
                        self.append("<li>%s: %d" % (record[0][0], record[0][1]))
                        record = CNX.DB_FETCHMANY()
                self.append("</ul>")
                query = "select count(distinct title_id) from votes"
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHONE()
                self.append("<li><b>Titles with Votes:</b> %d (%2.2f%%)" % (record[0][0], (100.0 * float(record[0][0]))/self.last_count))
                
                query = "select count(distinct title_id) from tag_mapping"
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHONE()
                self.append("<li><b>Titles with Tags:</b> %d (%2.2f%%)" % (record[0][0], (100.0 * float(record[0][0]))/self.last_count))

                self.summaryLine('series_id', 'series', 'Series')
                self.summaryLine('award_type_id', 'award_types', ISFDBLink('award_directory.cgi', '', 'Award Types'))
                self.summaryLine('award_cat_id', 'award_cats', 'Award Categories')
                self.summaryLine('award_id', 'awards', 'Awards')

                self.append("<ul>")
                query = """select at.award_type_name, count(at.award_type_id)
                        from awards AS aw, award_types AS at
                        where aw.award_type_id = at.award_type_id
                        group by at.award_type_name"""
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                while record:
                        self.append("<li>%s: %d" % (record[0][0], record[0][1]))
                        record = CNX.DB_FETCHMANY()
                self.append("</ul>")

                query = """select count(*) from identifiers"""
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHONE()
                self.append('<li><b><a href="%s://%s/index.php/Template:PublicationFields:ExternalIDs">External Identifiers</a>:</b> %d' % (PROTOCOL, WIKILOC, int(record[0][0])))

                self.append("<ul>")
                query = """select it.identifier_type_name, count(i.identifier_id)
                        from identifiers i, identifier_types it
                        where i.identifier_type_id = it.identifier_type_id
                        group by it.identifier_type_id
                        order by it.identifier_type_name"""
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                while record:
                        self.append("<li>%s: %d" % (record[0][0], int(record[0][1])))
                        record = CNX.DB_FETCHMANY()
                self.append("</ul>")
                            
                self.append("</ul>")
                self.file(4, 0)

        def titlesByYear(self):
                self.data = ''
                self.byYear('NOVEL', 'Novels')
                self.byYear('SHORTFICTION', 'Short Fiction')
                self.byYear('POEM', 'Poems')
                self.byYear('REVIEW', 'Reviews')
                self.file(5, 0)

        def publicationsByYear(self):
                self.data = ''
                self.byYear('PUBS', 'Publications (without magazines)')
                self.byYear('MAGAZINES', 'Magazines')
                self.byYear('VERIFIED', 'Verified Publications in Percent')
                self.file(6, 0)

        def titlesByAuthorAge(self):
                self.data = ''
                self.byAge('NOVEL', 'all', 'All Novels')
                self.byAge('NOVEL', 'first', 'First Novels')
                self.byAge('SHORTFICTION', 'all', 'All Short Fiction')
                self.byAge('SHORTFICTION', 'first', 'First Short Fiction')
                self.file(7, 0)

        def byYear(self, chart, subheader):
                self.subheader(subheader)
                # Set the start year to 1900
                startyear = 1900
                # Set the end year to the last year
                endyear = localtime()[0]-1
                results = []
                lastyear = startyear
                if chart in ('NOVEL', 'SHORTFICTION', 'POEM', 'REVIEW'):
                        query = """select YEAR(title_copyright),COUNT(*)
                                from titles where title_ttype='%s'
                                and title_parent=0
                                and YEAR(title_copyright)>%d
                                and YEAR(title_copyright)<%d
                                group by YEAR(title_copyright)
                                order by YEAR(title_copyright)""" % (chart, startyear-1, endyear+1)
                elif chart == 'VERIFIED':
                        query = """select YEAR(p.pub_year), count(distinct p.pub_id)
                                from pubs as p, primary_verifications as pv
                                where p.pub_id = pv.pub_id
                                and YEAR(p.pub_year)>%d
                                and YEAR(p.pub_year)<%d
                                group by YEAR(p.pub_year)
                                order by YEAR(p.pub_year)""" % (startyear-1, endyear+1)
                else:
                        query = "select YEAR(pub_year),COUNT(*) from pubs where "
                        if chart == 'PUBS':
                            query += "pub_ctype!='MAGAZINE'"
                        else:
                            query += "pub_ctype='MAGAZINE'"
                        query += """ and YEAR(pub_year)>%d
                                     and YEAR(pub_year)<%s
                                     group by YEAR(pub_year)
                                     order by YEAR(pub_year)""" % (startyear-1, endyear+1)
                
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                while record:
                        year = record[0][0]
                        count = record[0][1]
                        # If there is a gap in years with no data, pad it with 0s
                        if year > (lastyear+1):
                                for missingyear in range(lastyear+1,year):
                                        tuple = (missingyear-startyear, 0)
                                        results.append(tuple)
                        tuple = (year-startyear, count)
                        results.append(tuple)
                        record = CNX.DB_FETCHMANY()
                        # Save the last year that we had data for
                        lastyear = year

                # Get the minimum and maximum values
                minimum = min(results,key=itemgetter(1))[1]
                maximum = max(results,key=itemgetter(1))[1]

                # If displaying verified pubs, do another query to get their totals for each year
                if chart == 'VERIFIED':
                    totals = []
                    lastyear = startyear
                    # Set the minimum and maximum value to 0 and 100 since we will be displaying percentages
                    maximum = 100
                    minimum = 0
                    query = """select YEAR(pub_year), COUNT(pub_id) from pubs
                                where YEAR(pub_year)>%d and YEAR(pub_year)<%d
                                group by YEAR(pub_year)
                                order by YEAR(pub_year)""" % (startyear-1, endyear+1)
                    CNX.DB_QUERY(query)
                    record = CNX.DB_FETCHMANY()
                    while record:
                        total_count = record[0][1]
                        year = record[0][0]
                        # Calculate the relative position/index of this year in the results list
                        index = year-startyear
                        # Retrieve the tuple for this year
                        tuple = results[index]
                        # Calculate the percent of verified pubs for this year
                        percent = tuple[1]*100/total_count
                        # Build the new tuple, replacing the absolute value of verified pubs with the percent value for the year
                        newtuple = (tuple[0], percent)
                        # Replace this year's tuple in the list with the percent-based data
                        results[index] = newtuple
                        # Get the next year's data
                        record = CNX.DB_FETCHMANY()
                        # Save the last year that we had data for
                        lastyear = year
                
                years = endyear-startyear+1
                height = 200
                xscale = 6
                yscale = float(height)/float(maximum-minimum)
                results_dict = {}
                results_dict['black'] = results
                self.outputGraph(height, startyear, xscale, yscale, years, maximum, results_dict)

        def byAge(self, title_type, chart, subheader):
                self.subheader(subheader)
                # Set the start age to 0
                startage = 0
                # Set the end age to 100
                endage = 101
                results = []
                lastage=startage-1
                min_age = 0
                max_age = 101

                if chart == 'all':
                    query = """select YEAR(t.title_copyright)-YEAR(a.author_birthdate),count(t.title_id)
                        from titles t, canonical_author c, authors a
                        where t.title_id=c.title_id
                        and c.author_id=a.author_id
                        and YEAR(t.title_copyright)<8888
                        and YEAR(t.title_copyright)>0
                        and title_ttype='%s'
                        and title_parent=0
                        and a.author_birthdate IS NOT NULL
                        and YEAR(t.title_copyright)-YEAR(a.author_birthdate) > %d
                        and YEAR(t.title_copyright)-YEAR(a.author_birthdate) < %d
                        group by YEAR(t.title_copyright)-YEAR(a.author_birthdate)
                        order by YEAR(t.title_copyright)-YEAR(a.author_birthdate)"""  % (title_type, min_age, max_age)
                else:
                    query = """select v.FIRST-v.DOB,count(v.FIRST-v.DOB)
                                from (select YEAR(a.author_birthdate) as DOB,
                                (select min(YEAR(t.title_copyright)) from titles t, canonical_author c
                                where t.title_copyright!='0000-00-00'
                                and t.title_id=c.title_id
                                and t.title_ttype='%s'
                                and t.title_parent=0
                                and c.author_id=a.author_id
                                and c.ca_status=1) as FIRST
                                from authors a
                                where a.author_birthdate IS NOT NULL) as v
                                where v.FIRST IS NOT NULL
                                and v.FIRST-v.DOB > %d
                                and v.FIRST-v.DOB < %d
                                group by v.FIRST-v.DOB
                                order by v.FIRST-v.DOB""" % (title_type, min_age, max_age)
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                while record:
                    age = record[0][0]
                    count = record[0][1]
                    record = CNX.DB_FETCHMANY()
                    if age is None:
                            continue
                    if age < startage or age > endage:
                            continue
                    # If there is a gap in ages with no data, pad it with 0s
                    if age > (lastage+1):
                        for missingage in range(lastage+1,age):
                            tuple = (missingage, 0)
                            results.append(tuple)
                    tuple = (age, count)
                    results.append(tuple)
                    # Save the last age that we had data for
                    lastage = age

                # Get the minimum and maximum values
                minimum = min(results,key=itemgetter(1))[1]
                maximum = max(results,key=itemgetter(1))[1]

                ages = endage-startage
                height = 200
                xscale = 6
                yscale = float(height)/float(maximum-minimum)
                results_dict = {}
                results_dict['black'] = results
                self.outputGraph(height, startage, xscale, yscale, ages, maximum, results_dict)

        def novelsInSeries(self):
                self.start('<h3>Legend: Red - novels, Blue - short fiction</h3>')
                # Set the start year to 1900
                startyear = 1900
                # Set the end year to the current year
                endyear = localtime()[0]

                results_dict = {}
                results_dict['red'] = self.novelsInSeriesoneType('NOVEL', startyear, endyear)
                results_dict['blue'] = self.novelsInSeriesoneType('SHORTFICTION', startyear, endyear)

                minimum = 0
                maximum = 100

                years = endyear-startyear+1
                height = 200
                xscale = 6
                yscale = float(height)/float(maximum-minimum)
                self.outputGraph(height, startyear, xscale, yscale, years, maximum, results_dict)
                self.file(8, 0)

        def novelsInSeriesoneType(self, title_type, startyear, endyear):
                query = """select substring(title_copyright,1,4),count(*) as total,
                        count(series_id>0) as in_series, count(series_id>0)/count(*)*100 as ratio
                        from titles
                        where title_ttype="%s"
                        and substring(title_copyright,1,4)>%d
                        and substring(title_copyright,1,4)<%d
                        and title_parent=0
                        group by substring(title_copyright,1,4)
                        order by substring(title_copyright,1,4)""" % (title_type, startyear-1, endyear+1)

                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                results = []
                while record:
                        year = record[0][0]
                        percent = record[0][3]
                        data_tuple = (int(year)-startyear, int(round(float(percent))))
                        results.append(data_tuple)
                        record = CNX.DB_FETCHMANY()
                return results

        def titlesByTypeByYear(self):
                self.start('<h3>Legend: Red - novels, Blue - collections, Green - anthologies, Yellow - omnibuses, Orange - chapbooks</h3>')
                # Set the start year to 1900
                startyear = 1900
                # Set the end year to the current year
                endyear = localtime()[0]

                # Retrieve the data from the database
                query = """select YEAR(title_copyright),title_ttype,count(*) from titles
                        where YEAR(title_copyright)>%d
                        and YEAR(title_copyright)<%d
                        and title_ttype in ('ANTHOLOGY', 'NOVEL', 'COLLECTION', 'CHAPBOOK', 'OMNIBUS')
                        and title_parent=0
                        group by YEAR(title_copyright), title_ttype""" % (startyear-1, endyear+1)
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                total = AutoVivification()
                bytype = AutoVivification()
                while record:
                    year = record[0][0]
                    title_type = record[0][1]
                    count = record[0][2]
                    if not total[year]:
                            total[year] = 0
                    total[year] += count
                    if not bytype[title_type][year]:
                            bytype[title_type][year] = 0
                    bytype[title_type][year] += count
                    record = CNX.DB_FETCHMANY()

                # Add any missing years
                for title_type in bytype.keys():
                        for year in range(startyear,endyear+1):
                                if year not in bytype[title_type]:
                                        bytype[title_type][year] = 0

                colors = {'red' : 'NOVEL',
                          'blue': 'COLLECTION',
                          'green': 'ANTHOLOGY',
                          'yellow':  'OMNIBUS',
                          'orange': 'CHAPBOOK'}
                results_dict = {}
                for color in colors:
                        title_type = colors[color]
                        results_dict[color] = []
                        for year in bytype[title_type]:
                                percent = bytype[title_type][year] * 100 / total[year]
                                year_tuple = (int(year) - startyear, percent)
                                results_dict[color].append(year_tuple)

                minimum = 0
                maximum = 100

                years = endyear-startyear+1
                height = 200
                xscale = 6
                yscale = float(height)/float(maximum-minimum)
                self.outputGraph(height, startyear, xscale, yscale, years, maximum, results_dict)
                self.file(9, 0)

        def byFormat(self, report_type):
                if report_type == 'magazines':
                        pub_types = "in ('MAGAZINE', 'FANZINE')"
                        self.append('<h3>Magazines and Fanzines</h3>')
                        colors = {'red' : 'pulp',
                                  'blue': 'digest',
                                  'green': 'webzine',
                                  'orange': 'ebook',
                                  'yellow': 'quarto',
                                  'pink': 'digital audio download',
                                  'black': 'all others'
                                  }
                else:
                        pub_types = "not in ('MAGAZINE', 'FANZINE')"
                        self.append('<h3>Books</h3>')
                        colors = {'red' : 'pb',
                                  'yellow': 'tp',
                                  'green': 'hc',
                                  'orange': 'ebook',
                                  'black': 'all others'
                                  }
                self.append('<h3>Legend:')
                # Define recognized formats and print the legend
                recognized = []
                for color in sorted(colors):
                        format = colors[color]
                        recognized.append(format)
                        if color != 'black':
                                self.append('%s - %s, ' % (color.capitalize(), ISFDBPubFormat(format)))
                self.append('Black - all other formats</h3>')
                
                # Set the start year to 1900
                startyear = 1900
                # Set the end year to the last year (current year may not have enough data points)
                endyear = localtime()[0]-1

                # Retrieve the data from the database
                query = """select YEAR(pub_year), pub_ptype, count(*)
                           from pubs where YEAR(pub_year)>%d
                           and YEAR(pub_year)<%d
                           and pub_ptype != 'unknown'
                           and pub_ctype %s
                           group by pub_ptype, YEAR(pub_year)""" % (startyear-1, endyear+1, pub_types)
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                total = AutoVivification()
                bytype = AutoVivification()
                while record:
                    year = record[0][0]
                    pub_type = record[0][1]
                    count = record[0][2]
                    if not total[year]:
                            total[year] = 0
                    total[year] += count
                    if pub_type not in recognized:
                            pub_type = 'all others'
                    if not bytype[pub_type][year]:
                            bytype[pub_type][year] = 0
                    bytype[pub_type][year] += count
                    record = CNX.DB_FETCHMANY()

                # Add any missing years
                for pub_type in bytype.keys():
                        for year in range(startyear,endyear+1):
                                if year not in bytype[pub_type]:
                                        bytype[pub_type][year] = 0

                results_dict = {}
                for color in colors:
                        pub_type = colors[color]
                        results_dict[color] = []
                        for year in bytype[pub_type]:
                                percent = bytype[pub_type][year] * 100 / total[year]
                                year_tuple = (int(year) - startyear, percent)
                                results_dict[color].append(year_tuple)
                minimum = 0
                maximum = 100

                years = endyear-startyear+1
                height = 200
                xscale = 6
                yscale = float(height)/float(maximum-minimum)
                self.outputGraph(height, startyear, xscale, yscale, years, maximum, results_dict)

        def pubsByFormat(self):
                self.start('')
                self.byFormat('magazines')
                self.byFormat('books')
                self.file(10, 0)

        def authorsByDebutDate(self):
                delete = "delete from authors_by_debut_date"
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(delete)
                query = """insert into authors_by_debut_date (debut_year, author_id, title_count)
                        select MIN(date_format(t.title_copyright,'%Y')) debut,
                        a.author_id, count(t.title_id) NumTitles
                        from titles t, canonical_author ca, authors a
                        where t.title_copyright not in ('0000-00-00', '8888-00-00')
                        and t.title_ttype IN ('NOVEL', 'COLLECTION', 'SHORTFICTION', 'POEM')
                        and ca.ca_status=1
                        and ca.title_id = t.title_id
                        and ca.author_id = a.author_id
                        and t.title_parent = 0
                        and a.author_canonical not in ('Anonymous', 'unknown', 'uncredited')
                        GROUP BY ca.author_id
                        HAVING NumTitles > 5"""
                CNX.DB_QUERY(query)

        def submissionsByYear(self):
                # Set the start year to 2007
                startyear = 2007
                # Set the end year to the last year
                currentyear = localtime()[0]
                lastyear = currentyear - 1
                years = lastyear - startyear + 1

                # Retrieve the data from the database
                query = """select YEAR(sub_time), count(*)
                        from submissions
                        where YEAR(sub_time) > 2006
                        group by YEAR(sub_time)
                        order by YEAR(sub_time)"""
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                results_dict = {}
                results_dict['black'] = []
                minimum = 0
                maximum = 0
                years_dict = {}
                while record:
                        year = record[0][0]
                        count = record[0][1]
                        years_dict[year] = int(count)
                        if count > maximum:
                                maximum = count
                        record = CNX.DB_FETCHMANY()
                # If there is no data, don't create the report
                if not maximum:
                        return
                # Populate years with no submissions with 0s
                for year in range(startyear, currentyear):
                        if year in years_dict:
                                data_tuple = (year - startyear, years_dict[year])
                        else:
                                data_tuple = (year - startyear, 1)
                        results_dict['black'].append(data_tuple)
                height = 200
                xscale = 50
                yscale = float(height)/float(maximum - minimum)
                self.start('')
                self.outputGraph(height, startyear, xscale, yscale, years, maximum, results_dict)
                self.file(11, 0)

        def topNovels(self):
                self.top100('novel', 12)
        
        def topShorts(self):
                self.top100('short', 25)
        
        def top100(self, report_type, report_id):
                if report_type == 'novel':
                        ttype = 'NOVEL'
                elif report_type == 'short':
                        ttype = 'SHORTFICTION'

                self.start('')
                query = """select t.title_id, t.title_title, DATE_FORMAT(t.title_copyright, '%%Y-%%m-%%d') as year, AVG(v.rating)
                        from titles t, votes v
                        where t.title_id = v.title_id
                        and t.title_ttype = '%s'
                        group by t.title_id
                        having COUNT(v.rating)>5
                        order by AVG(v.rating) desc limit 500""" % ttype
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()

                self.append('<table class="generic_table">')
                self.append('<tr class="generic_table_header">')
                self.append('<th>Rank</th>')
                self.append('<th>Rating</th>')
                self.append('<th>Title</th>')
                self.append('<th>Year</th>')
                self.append('<th>Author(s)</th>')
                self.append('</tr>')
                counter = 1
                color = 1
                while record:
                        if color:
                                self.append('<tr align=left class="table1">')
                        else:
                                self.append('<tr align=left class="table2">')
                        self.append('<td>%d</td>' % counter)
                        self.append('<td>%2.2f</td>' % record[0][3])
                        self.append('<td>%s</td>' % ISFDBLink('title.cgi', record[0][0], record[0][1]))
                        self.append('<td>%s</td>' % record[0][2][:4])
                        authors = SQLTitleBriefAuthorRecords(int(record[0][0]))
                        self.append('<td>')
                        self.append(LIBbuildRecordList('author', authors))
                        self.append('</td>')
                        self.append('</tr>')
                        record = CNX.DB_FETCHMANY()
                        counter += 1
                        color = color ^ 1
                self.append('</table>')
                self.file(report_id, 0)

        def mostViewedAuthors(self):
                query = """select av.views, av.author_id, a.author_canonical
                           from authors a, author_views av
                           where a.author_id = av.author_id
                           order by av.views desc
                           limit 500"""
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()

                self.start('<table class="seriesgrid">')
                self.append('<tr>')
                for header in ('Rank', 'Views', 'Author'):
                        self.append('<th>%s</th>' % header)
                self.append('</tr>')
                bgcolor = 0
                rank = 1
                while record:
                        self.append('<tr class="table%d">' % (bgcolor+1))
                        self.append('<td>%s</td>' % rank)
                        self.append('<td>%s</td>' % record[0][0])
                        self.append('<td>')
                        self.append(ISFDBLink('ea.cgi', record[0][1], record[0][2]))
                        self.append('</td>')
                        self.append('</tr>')
                        record = CNX.DB_FETCHMANY()
                        bgcolor ^= 1
                        rank += 1
                self.append('</table>')
                self.file(13, 0)

        def authorDisplay(self, query, headers, report_id, note = None):
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()

                self.start('')
                if note:
                        self.append('<h3>Note: %s</h3>' % note)

                self.append('<table class="seriesgrid">')
                self.append('<tr>')
                for header in headers:
                        self.append('<th>%s</th>' % header)
                self.append('</tr>')
                bgcolor = 0
                while record:
                        self.append('<tr class="table%d">' % (bgcolor+1))
                        self.append('<td>%s</td>' % (record[0][0]))
                        self.append('<td>%s</td>' % (record[0][2]))
                        self.append('<td>')
                        self.append(ISFDBLink('ea.cgi', record[0][3], record[0][1]))
                        self.append('</td>')
                        self.append('</tr>')
                        record = CNX.DB_FETCHMANY()
                        bgcolor ^= 1
                self.append('</table>')
                self.file(report_id, 0)

        def mostViewedNovels(self):
                self.mostViewed('NOVEL', 14)

        def mostViewedShorts(self):
                self.mostViewed('SHORTFICTION', 15)

        def mostViewed(self, title_type, report_id):
                self.start('<table class="seriesgrid">')
                self.append('<tr>')
                self.append('<th>Rank</th>')
                self.append('<th>Views</th>')
                self.append('<th>Title</th>')
                self.append('<th>Year</th>')
                self.append('<th>Authors</th>')
                self.append('</tr>')
                CNX = MYSQL_CONNECTOR()
                query = """select tv.views, tv.title_id, t.title_title, t.title_copyright
                           from titles t, title_views tv
                           where t.title_ttype='%s'
                           and t.title_id = tv.title_id
                           order by tv.views desc
                           limit 500""" % (CNX.DB_ESCAPE_STRING(title_type))
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                bgcolor = 0
                rank = 1
                while record:
                        views = record[0][0]
                        title_id = record[0][1]
                        title_title = record[0][2]
                        title_year = ISFDBconvertYear(record[0][3])
                        self.append('<tr align=left class="table%d">' % (bgcolor+1))
                        self.append('<td>%d</d>' % rank)
                        self.append('<td>%d</td>' % views)
                        self.append('<td>%s</td>' % ISFDBLink('title.cgi', title_id, title_title))
                        self.append('<td>%s</td>' % title_year)
                        self.append('<td>')
                        authors = SQLTitleBriefAuthorRecords(title_id)
                        self.append(LIBbuildRecordList('author', authors))
                        self.append('</td>')
                        self.append('</tr>')
                        bgcolor = bgcolor ^ 1
                        rank += 1
                        record = CNX.DB_FETCHMANY()
                self.append('</table>')
                self.file(report_id, 0)

        def oldestLivingAuthors(self):
                query = """select YEAR(NOW())-YEAR(author_birthdate) as age,
                           author_canonical, author_birthdate, author_id
                           from authors
                           where author_birthdate is not null
                           and YEAR(author_birthdate) != '0000'
                           and author_deathdate is null
                           and YEAR(NOW())-YEAR(author_birthdate) > 84
                           and YEAR(NOW())-YEAR(author_birthdate) < 117
                           order by author_birthdate"""
                headers = ('Age', 'Date of Birth', 'Author')
                note = """The following list includes authors whose year of birth
                          is between 85 and 116 years in the past and who do not
                          have a year of death on file"""
                self.authorDisplay(query, headers, 16, note)

        def oldestNonLivingAuthors(self):
                query = """select YEAR(author_deathdate)-YEAR(author_birthdate) as age,
                        author_canonical, author_birthdate, author_id
                        from authors
                        where author_birthdate is not null
                        and author_deathdate is not null
                        and YEAR(author_birthdate) != '0000'
                        and YEAR(author_deathdate) != '0000'
                        and YEAR(author_deathdate)-YEAR(author_birthdate) > 84
                        order by YEAR(author_deathdate)-YEAR(author_birthdate) desc"""
                headers = ('Age', 'Date of Birth', 'Author')
                note = """The following list includes authors whose year of birth
                          is between 85 and 116 years in the past and who
                          have a known year of death on file"""
                self.authorDisplay(query, headers, 17, note)

        def youngestLivingAuthors(self):
                query = "select YEAR(NOW())-YEAR(author_birthdate) as age, author_canonical, author_birthdate, "
                query += "author_id from authors where author_birthdate is not null and author_deathdate is null "
                query += "and YEAR(NOW())-YEAR(author_birthdate) < 40 order by author_birthdate desc"
                headers = ('Age', 'Date of Birth', 'Author')
                self.authorDisplay(query, headers, 18)

        def youngestNonLivingAuthors(self):
                query = """select YEAR(author_deathdate)-YEAR(author_birthdate) as age,
                           author_canonical, author_birthdate, author_id from authors
                           where author_birthdate is not null
                           and YEAR(author_birthdate) != '0000'
                           and author_deathdate is not null
                           and YEAR(author_deathdate) != '0000'
                           and YEAR(author_deathdate)-YEAR(author_birthdate) < 40
                           and YEAR(author_deathdate)-YEAR(author_birthdate) > 0
                           order by YEAR(author_deathdate)-YEAR(author_birthdate)"""
                headers = ('Age', 'Date of Birth', 'Author')
                self.authorDisplay(query, headers, 19)

        def authorsByLanguage(self):
                query = "select author_language, count(*) cnt from authors group by author_language"
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                rows = []
                total = 0
                while record:
                        lang_id = record[0][0]
                        if lang_id == 0:
                                language = 'Undefined'
                        elif not lang_id:
                                language = 'To Be Assigned'
                        else:
                                language = LANGUAGES[lang_id]
                        lang_count = -record[0][1]
                        total += record[0][1]
                        row = (lang_count, language)
                        rows.append(row)
                        record = CNX.DB_FETCHMANY()

                self.start('<h4>Total authors: %d</h4>' % total)
                self.append('<p>')
                self.append('<table class="seriesgrid">')
                self.append('<tr>')
                self.append('<th>Working Language</th>')
                self.append('<th>Count</th>')
                self.append('<th>Percent</th>')
                self.append('</tr>')
                bgcolor = 1
                for row in sorted(rows):
                        self.append('<tr class="table%d">' % bgcolor)
                        count = -row[0]
                        language = row[1]
                        self.append('<td>%s</td>' % language)
                        self.append('<td>%d</td>' % count)
                        self.append('<td>% 3.2f</td>' % (count*100/float(total)))
                        self.append('</tr>')
                        bgcolor ^= 1
                self.append('</table>')
                self.file(20, 0)

        def titlesByLanguage(self):
                query = "select title_language, count(*) cnt from titles group by title_language"
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                rows = []
                total = 0
                while record:
                        lang_id = record[0][0]
                        if lang_id == 0:
                                language = 'Undefined'
                        elif not lang_id:
                                language = 'To Be Assigned'
                        else:
                                language = LANGUAGES[lang_id]
                        lang_count = -record[0][1]
                        total += record[0][1]
                        row = (lang_count, language)
                        rows.append(row)
                        record = CNX.DB_FETCHMANY()

                self.start('<h4>Total titles: %d</h4>' % total)
                self.append('<p>')
                self.append('<table class="seriesgrid">')
                self.append('<tr>')
                self.append('<th>Language</th>')
                self.append('<th>Count</th>')
                self.append('<th>Percent</th>')
                self.append('</tr>')
                bgcolor = 1
                for row in sorted(rows):
                        self.append('<tr class="table%d">' % bgcolor)
                        count = -row[0]
                        language = row[1]
                        self.append('<td>%s</td>' % language)
                        self.append('<td>%d</td>' % count)
                        self.append('<td>% 3.2f</td>' % (count*100/float(total)))
                        self.append('</tr>')
                        bgcolor ^= 1
                self.append('</table>')
                self.file(21, 0)

        def topTaggers(self):
                self.start('<h2>Top ISFDB Taggers</h2>')
                self.append('<p>')
                self.append('<table class="generic_table">')
                self.append('<tr class="table1">')
                self.append('<th>User</th>')
                self.append('<th>Tags</th>')
                self.append('<th>Last User Activity</th>')
                self.append('</tr>')

                query = "select distinct user_id,count(user_id) as xx from tag_mapping group by user_id order by xx desc"
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()

                color = 0
                while record:
                        user_id = record[0][0]
                        count = record[0][1]
                        # Only display users with 10+ tags
                        if count < 10:
                                break
                        user_name = SQLgetUserName(user_id)
                        if color:
                                self.append('<tr align=left class="table1">')
                        else:
                                self.append('<tr align=left class="table2">')
                        self.append('<td>%s</td>' % WikiLink(user_name))
                        self.append('<td>%d</td>' % count)
                        self.append('<td>%s</td>' % SQLLastUserActivity(user_id))
                        self.append('</tr>')
                        color = color ^ 1
                        record = CNX.DB_FETCHMANY()
                self.append('</table>')
                self.file(22, 0)

        def topVoters(self):
                self.start('<h2>Top ISFDB Voters</h2>')
                self.append('<p>')
                self.append('<table class="generic_table">')
                self.append('<tr class="table1">')
                self.append('<th>User</th>')
                self.append('<th>Votes</th>')
                self.append('<th>Last User Activity</th>')
                self.append('</tr>')

                query = "select distinct user_id,count(user_id) as xx from votes group by user_id order by xx desc"
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()

                color = 0
                while record:
                        user_id = record[0][0]
                        count = record[0][1]
                        # Only display users with 10+ votes
                        if count < 10:
                                break
                        user_name = SQLgetUserName(user_id)
                        if color:
                                self.append('<tr align=left class="table1">')
                        else:
                                self.append('<tr align=left class="table2">')
                        self.append('<td>%s</td>' % WikiLink(user_name))
                        self.append('<td>%d</td>' % count)
                        self.append('<td>%s</td>' % SQLLastUserActivity(user_id))
                        self.append('</tr>')
                        color = color ^ 1
                        record = CNX.DB_FETCHMANY()
                self.append('</table>')
                self.file(23, 0)

        def topForthcoming(self):
                self.start("<h3>The following forthcoming novels are those with the most interest as generated")
                self.append("by the users of the ISFDB. Note: Information based on pre-publication data and subject to change.</h3>")
                self.append('<p>')

                query = """select tv.views, t.title_title, t.title_id, t.title_copyright
                        from titles t, title_views tv
                        where t.title_id = tv.title_id
                        and t.title_ttype = 'NOVEL'
                        and tv.views > 0
                        and t.title_copyright > NOW()
                        and YEAR(t.title_copyright) < (YEAR(CURDATE())+5)
                        order by tv.views desc
                        limit 50"""

                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()

                self.append('<table>')
                self.append('<tr>')
                self.append('<th>Rank</th>')
                self.append('<th>Title</th>')
                self.append('<th>Author(s)</th>')
                self.append('<th>Date</th>')
                self.append('</tr>')
                bgcolor = 1
                title_count = 1
                while record:
                        if bgcolor:
                                line = '<tr align=left class="table1">'
                        else:
                                line = '<tr align=left class="table2">'
                        line += '<td>%d</td>' % title_count
                        line += '<td>%s</td>' % ISFDBLink('title.cgi', record[0][2], record[0][1])

                        authors = SQLTitleBriefAuthorRecords(int(record[0][2]))
                        author_count = 0
                        line += '<td>'
                        for author in authors:
                                if author_count > 0:
                                        line += ', '
                                line += ISFDBLink('ea.cgi', author[0], author[1])
                                author_count += 1
                        line += '</td>'

                        line += '<td>%s</td>' % record[0][3]
                        line += '</tr>'
                        self.append(line)
                        record = CNX.DB_FETCHMANY()
                        bgcolor ^= 1
                        title_count += 1

                self.append('</table>')
                self.file(24, 0)

        def mostReviewed(self):
                # Initialize the dictionary which will hold review counts for title IDs
                counts = {}
                # Initialize the dictionary which will hold years for title IDs
                years = {}
                # Initialize the list of parent title IDs
                parents = []
                # Retrieve all reviewed title IDs, their dates and IDs of their parent titles
                query = """select t.title_id,t.title_parent,YEAR(t.title_copyright)
                           from title_relationships as r, titles as t
                           where r.title_id=t.title_id"""
                CNX = MYSQL_CONNECTOR()
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()
                while record:
                        title_id = record[0][0]
                        parent_id = record[0][1]
                        year = record[0][2]
                        # If this title is a VT, add its parent to the list of parents to be retrieved later
                        if parent_id != 0:
                                title_id = parent_id
                                if str(parent_id) not in parents:
                                        parents.append(str(parent_id))
                        # Increment the count of reviews for this title ID
                        counts[title_id] = counts.get(title_id, 0) +1
                        years[title_id] = year
                        record = CNX.DB_FETCHMANY()
                # Convert the list of parent IDs to a string in the SQL IN clause format
                parents_string = ','.join(parents)

                # Retrieve dates of parent titles
                query = "select title_id, YEAR(title_copyright) from titles where title_id in (%s)" % (CNX.DB_ESCAPE_STRING(parents_string))
                CNX.DB_QUERY(query)
                record = CNX.DB_FETCHMANY()

                while record:
                        title_id = record[0][0]
                        year = record[0][1]
                        # If the parent's year is less than the variant's, use the parent's year
                        if (years[title_id] == 0) or (year < years[title_id]):
                                years[title_id] = year
                        record = CNX.DB_FETCHMANY()

                CNX.DB_QUERY("truncate most_reviewed")
                values = []
                for title_id in counts:
                        reviews = counts[title_id]
                        year = years[title_id]
                        if year < 1900:
                                decade = 'pre1900'
                        else:
                                decade = str(year)[:3] + '0'
                        values.append((int(title_id), int(year), decade, int(reviews)))
                        if len(values) > 300:
                                self.most_reviewed_file(values)
                                values = []
                if values:
                        self.most_reviewed_file(values)

        def most_reviewed_file(self, values):
                mycursor = db.cursor()
                insert = """insert into most_reviewed(title_id, year, decade, reviews)
                             VALUES(%s, %s, %s, %s)"""
                mycursor.executemany(insert, values)
                db.commit()

        def awardTitles(self):
                import awards
                award_titles = awards.awardTitles()
                award_titles.buildAwardTitles()

def database_stats():
        output = Output()
        output.report("awardTitles")
        output.report("submissionsByYear")
        output.report("titlesByYear")
        output.report("publicationsByYear")
        output.report("titlesByAuthorAge")
        output.report("summaryStatistics")
        output.report("contributorStatistics")
        output.report("topVerifiers")
        output.report("topModerators")
        output.report("novelsInSeries")
        output.report("titlesByTypeByYear")
        output.report("pubsByFormat")
        output.report("authorsByDebutDate")
        output.report("topNovels")
        output.report("topShorts")
        output.report("mostViewedAuthors")
        output.report("mostViewedNovels")
        output.report("mostViewedShorts")
        output.report("oldestLivingAuthors")
        output.report("oldestNonLivingAuthors")
        output.report("youngestLivingAuthors")
        output.report("youngestNonLivingAuthors")
        output.report("authorsByLanguage")
        output.report("titlesByLanguage")
        output.report("topTaggers")
        output.report("topVoters")
        output.report("topForthcoming")
        output.report("mostReviewed")
        print("SUCCESS")
