#!_PYTHONLOC
#
#     (C) COPYRIGHT 2021-2025   Ahasuerus
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 667 $
#     Date: $Date: 2021-06-28 18:30:46 -0400 (Mon, 28 Jun 2021) $


from awardtypeClass import *
from isfdb import *
from isfdblib import *
from SQLparsing import *
from library import ISFDBLocalRedirect


if __name__ == '__main__':

        sys.stderr = sys.stdout
        form = cgi.FieldStorage()
        try:
                title_id = int(form['title_id'].value)
                # If the passed in title ID is not 0, i.e. this is a title-based award, so load the associated title data
                if title_id:
                        title = SQLloadTitle(title_id)
                        if not title:
                                raise
        except:
                SESSION.DisplayError('Missing or Invalid Title ID') 

        try:
                award_type_id = int(form['award_type_id'].value)
                awardType = award_type()
                awardType.award_type_id = award_type_id
                awardType.load()
                if not awardType.award_type_name:
                        raise
        except:
                SESSION.DisplayError('Missing or Invalid Award Type ID')

        ISFDBLocalRedirect('edit/addaward.cgi?%d+%d' % (title_id, award_type_id))
