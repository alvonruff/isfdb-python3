#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2010-2025   Ahasuerus, Dirk Stoecker, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 921 $
#     Date: $Date: 2022-05-26 12:58:37 -0400 (Thu, 26 May 2022) $


from SQLparsing import *
from common import *
from seriesClass import *
from library import ISFDBLink


class SeriesGrid:
        def __init__(self):
                self.seriesId = 0
                self.seriesName = ''
                self.seriesParentId = 0
                self.seriesParent = ''
                # Display order:
                # 1 is "descending", i.e. latest year is dispayed first (default value)
                # 0 is "ascending", i.e. first year is displayed first
                self.displayOrder = 1
                self.ser = series(db)
                self.arr = AutoVivification()
                self.list_months = ('01','02','03','04','05','06','07','08','09','10','11','12','00')
                self.bgcolor = 0
                self.formats = {}
                self.default_format = ''

        def GetParameters(self):
                # Get the series parameter. May be a series name or a series record number.
                argument = SESSION.Parameter(0, 'unescape')

                # Translate the series name to its series number if necessary
                try:
                        self.seriesId = int(argument)
                except:
                        self.seriesId = 0
                
                if self.seriesId:
                        if not SQLFindSeriesName(self.seriesId):
                                if SQLDeletedSeries(self.seriesId):
                                        SESSION.DisplayError('This series has been deleted. See %s for details' % ISFDBLink('series_history.cgi', self.seriesId, 'Edit History'))
                                else:
                                        SESSION.DisplayError('Specified Series Does Not Exist')
                else:
                        self.seriesId = SQLFindSeriesId(argument)

                if not self.seriesId:
                        SESSION.DisplayError('Specified Series Does Not Exist')
                self.seriesName = SQLFindSeriesName(self.seriesId)

                # Get the Display Order.
                self.displayOrder = SESSION.Parameter(1, 'int', 1, (0, 1))

        def LoadAllSeries(self):
                # Add all EDITOR titles for this magazine series to the array
                self.LoadOneSeries()
                # Retrieve all child series and add them to the array
                children = SQLFindSeriesChildren(self.seriesId)
                for child in children:
                        self.seriesName=SQLgetSeriesName(child)
                        self.LoadOneSeries()

        def LoadOneSeries(self):
                titles = SQLFindSeriesTitles(self.seriesName)
                # Add all pubs for a list of titles to the nested dictionary
                for title in titles:
                        # Retrieve all pubs for this EDITOR title, including the parent title's pubs
                        pubs = SQLGetPubsByTitle(title[TITLE_PUBID])
                        for pub in pubs:
                                year = pub[PUB_YEAR][0:4]
                                month = pub[PUB_YEAR][5:7]
                                day = pub[PUB_YEAR][8:10]
                                format = pub[PUB_PTYPE]
                                if format not in self.formats:
                                        self.formats[format] = 0
                                self.formats[format] += 1
                                self.arr[year][month][day][pub[PUB_PUBID]]=pub

        def DetermineDefaultFormat(self):
                highest_count = 0
                for format in self.formats:
                        count = self.formats[format]
                        if count > highest_count:
                                self.default_format = format
                                highest_count = count

        def PrintHeader(self):
                self.ser.load(self.seriesId)

                user = User()
                user.load()

                title = "Issue Grid: %s" % self.ser.series_name
                PrintHeader(title)
                PrintNavbar('seriesgrid', self.seriesId, 0, 'seriesgrid.cgi', self.seriesId)

                (seriesData, seriesTitles, seriesTree, parentAuthors,
                 seriesTags, variantTitles, variantSerials, parentsWithPubs,
                 variantAuthors, translit_titles, translit_authors) = self.ser.BuildTreeData(user)

                self.ser.PrintMetaData(user, 'brief', seriesTags, 'grid')

                print('<div class="ContentBox">')
                print('<b>Format:</b> %s' % ISFDBPubFormat(self.default_format))
                if len(list(self.formats.keys())) > 1:
                        print('(unless indicated otherwise)')
                print('<br>')
                print('<b>Legend:</b> Unverified issues are gold, secondary verifications are light blue.')

                print('<p class="textindent"> %s %s ' % (ISFDBLinkNoName('pe.cgi', self.seriesId, 'View this magazine as a series'), SESSION.ui.bullet))

                if self.displayOrder:
                        print(ISFDBLink("seriesgrid.cgi", "%s+0" % self.seriesId, "Show earliest year first"))
                else:
                        print(ISFDBLink("seriesgrid.cgi", "%s+1" % self.seriesId, "Show last year first"))

        def PrintTable(self):
                print('<table class="seriesgrid">')
                print('<tr><th>&nbsp;</th>')
                for month in sorted(ISFDBmonthmap.keys()):
                        print('<th>%s</th>' % (ISFDBmonthmap[month]))
                print('<th>No month</th></tr>')
                for year in sorted(list(self.arr.keys()), reverse=self.displayOrder):
                        self.bgcolor ^= 1
                        self.PrintOneYear(year)
                
                print('</table>')
                print('</div>')

        def PrintOneYear(self, year):
                print('<tr align=center class="table%d">' % (self.bgcolor+1))
                print('<th class="year">%s</th>' % ISFDBconvertYear(year))
                for month in self.list_months:
                        if PYTHONVER == 'python2':
                                display_month = unicode(month)
                        else:
                                display_month = str(month)
                        if display_month not in self.arr[year]:
                                print('<td>-</td>')
                                continue
                        # Create a nested table
                        print('<td class="seriesgridinner"><table class="seriesgridinner">')
                        for day in sorted(self.arr[year][month]):
                                for pub_id in sorted(self.arr[year][month][day]):
                                        # Retrieve the publication record
                                        pub = self.arr[year][month][day][pub_id]
                                        # Retrieve the full title of the publication and save it off
                                        # in case the stipping algorithm strips all text
                                        title = pub[PUB_TITLE]
                                        original_title = title
                                        # Find the first place where a comma occurs
                                        comma = title.find(',')
                                        if comma != -1:
                                                # If we found a comma, then strip everything up to it
                                                title = title[comma+1:]
                                        # Convert the title to a list
                                        list_title = title.split()
                                        # 
                                        # Extract the last word from the title
                                        last_word = list_title[len(list_title)-1]
                                        # Check if the last word in the title is the same as the pub year
                                        # If it is, then strip it
                                        if last_word == year:
                                                title = title[0:len(title)-4]
                                        # Strip leading and trailing punctuation
                                        title = self.StripLeadingTrailing(title)
                                        # If the stipping algorithm stripped all text, restore the original title
                                        if not title:
                                                title = original_title
                                        # Get the verification status: 0 - not verified, 1 - primary, 2 - secondary
                                        verified = SQLVerificationStatus(pub[PUB_PUBID])
                                        color = "notverified"
                                        if verified == 1:
                                                color = "verifiedprimary"
                                        elif verified == 2:
                                                color = "verifiedsecondary"
                                        print('<tr class="seriesgridinner">')
                                        format = ''
                                        if pub[PUB_PTYPE] != self.default_format:
                                                format = ' <small>[%s]</small>' % pub[PUB_PTYPE]
                                        print('<td class="%s">%s%s</td>' % (color, ISFDBLink("pl.cgi", pub[PUB_PUBID], title), format))
                                        print('</tr>')
                        # Close the nested table
                        print('</table></td>')
                print('</tr>')

        def StripLeadingTrailing(self, title):
                # Check every character in the string starting with 1
                count = -1
                for char in title:
                        count += 1
                        # If we found a non-punctuation character, stop
                        if char not in ' ,.':
                                break
                title = title[count:len(title)]
                
                count = -1
                # Check every character in the reversed string
                for char in title[::-1]:
                        count += 1
                        if char not in ' ,.':
                                break
                title = title[0:len(title)-count]
                # Handle single character strings
                if title in ' ,.':
                        title = ''
                return title


if __name__ == '__main__':

        grid = SeriesGrid()
        grid.GetParameters()
        grid.LoadAllSeries()
        grid.DetermineDefaultFormat()
        grid.PrintHeader()
        grid.PrintTable()
        PrintTrailer('series', 0, 0)
