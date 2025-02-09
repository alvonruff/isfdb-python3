#!_PYTHONLOC
#
#     (C) COPYRIGHT 2014-2021   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 641 $
#     Date: $Date: 2021-06-17 13:27:32 -0400 (Thu, 17 Jun 2021) $


from SQLparsing import *
from common import *
from library import *
from seriesClass import *


if __name__ == '__main__':

        series_id = SESSION.Parameter(0, 'int')
        series_name = SQLFindSeriesName(series_id)
        if not series_name:
                SESSION.DisplayError('Series Does Not Exist')

	PrintHeader('All Tags for Series %s' % series_name)
	PrintNavbar('seriestags', 0, 0, 'seriestags.cgi', series_id)

        ser = series(db)
        ser.load(series_id)

        user = User()
        user.load()

        (seriesData, seriesCanonicalTitles, seriesTree, parentAuthors,
                        seriesTags, variantTitles, variantSerials, parentsWithPubs, variantAuthors,
                        translit_titles, translit_authors) = ser.BuildTreeData(user)

        ser.PrintMetaData(user, 'full', seriesTags, 'tags')

	PrintTrailer('seriestags', series_id, series_id)
