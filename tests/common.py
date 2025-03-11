#
#     (C) COPYRIGHT 2025   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#

# Stolen from biblio/common.py

def PrintWebPages(webpages, format = '<li>'):
        if not webpages:
                return
        printed = {}
        for webpage in webpages:
                # Get the corrected link and the displayed form of this URL
                (corrected_webpage, display, home_page, linked_page) = BuildDisplayedURL(webpage)
                # Add this URL to the list of sites for this domain
                if display not in printed:
                        printed[display] = []
                printed[display].append(corrected_webpage)
        total = 0
        # Sort all domain names, recognized as well as unrecognized, in a case-insensitive way
        for display in sorted(list(printed.keys()), key=lambda x: x.lower()):
                count = 1
                # Retrieve Web page urls for this domain name
                for webpage in printed[display]:
                        if not total:
                                output = "%s<b>Webpages:</b> " % format
                                total = 1
                        else:
                                output += ", "
                        # If there is more than one URL with this domain for this author, show its relative number
                        qualifier = ''
                        if len(printed[display]) > 1:
                                qualifier = "-%d" % (count)
                        output += '<a href="%s" target="_blank">%s%s</a>' % (webpage, display, qualifier)
                        count += 1
        print(output)
