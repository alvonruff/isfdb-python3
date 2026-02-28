from __future__ import print_function
#
#     (C) COPYRIGHT 2007-2026   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1269 $
#     Date: $Date: 2026-02-26 14:26:55 -0500 (Thu, 26 Feb 2026) $

import sys
if sys.version_info.major == 3:
        PYTHONVER = "python3"
elif sys.version_info.major == 2:
        PYTHONVER = "python2"

import re
import string
import traceback
import cgi
from SQLparsing import *
from xml.dom import minidom
from xml.dom import Node
from datetime import datetime

################################################################
# The functions and classes in this module are used across all
# ISFDB directories
################################################################

def ISFDBDate():
        return datetime.today().strftime('%Y-%m-%d')

ISFDBmonthmap = {
        1  : 'Jan',
        2  : 'Feb',
        3  : 'Mar',
        4  : 'Apr',
        5  : 'May',
        6  : 'Jun',
        7  : 'Jul',
        8  : 'Aug',
        9  : 'Sep',
        10 : 'Oct',
        11 : 'Nov',
        12 : 'Dec',
}

def ISFDBAuthorError(value):
        # Plus signs are not allowed because they are used as delimiters
        # in the body of the submission (to be changed later)
        if '+' in value:
                return 'Plus signs are currently not allowed in author names'
        else:
                return ''

def ISFDBDifferentAuthorStrings(first_author_string, second_author_string):
        first_author_list = first_author_string.split('+')
        second_author_list = second_author_string.split('+')
        if set([x.lower() for x in first_author_list]) != set([x.lower() for x in second_author_list]):
                return 1
        else:
                return 0

def ISFDBDifferentAuthorLists(first_author_list, second_author_list):
        # Note that the first author list contains XML-escaped names while the second one doesn't
        if set([x.lower() for x in first_author_list]) != set([XMLescape(x).lower() for x in second_author_list]):
                return 1
        else:
                return 0

def ISFDBAuthorInAuthorList(author_name, author_list):
        if author_name.lower() not in [x.lower() for x in author_list]:
                return 0
        else:
                return 1

def ISFDBnormalizeAuthor(value):
        # Convert double quotes to single quotes
        value = str.replace(value,'"',"'")
        # Strip all leading, trailing and double spaces
        # How did this ever work?
        #return str.join(str.split(value))
        return ' '.join(str.split(value))

def ISFDBnormalizeDate(date):
        now = datetime.now()
        # This function takes a date and normalizes it to be in the standard 'YYYY-MM-DD' format
        # For invalid dates, '0000-00-00' is returned
        date = str.replace(date, "'", '')
        date = str.replace(date, "<", '')
        date = str.replace(date, ">", '')
        date = str.replace(date, " ", '')

        # Check for missing date elements
        if len(date) < 4:
                return '0000-00-00'
        elif len(date) == 4:
                date = '%s-00-00' % date
        elif len(date) == 7:
                date = '%s-00' % date
        elif len(date) != 10:
                return '0000-00-00'

        if (date[4] != '-') or (date[7] != '-'):
                return '0000-00-00'

        # Make sure the date elements are all integers and pass date validation
        try:
                year = int(date[0:4])
                month = int(date[5:7])
                day = int(date[8:10])
                if (year > (now.year +1)) and (year != 8888) and (year != 9999):
                        return '0000-00-00'
                elif month > 12:
                        return '0000-00-00'
                else:
                        # Determine the last day of the specified month. For '00' month, the max day is 31 in MySQL
                        maxday = 31
                        if (month == 4) or (month == 6) or (month == 9) or (month == 11):
                                maxday = 30
                        elif month == 2:
                                maxday = 28
                                leap = 0
                                # Years divisible by 400 are leap years
                                if year % 400 == 0:
                                        leap = 1
                                # Years divisble by 100 but not by 400 are not leap years
                                elif year % 100 == 0:
                                        leap = 0
                                # Years divisible by 4, but not by 100 are leap years
                                elif year % 4 == 0:
                                        leap = 1
                                if leap:
                                        maxday = 29
                        if day > maxday:
                                return '0000-00-00'
        except ValueError:
                return '0000-00-00'

        return date

def ISFDBconvertForthcoming(theDate):
        year  = theDate[0:4]
        month = int(theDate[5:7])
        day   = theDate[8:10]
        if month:
                if int(day):
                        datestr = "%s %s %s" % (ISFDBmonthmap[month], day, year)
                else:
                        datestr = "%s %s" % (ISFDBmonthmap[month], year)
        else:
                datestr = year
        return datestr

def ISFDBconvertYear(date):
        if not date:
                date = '0000'
        year = str(date)[:4]
        if year == '0000':
                yearstr = 'unknown'
        elif year == '8888':
                yearstr = ISFDBunpublishedDate()
        elif year == '9999':
                yearstr = 'forthcoming'
        else:
                yearstr = year
        return yearstr

def ISFDBunpublishedDate():
        return 'unpublished'

def ISFDBconvertDate(theDate, precise = 0):
        try:
                if theDate == '0000-00-00':
                        datestr = 'date unknown'
                elif theDate == '8888-00-00':
                        datestr = ISFDBunpublishedDate()
                elif theDate == '9999-00-00':
                        datestr = 'forthcoming'
                elif precise:
                        datestr = theDate
                else:
                        month = str.split(theDate, "-")[1]
                        if month:
                                try:
                                        strmonth = ISFDBmonthmap[int(month)]
                                        datestr = "%s %s" % (strmonth, theDate[:4])
                                except (ValueError, KeyError):
                                        datestr = theDate[:4]
                        else:
                                datestr = theDate[:4]
        except (AttributeError, TypeError):
                datestr = ''
        return datestr


##########################################################################
#  Compare two dates and return:
#    1 if Date 1 is before Date 2
#    2 if Date is more precise than Date 2
#    0 is neither is the case
##########################################################################
def ISFDBCompare2Dates(date1, date2):
        # If date1 is blank or '0000-00-00', it can't be "before" or "more precise" than date2
        if not date1 or (date1 == '0000-00-00'):
                return 0
        # If date2 is blank or '0000-00-00' and date1 is not (already checked above), then date1 is more precise
        if not date2 or (date2 == '0000-00-00'):
                return 2
        date1_year = date1[0:4]
        date1_month = date1[5:7]
        date1_day = date1[8:10]
        date2_year = date2[0:4]
        date2_month = date2[5:7]
        date2_day = date2[8:10]
        # If the first year is after the second year, then return 0
        if int(date1_year) > int(date2_year):
                return 0
        # If the first year is before the second year, return 1
        if int(date1_year) < int(date2_year):
                return 1
        #
        # If the two years are the same, compare the two months
        #
        # If the month of date1 is unknown, then it's neither more precise nor before date2
        if date1_month == '00':
                return 0
        # If the month of date2 is unknown and the month of date1 is known, then date1 is more precise
        if date2_month == '00':
                return 2
        # If the first month is after the second month, then date1 is not before date2
        if int(date1_month) > int(date2_month):
                return 0
        # If the first month is before the second month, then date1 is before date2
        if int(date1_month) < int(date2_month):
                return 1
        #
        # If the years and months are the same, compare days
        #
        # If date1 is unknown, it's neither before nor more precise than date2
        if date1_day == '00':
                return 0
        # If the day of date2 is unknown and the day of date1 is known, then date1 is more precise
        if date2_day == '00':
                return 2
        if int(date1_day) < int(date2_day):
                return 1
        return 0

##############################################
# Obtains the value associated with a
# particular XML tag.
##############################################
def GetElementValue(element, tag):
        document = element[0].getElementsByTagName(tag)
        try:
                if PYTHONVER == 'python2':
                        value = document[0].firstChild.data.encode('iso-8859-1')
                else:
                        value = document[0].firstChild.data
        except (IndexError, AttributeError):
                value = ''
        return value

def GetChildValue(doc, label):
        try:
                tag = doc.getElementsByTagName(label)[0]
                if PYTHONVER == 'python2':
                        value = tag.firstChild.data.encode('iso-8859-1')
                else:
                        value = tag.firstChild.data
        except (IndexError, AttributeError):
                value = ''
        return value

def XMLunescape(input, compliant = 0):
        retval = str.replace(str(input), "&amp;", "&")
        # If standards-compliant XML was requested, unescape &apos;.
        # Internally we use HTML-specific &rsquo; instead (for now)
        if compliant:
                retval = str.replace(retval, "&apos;", "'")
        else:
                retval = str.replace(retval, "&rsquo;", "'")
        retval = str.replace(retval, "&quot;", '"')
        retval = str.replace(retval, "&lt;", "<")
        retval = str.replace(retval, "&gt;", ">")
        retval = str.strip(retval)
        retval = str.rstrip(retval)
        return retval

def XMLunescape2(input):
        # un-encode quotes
        retval = str.replace(str(input), "&rsquo;", "'")
        retval = str.replace(retval, "&quot;", '"')
        # sometimes we get \r + \n, sometimes just \n.
        # remove any \r instances.
        retval = str.replace(retval, "\r", "")
        # remove leading + trailing spaces
        retval = str.strip(retval)
        retval = str.rstrip(retval)
        return retval

##############################################
# Determines whether or not a particular
# XML tag is present in the given element.
##############################################
def TagPresent(element, tag):
        try:
                document = element.getElementsByTagName(tag)[0]
        except (IndexError, AttributeError):
                try:
                        document = element[0].getElementsByTagName(tag)
                except (IndexError, AttributeError, TypeError):
                        return 0
        if document:
                return 1
        else:
                return 0

def normalizeInput(retval):
        retval = str(retval)
        # First replace ". . . ." with "....", otherwise ". . . ." will be converted to "... ."
        while ". . . ." in retval:
                retval = retval.replace(". . . .", "....")

        ###################################################################################
        # Replace and/or remove various characters
        ###################################################################################
        replace_dict = {}
        for char in range(0,32):
                # Do not replace carriage return and line feed since they are legal
                if char in (10,13):
                        continue
                # Convert tabs to spaces
                elif char == 9:
                        replace_dict[chr(char)] = ' '
                # Remove all other control characters
                else:
                        replace_dict[chr(char)] = ''

        # Replace double spaces with single spaces
        replace_dict['  '] = ' '
        # Replace ". . ." with "..."
        replace_dict['. . .'] = '...'
        # Replace the single ellipsis character with three dots
        replace_dict[chr(133)] = '...'
        # Replace Latin-1 and Unicode punctuation with ASCII equivalents
        replace_dict[chr(130)] = ','
        replace_dict[chr(132)] = '"'
        replace_dict[chr(145)] = "'"
        replace_dict[chr(146)] = "'"
        replace_dict[chr(147)] = '"'
        replace_dict[chr(148)] = '"'
        replace_dict[chr(160)] = ' '
        replace_dict[chr(173)] = '' # Soft hyphen

        retval = replaceDict(retval, replace_dict)

        # Next replace characters followed by invalid Unicode characters,
        # including "combining diacritics", with Latin-1 equivalents where
        # available, otherwise decimally HTML-encoded Unicode equivalents
        replace_dict = ISFDBUnicodeTranslation()
        retval = replaceDict(retval, replace_dict)
        return retval

def replaceDict(retval, replace_dict):
        # Perform the actual replacement
        for key in replace_dict:
                while key in retval:
                        retval = retval.replace(key, replace_dict[key])
        return retval


###################################################
# This function converts input, typically from
# an editing form, into a format that can be
# utilized in an XML structure.
###################################################

def XMLescape(input, compliant = 0):

        retval = normalizeInput(input)

        ###########################################
        # Replace the usual ASCII characters with
        # their escaped equivalents for XML
        ###########################################
        retval = str.replace(retval, "&", "&amp;")
        # If standards-compliant XML was requested, use &apos;. Internally we use HTML-specific &rsquo; instead (for now)
        if compliant:
                retval = str.replace(retval, "'", "&apos;")
        else:
                retval = str.replace(retval, "'", "&rsquo;")
        retval = str.replace(retval, '"', "&quot;")
        retval = str.replace(retval, "<", "&lt;")
        retval = str.replace(retval, ">", "&gt;")

        ###########################################
        # Sometimes we get \r + \n, sometimes just
        # \n.  Remove all instances of \r.
        ###########################################
        retval = str.replace(retval, "\r", "")

        ###########################################
        # Strip off leading and trailing spaces
        ###########################################
        retval = str.strip(retval)
        retval = str.rstrip(retval)
        return retval

def ISFDBHostCorrection(value, mode = 'start'):
        # Replace www.isfdb.org with the current host/Wiki location and adjust http/https
        if not value:
                return value
        if mode == 'start':
                if value.startswith('http://www.isfdb.org/wiki/'):
                        value = '%s://%s/%s' % (PROTOCOL, WIKILOC, value[26:])
                elif value.startswith('https://www.isfdb.org/wiki/'):
                        value = '%s://%s/%s' % (PROTOCOL, WIKILOC, value[27:])
        elif mode == 'all':
                value = value.replace('http://www.isfdb.org/wiki/', '%s://%s/' % (PROTOCOL, WIKILOC))
                value = value.replace('https://www.isfdb.org/wiki/', '%s://%s/' % (PROTOCOL, WIKILOC))
                value = value.replace('http://www.isfdb.org/cgi-bin/', '%s://%s/' % (PROTOCOL, HTFAKE))
                value = value.replace('https://www.isfdb.org/cgi-bin/', '%s://%s/' % (PROTOCOL, HTFAKE))
        return value

def IMDBLink(title_code, displayed_link = 'IMDB'):
        if title_code:
                imdb_link = '<a href="https://www.imdb.com/title/%s/" target="_blank">%s</a>' % (title_code, ISFDBText(displayed_link))
        else:
                imdb_link = ''
        return imdb_link

def ISFDBScan(pub_id, pub_image, css_class = 'scans'):
        pub_image = ISFDBHostCorrection(pub_image).split("|")[0]
        if not pub_image:
                return ''
        image_link = '<img src="%s" alt="Image" class="%s">' % (pub_image, css_class)
        if pub_id:
                image_link = '<a href="%s:/%s/%s?%s" dir="ltr">%s</a>' % (PROTOCOL, HTFAKE, 'pl.cgi', pub_id, image_link)
        return image_link

def ISFDBFormatImage(value, pub_id = '', css_class = 'tallscan'):
        image = ISFDBScan(pub_id, value, css_class)
        if not image:
                return ''
        display_value = '%s<br>[%s]' % (image, value)

        if WIKILOC in value:
                try:
                        wikilink = value.split(WIKILOC)[1].split('/')[-1]
                        wikilink = '%s://%s/index.php/Image:%s' % (PROTOCOL, WIKILOC, wikilink)
                        display_value += '<br><a href="%s" target="_blank">ISFDB Wiki page for this image</a>' % wikilink
                except IndexError:
                        pass
        return display_value

def ISFDBLinkNoName(script, record_id, displayed_value, brackets=False, argument=''):
        return ISFDBLink(script, record_id, displayed_value, brackets, argument, {})

def ISFDBLink(script, record_id, displayed_value, brackets=False, argument='', transliterations = None):
        # Special case: author "uncredited" is displayed without a link for performance reasons
        if script == 'ea.cgi' and displayed_value == 'uncredited':
                return 'uncredited'
        trans_functions = {'ea.cgi': SQLloadTransAuthorNames,
                           'pe.cgi': SQLloadTransSeriesNames,
                           'pl.cgi': SQLloadTransPubTitles,
                           'title.cgi': SQLloadTransTitles,
                           'publisher.cgi': SQLloadTransPublisherNames,
                           'pubseries.cgi': SQLloadTransPubSeriesNames
                           }
        trans_function = trans_functions.get(script, None)
        separator = "?"
        if record_id == '':
                separator = ''
        if argument:
                argument += ' '
        link = '<a %shref="%s:/%s/%s%s%s" dir="ltr">%s</a>' % (argument, PROTOCOL,
                                                               HTFAKE, script,
                                                               separator, record_id,
                                                               ISFDBText(displayed_value))
        # Transliterated values
        trans_values = None
        # If a list of transliterated values was passed in and contains
        # transliterated values for this record ID, display them
        if transliterations is not None:
                trans_values = transliterations.get(record_id, None)
        # If no transliterations were passed in, the record ID is numeric,
        # and the CGI script is associated with a data retrieval function,
        # use that function to retrieve transliterations
        elif trans_function and str(record_id).isdigit():
                trans_values = trans_function(record_id)
        # If transliterated values have been found, add them to the link
        if trans_values:
                link = ISFDBMouseover(mouseover_values = trans_values,
                                      display_value = link, tag = '', html_escape = False)
        if brackets:
                link = '[%s]' % link
        return link

def ISFDBText(text, escape_quotes = False):
        if PYTHONVER == 'python2':
                from cgi import escape
                text = escape('%s' % text, escape_quotes)
        else:
                from html import escape
                text = escape('%s' % text, escape_quotes)
        if UNICODE != "utf-8":
                text = text.replace("&amp;#","&#")
        return text

def ISFDBPubFormat(format_code, position = 'right'):
        formats = {'pb': """Paperback. Typically 7" by 4.25" (18 cm by 11 cm) or smaller,
                            though trimming errors can cause them to sometimes be slightly
                            (less than 1/4 extra inch) taller or wider/deeper.""",
                   'tp': """Trade paperback. Any softcover book which is at least 7.25"
                            (or 19 cm) tall, or at least 4.5" (11.5 cm) wide/deep.""",
                   'hc': """Hardcover. Used for all hardbacks of any size.""",
                   'ph': """Pamphlet. Used for short (in page count), unbound, staple-bound,
                            or otherwise lightly bound publications.""",
                   'digest': """Books which are similar in size and binding to digest-formatted
                            magazines, using the standard digest size of approximately 7" by 4.5""",
                   'dos': """Dos-a-dos or tete-beche formatted paperback books, such as Ace Doubles
                            and Capra Press back-to-back books.""",
                   'audio CD': "Compact disc with standard audio tracks",
                   'audio MP3 CD': "Compact disc with mp3-encoded audio tracks ",
                   'audio MP3 DVD': "DVD with mp3-encoded audio tracks ",
                   'audio MP3 USB Drive': "Thumb (flash) USB drive with mp3-encoded audio tracks ",
                   'audio cassette': "Cassette tape",
                   'audio LP': "Long-playing record (vinyl)",
                   'digital audio player': "Player with a pre-loaded digital file of the audiobook",
                   'digital audio download': """Digital recording in any format that is downloaded
                            directly from the Internet. This category includes podcasts.""",
                   'digest': """Digest-size magazine, including both standard digest size, at about
                            7" by 4.5", and also large digest, such as recent issues of Asimov's,
                            which are about 8.25" by 5.125".""",
                   'pulp': """Magazine using the common pulp size: 6.5" by 9.5". For ISFDB purposes
                            this may also be used as a designation for the quality of the paper.
                            There are some untrimmed pulps that are as large as 8" by 11.75""",
                   'bedsheet': """8.5" by 11.25" magazines, e.g. early issues of Amazing; or the
                            1942-43 issues of Astounding.""",
                   'tabloid': """11" by 16" magazine, usually newsprint, e.g. British Science Fiction Monthly.""",
                   'A4': """21 cm by 29.7 cm or 8.3" by 11.7" magazine, used by some UK and European magazines""",
                   'A5': """14.8 cm by 21 cm or 5.8" by 8.3" magazine, used by some UK and European magazines""",
                   'quarto': """8.5" by 11" magazine, usually saddle-stapled, instead of side-stapled or glued""",
                   'octavo': """5.5" by 8.5" magazine, usually saddle-stapled, instead of side-stapled or glued""",
                   'ebook': """Used for all electronic formats, including but not limited to EPUB,
                            eReader, HTML, iBook, Mobipocket, and PDF.""",
                   'webzine': """Used for Internet-based periodical publications which are otherwise
                            not downloadable as an "ebook".""",
                   'other': """The publication format is non-standard. The details are usually provided
                            publication notes.""",
                   'unknown': """The publication record was created from a secondary source and
                            the publication format is unknown."""
                   }
        mouseover_text = formats.get(format_code, '')
        while "\n" in mouseover_text:
                mouseover_text = mouseover_text.replace("\n", " ")
        mouseover_text = normalizeInput(mouseover_text)

        if mouseover_text:
                display_value = ISFDBMouseover((mouseover_text,), format_code, '', SESSION.ui.question_mark, position)
        else:
                display_value = format_code
        return display_value

def ISFDBPrice(price, location = 'right'):
        if price == '':
                return ''
        mouseover_text = ''
        symbols = {'A$': 'Australian dollar. ISO code: AUD',
                   'Ar$': 'Argentine peso. ISO code: ARS',
                   SESSION.currency.baht: 'Thai baht. ISO code: THB',
                   'Bfr ': 'Belgian franc. ISO code: BEF',
                   'C$': 'Canadian dollar. ISO code: CAD',
                   'CHF ': 'Swiss franc. ISO code: CHF',
                   'CLP$': 'Chilean peso. ISO code: CLP',
                   'COL$': 'Colombian peso. ISO code: COP',
                   'Din ': 'Serbian and Yugoslavian dinar. ISO codes: YUF in 1945-1966, YUD in 1966-1989, YUN in 1990-1992, YUR in July 1992-September 1993, YUO in October-December 1993, YUG in early January 1994, YUM in 1994-2003, CSD in 2003-2006, RSD since 2006',
                   'dkr ': 'Danish krone (crown). ISO code: DKK',
                   '$': 'US dollar. ISO code: USD',
                   '$U': 'Uruguayan peso. ISO codes: UYN in 1896-1975, UYP in 1975-1993, UYU since 1993',
                   'DM ': 'German (Deutsche) mark. ISO code: DEM in 1948-1999',
                   SESSION.currency.euro: 'Euro. ISO code: EUR',
                   'Ft ': 'Hungarian forint. ISO code: HUF',
                   'F': 'French frank. ISO code: FRF in 1960-1999',
                   SESSION.currency.guilder: 'Dutch guilder. ISO code: NLG in 1810s-1999',
                   'HK$': 'Hong Kong dollar. ISO code: HKD',
                   'hrn ': 'Ukrainian hryvnia. ISO code: UAH',
                   '%s ' % SESSION.currency.czech_koruna: 'Czech koruna (crown). ISO code: CZK',
                   '%s ' % SESSION.currency.czechoslovak_koruna: 'Czechoslovak koruna (crown). ISO codes: CSJ in 1919-1939 and 1945-1953, CSK in 1953-1993',
                   'kn ': 'Croatian kuna. ISO code: HRK in 1994-2023',
                   'Lei ': 'Romanian leu. ISO codes: ROK in 1947-1952, ROL in 1952-2005, RON since 2005',
                   'Lev ': 'Bulgarian lev. ISO codes: BGJ in 1881-1952, BGK in 1952-1962, BGL in 1962-1999, BGN since 1999',
                   'Lit ': 'Italian lira. ISO code: ITL in 1861-1999',
                   SESSION.currency.german_gold_mark: 'German gold mark',
                   'Mx$': 'Mexican dollar. ISO codes: MXP until 1993, MXN since 1993',
                   'M ': 'East German mark. ISO code: DDM in 1948-1990',
                   'nkr ': 'Norwegian krone (crown). ISO code: NOK',
                   'NT$': 'Taiwan dollar. ISO code: TWD. Unofficial abbreviation NTD for "New Taiwan Dollar"',
                   'NZ$': 'New Zealand dollar. ISO code: NZD',
                   'P$': 'Portuguese escudo. ISO code: PTE',
                   SESSION.currency.peso: 'Philippine peso. ISO code: PHP',
                   'Pta ': 'Spanish peseta. ISO code: ESP',
                   SESSION.currency.pound: 'UK pound. ISO code: GBP',
                   'R ': 'South African rand. ISO code: ZAR',
                   'R$': 'Brazilian real. ISO code: BRL',
                   'Rub ': 'Russian or Soviet ruble. ISO codes: SUR in 1961-1991, RUR in 1992-1997, RUB since 1998',
                   SESSION.currency.indian_rupee: 'Indian rupee. ISO code: INR',
                   SESSION.currency.pakistani_rupee: 'Pakistani rupee. ISO code: PKR',
                   'S ': 'Austrian schilling. ISO code: ATS in 1945-1999',
                   'S$': 'Singapore dollar. ISO code: SGD',
                   'skr ': 'Swedish krona (crown). ISO code: SEK',
                   'Tk ': 'Bangladesh Taka. ISO code: BDT',
                   'TL ': 'Turkish lira. ISO code: TRY',
                   SESSION.currency.won:  'South Korean won. ISO code: KRW',
                   SESSION.currency.yen:  'Japanese yen. ISO code: JPY',
                   SESSION.currency.yuan: 'Chinese renminbi/yuan. ISO code: CNY',
                   '%s ' % SESSION.currency.zloty: 'Polish zloty. ISO codes: PLZ in 1950-1994, PLN since 1995'
                   }
        if '/' in price:
                mouseover_text = """Prior to decimilisation (1968-1971), UK books were priced
                                in shillings, or shillings and pence, where 20 shillings
                                equals one pound and 12 old pence equals one shilling.
                                Shillings were indicated with a variety of suffixes, e.g.
                                3s, 3', 3", 3/ all mean 3 shillings. Any number after that
                                is additional pence, usually 6 (half a shilling) but
                                sometimes 3 or 9 (a quarter of a shilling or three-quarters
                                of a shilling)."""
        else:
                found = 0
                for symbol in symbols:
                        if price == symbol:
                                found = 1
                        elif price.lower().startswith(symbol.lower()) and price[len(symbol)].isdigit():
                                found = 1
                        if found:
                                mouseover_text = '%s: %s' % (symbol.strip(), symbols[symbol])
                                break
        if mouseover_text:
                display_value = ISFDBMouseover((mouseover_text,), price, '', SESSION.ui.question_mark, location)
        else:
                display_value = price
        return display_value

class ISFDBTable():
        def __init__(self):
                self.headers = ['#']
                self.headers_colspan = [1]
                self.display_count = 1
                self.rows = []
                self.table_css = 'generic_table'
                self.header_css = 'generic_table_header'
                self.row_align = 'center'

        def PrintTable(self):
                print('<table class="%s">' % self.table_css)
                print('<tr align="left" class="%s">' % self.header_css)
                self._PrintHeaders()
                print('</tr>')
                self._PrintBody()
                print('</table>')

        def _PrintHeaders(self):
                for count, header in enumerate(self.headers):
                        colspan = 1
                        try:
                                colspan = self.headers_colspan[count]
                        except IndexError:
                                pass
                        print('<th colspan="%d">%s</th>' % (colspan, header))

        def _PrintBody(self):
                for index, row in enumerate(self.rows):
                        if index % 2 == 0:
                                row_css = 'table1'
                        else:
                                row_css = 'table2'
                        print('<tr align="%s" class="%s">' % (self.row_align, row_css))
                        if self.display_count:
                                print('<td>%d</td>' % (index + 1))
                        for cell in row:
                                if cell != '' and cell is not None:
                                        print('<td>%s</td>' % cell)
                                else:
                                        print('<td>&nbsp;</td>')
                        print('</tr>')

class AutoVivification(dict):
        """Emulate Perl's autovivification feature"""
        def __getitem__(self, item):
                try:
                    return dict.__getitem__(self, item)
                except KeyError:
                    value = self[item] = type(self)()
                    return value

def roman2int(roman):
        # Convert a roman numeral to regular integer format
        conversion = { 'm':1000, 'd':500, 'c':100, 'l':50, 'x':10, 'v':5, 'i':1 }
        sum = 0
        roman = roman.lower()
        for i in range(len(roman)):
                if roman[i] in conversion:
                        value = conversion[roman[i]]
                else:
                        return 0
                if i < (len(roman)-1):
                        if roman[i+1] in conversion:
                                nextvalue = conversion[roman[i+1]]
                        else:
                                return 0
                        if nextvalue > value:
                                value *= -1
                sum += value
        return sum

def ConvertPageNumber(page):
        # Returns a tuple with the following sorting information for one page number:
        #  1. page group
        #  2. normalized page number
        #  3. decimal part of the page number
        # The page groups are:
        #    1 for "no page", 2 for "cover", 3 for "roman", 4 for "arabic", 5 for "back"
        if not page:
                return (1, 0, '')

        # If the page value contains a "pipe" character (|), then everything before the pipe is
        # the display value and the everything after the pipe is the "sort" value
        pipe_list = page.split('|')
        # If there is a pipe, then change the page value to what's to the right of the pipe
        if len(pipe_list) > 1:
                page = pipe_list[1]
        # Re-check the page number now that it may have been repaced with the "sort" value
        if not page:
                return (1, 0, '')

        # If the first and last characters are square brackets, remove them
        if page[0] == '[' and page[-1] == ']':
                page = page[1:-1]

        # "fc" means "front cover"
        if page == 'fc':
                return (2, 1, '')

        # "rj" means "reverse jacket", i.e. inside of the dust jacket
        if page == 'rj':
                return (2, 2, '')

        # "fep" means "front end paper" or inside front cover of a magazine
        if page == 'fep':
                return (2, 3, '')

        # "bp" means "unpaginated pages that precede pagination"
        if page == 'bp':
                return (2, 4, '')

        # "ep" means "unpaginated pages that follow pagination"
        if page == 'ep':
                return (5, 1, '')

        # "bep" means "back end paper" or inside back cover of a magazine
        if page == 'bep':
                return (5, 2, '')

        # "bc" means "back cover"
        if page == 'bc':
                return (5, 3, '')

        # Extract the integer and decimal parts of the page value
        numeric_list = page.split('.')
        if len(numeric_list) > 1:
                integer_part = numeric_list[0]
                decimal_part = numeric_list[1]
        else:
                integer_part = page
                decimal_part = ''

        # Check if the supposed integer part of the page number is really an integer
        try:
                integer_part = int(integer_part)
                return (4, integer_part, decimal_part)
        except ValueError:
                # If the supposed integer part is not an integer, check if it's a roman numeral
                integer_part = roman2int(integer_part)
                if integer_part:
                        return (3, integer_part, decimal_part)
                # If it's neither an arabic numeral nor a roman numeral, then it is unrecognized, so we will display this page value first
                else:
                        return (1, 0, decimal_part)


def getPubContentList(pubid):
        pub_content_list = SQLGetPubContentList(pubid)
        sorted_list = []
        alphabetical_position = 1
        # Build a list of content items with "sort group" and "normalized page number" information
        for pub_content_record in pub_content_list:
                page = pub_content_record[PUB_CONTENTS_PAGE]
                (group, normalized_page, decimal_part) = ConvertPageNumber(str(page))
                sorted_list.append((group, normalized_page, decimal_part, alphabetical_position, pub_content_record))
                alphabetical_position += 1
        # Re-sort the list of content items based on group, page number and record's title
        sorted_list.sort()
        # Strip intermediate sorting data and build a list of content record in display order
        result = []
        for content_item in sorted_list:
                result.append(content_item[4])
        return result

def getSortedTitlesInPub(pub_id):
        titles = SQLloadTitlesXBT(pub_id)
        title_dict = {}
        for title in titles:
                title_dict[title[TITLE_PUBID]] = title
        sorted_contents = getPubContentList(pub_id)
        new_titles = []
        for content in sorted_contents:
                title_id = content[PUB_CONTENTS_TITLE]
                # Check that the title ID retrieved from the table of contents titles
                # is in the main list of titles for this pub in case of data corruption
                if title_id in title_dict:
                        title = title_dict[title_id]
                        new_titles.append(title)
        return new_titles

def FormatNote(note, note_type = '', display_mode = 'short', record_id = 0, record_type = '', div = 1):
        if PYTHONVER == 'python2':
                import urllib
        else:
                import urllib.request, urllib.parse, urllib.error
        note = ISFDBHostCorrection(note, 'all')
        if display_mode == 'short' and '{{BREAK}}' in note:
                note = note[:note.index('{{BREAK}}')]
                note += """ ... <big><a class="inverted" href="%s:/%s/note.cgi?%s+%d">view
                        full %s</a></big>""" % (PROTOCOL, HTFAKE, record_type, int(record_id), note_type)
        # Strip {{BREAK}} for full note display mode, but not for edit mode
        if display_mode == 'full' and '{{BREAK}}' in note:
                # Replace {{BREAK}} and any spaces next to it with a single space
                note1 = note[:note.index('{{BREAK}}')].rstrip(' ')
                note2 = note[note.index('{{BREAK}}')+9:].lstrip(' ')
                note = note1 + ' ' + note2

        templates = SQLLoadAllTemplates()
        # Substitute templates
        for template in templates:
                dict_node = templates[template]
                template_link = dict_node[0]
                if len(dict_node) > 1:
                        template_name = dict_node[1]
                else:
                        template_name = ''
                if len(dict_node) > 2:
                        template_description = dict_node[2]
                else:
                        template_description = ''
                # Non-record based templates
                if '%s' not in template_link:
                        pattern = "{{"+template+"}}"
                # Record-based templates
                else:
                        pattern = "{{"+template+"\|"
                # Make the regex pattern case-insensitive
                regex = re.compile(pattern, flags=re.I)
                fragments = regex.split(note)
                if '%s' not in template_link:
                        if template_link == '':
                                substituted_text = template_name
                        else:
                                substituted_text = '<a href="%s">%s</a>' % (template_link, template_name)
                        if template_description:
                                substituted_text = '<abbr class="template" title="%s">%s</abbr>' % (template_description, substituted_text)
                        note = substituted_text.join(fragments)
                        continue
                note = ''
                count = 0
                for fragment in fragments:
                        # The first fragment is everything to the left of the first occurrence of this template
                        if not count:
                                note = fragment
                                count += 1
                                continue
                        fragment_pieces = fragment.split('}}')
                        linking_value = fragment_pieces[0]
                        # Create a link only if a linking value was entered
                        if linking_value:
                                # Replace the '%s' in the template link with a URL-escaped version of the linking value
                                actual_link = template_link % Portable_urllib_quote(linking_value)
                                # If there is no template name, use the linking value as the display value
                                if not template_name:
                                        display_value = linking_value
                                # If there is a template name, display it first, then display the linking value
                                else:
                                        display_value = '%s %s' % (template_name, linking_value)
                                # For URLs, add the actual link and the display value to the note
                                if template_link[:4] == 'http':
                                        full_value = '<a href="%s">%s</a>' % (actual_link, display_value)
                                else:
                                        full_value = display_value
                                if template_description:
                                        full_value = '<abbr class="template" title="%s">%s</abbr>' % (template_description, full_value)
                                note += full_value

                        # Add the rest of the original text to the body of the note
                        note += '}}'.join(fragment_pieces[1:])

        retval = note

        # Remove all '<!--isfdb specific-->' strings which were used for magazine links in the past
        retval = str.replace(retval, '<!--isfdb specific-->','')
        list_of_brs = ('br', 'br/', 'br /', 'Br', 'Br/', 'Br /', 'BR', 'BR/', 'BR /')
        # Replace double <br>s with <p> (which will be replaced with two newlines later)
        for element in list_of_brs:
                double_element = '<' + element + '>' + '<' + element + '>'
                while double_element in retval:
                        retval = str.replace(retval, double_element, '<p>')
        # Replace HTML <br>s with regular carriage returns
        for element in list_of_brs:
                enclosed_element = '<' + element + '>'
                retval = str.replace(retval, enclosed_element, '\n')

        # Convert all double carriage returns, which may have resulted from the <br> conversion above, into single carriage returns
        while '\n\n' in retval:
                retval = str.replace(retval, '\n\n', '\n')

        # Remove all carriage returns before and after <p> and <ul> to avoid creating additional displayed new lines
        for element in ('p', '/p', 'ul', 'li', '/li'):
                enclosed = '<' + element + '>'
                enclosed_upper = enclosed.upper()
                prefixed_element = ' ' + enclosed
                while prefixed_element in retval:
                        retval = str.replace(retval, prefixed_element, enclosed)
                suffixed_element = enclosed + ' '
                while suffixed_element in retval:
                        retval = str.replace(retval, suffixed_element, enclosed)
                retval = str.replace(retval, '\n' + enclosed, enclosed)
                retval = str.replace(retval, enclosed + '\n', enclosed)
                retval = str.replace(retval, '\n' + enclosed_upper, enclosed_upper)
                retval = str.replace(retval, enclosed_upper + '\n', enclosed_upper)

        # Replace HTML <p>s with two regular carriage returns
        retval = str.replace(retval, '<p>', '\n\n')
        retval = str.replace(retval, '<P>', '\n\n')

        # Remove leading and trailing spaces (but not newlines)
        retval = str.strip(retval, ' ')

        if div:
                if note_type:
                        retval = '<div class="notes"><b>%s:</b> %s</div>' % (note_type, retval)
                else:
                        retval = '<div class="notes">%s</div>' % (retval)
        return retval

def ISFDBLocalRedirect(script):
        location = '%s:/%s/%s' % (PROTOCOL, HTFAKE, script)
        _ServerSideRedirect(location)

def ISFDBExternalRedirect(location):
        _ServerSideRedirect(location)

def _ServerSideRedirect(location):
        print('Status: 303 See Other')
        print('Location: %s' % location)
        print('Content-type: text/html; charset=%s\n' % (UNICODE))
        print('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">')
        print('<html lang="en-us">')
        print('<body>')
        print('</body>')
        sys.exit(0)

def ISFDBFormatAllAuthors(title_id, prefix = '', suffix = ''):
        authors = SQLTitleBriefAuthorRecords(title_id)
        return '%s%s%s' % (prefix, FormatAuthors(authors), suffix)

def FormatAuthors(authors):
        counter = 0
        output = ''
        for author in authors:
                if counter:
                        output += " <b>and</b> "
                output += ISFDBLink('ea.cgi', author[0], author[1])
                counter += 1
        return output

def AwardLevelDescription(award_level, award_id):
        # Load the award type record for this award
        from awardtypeClass import award_type
        awardType = award_type()
        awardType.award_type_id = award_id
        awardType.load()
        # Retrieve the list of special award levels
        special_awards = awardType.SpecialAwards()

        if not award_level:
                award_level_desc = ''
        elif award_level in special_awards:
                award_level_desc = special_awards[award_level]
        elif awardType.award_type_poll == 'Yes':
                award_level_desc = award_level
        else:
                if award_level == '1':
                        award_level_desc = "Win"
                else:
                        award_level_desc = "Nomination"
        return award_level_desc

def ISFDBSubmissionType(recordType, subtype, doc2):
        from xml.dom import minidom
        from xml.dom import Node
        # Since XML tag "NewPub" is used for "New Pub", "Add Pub to Title", "Import Contents", "Export Contents"
        # and "Clone Pub", we need to check the sub-tags inside the XML body to determine the actual type
        if recordType == 'NewPub':
                if GetElementValue(doc2, 'ClonedTo'):
                        recordType = 'ImportExport'
                elif GetElementValue(doc2, 'Parent'):
                        if subtype == MOD_PUB_NEW:
                                recordType = 'AddPub'
                        elif subtype == MOD_PUB_CLONE:
                                recordType = 'ClonePub'
        if recordType in SUBMISSION_TYPE_DISPLAY:
                recordType = SUBMISSION_TYPE_DISPLAY[recordType]
        return recordType

def ISFDBUnicodeTranslation():
##      Possible candidates:
##        '&#699;' : "'",      # Modifier letter turned comma
##        '&#700;' : "'",      # Modified letter apostrophe
        replace = {
                   '&#146;': "'",       # Windows-1252 apostrophe
                   '&#165;': SESSION.currency.yen,  # Unicode yen changed to regular yen
                   '&#847;': '',        # Combining Grapheme Joiner, which we replace with "no character"
                   '&#8192;': ' ',      # En quad space
                   '&#8193;': ' ',      # Em quad space
                   '&#8194;': ' ',      # En space
                   '&#8195;': ' ',      # Em space
                   '&#8196;': ' ',      # Three-per-em space
                   '&#8197;': ' ',      # Four-per-em space
                   '&#8198;': ' ',      # Six-per-em space
                   '&#8199;': ' ',      # Figure space
                   '&#8200;': ' ',      # Punctuation space
                   '&#8201;': ' ',      # Thin space
                   '&#8202;': ' ',      # Hair space
                   '&#8203;': '',       # Zero width space, which we replace with "no character"
                   '&#8204;': '',       # Zero width non-joiner, which we replace with "no character"
                   '&#8205;': '',       # Zero width joiner, which we replace with "no character"
                   '&#8206;': '',       # Left-To-Right character
                   '&#8207;': '',       # Right-To-Left character
                   '&#8216;': "'",      # Left single quotation mark
                   '&#8217;': "'",      # Right single quotation mark
                   '&#8218;': "'",      # Single low-reverse-9 quotation mark
                   '&#8219;': "'",      # Single high-reverse-9 quotation mark
                   '&#8220;': '"',      # Left double quotation mark
                   '&#8221;': '"',      # Right double quotation mark
                   '&#8222;': '"',      # Double low-reverse-9 quotation mark
                   '&#8223;': '"',      # Double high-reverse-9 quotation mark
                   '&#8230;': '...',    # Horizontal ellipsis
                   '&#8232;': '',       # Line separator
                   '&#8239;': ' ',      # Narrow no-break space
                   '&#8287;': ' ',      # Medium mathematical space
                   '&#8288;': '',       # Word joiner, which we replace with "no character"
                   '&#12288;':' ',      # Ideographic space
                   '&#65279;':'',       # Zero width no-break space, which we replace with "no character"
                   '&#65284;':'$',      # Fullwidth Unicode dollar sign changed to regular dollar sign
                   '&#65505;': SESSION.currency.pound, # Fullwidth Unicode pound sign changed to regular pound sign
                   '&#65509;': SESSION.currency.yen,   # Fullwidth Unicode yen changed to regular yen
                   '&#65510;': SESSION.currency.won,   # Fullwidth Unicode won changed to regular won
                   'A&#768;': chr(192), # A grave accent
                   'A&#769;': chr(193), # A acute accent
                   'A&#770;': chr(194), # A cirmuflex accent
                   'A&#771;': chr(195), # A tilde
                   'A&#772;': '&#256;', # A macron
                   'A&#774;': '&#258;', # A breve
                   'A&#775;': '&#550;', # A dot above
                   'A&#776;': chr(196), # A diaresis/umlaut
                   'A&#778;': chr(197), # A ring above
                   'A&#780;': '&#461;', # A caron
                   'A&#783;': '&#512;', # A double grave
                   'A&#785;': '&#514;', # A inverted breve
                   'A&#808;': '&#260;', # A ogonek
                   'C&#769;': '&#262;', # C acute accent
                   'C&#770;': '&#264;', # C cirmuflex accent
                   'C&#775;': '&#266;', # C dot above
                   'C&#780;': '&#268;', # C caron
                   'C&#807;': chr(199), # C cedilla
                   'D&#780;': '&#270;', # D caron
                   'E&#768;': chr(200), # E grave accent
                   'E&#769;': chr(201), # E acute accent
                   'E&#770;': chr(202), # E cirmuflex accent
                   'E&#772;': '&#274;', # E macron
                   'E&#774;': '&#276;', # E breve
                   'E&#775;': '&#278;', # E dot above
                   'E&#776;': chr(203), # E diaresis/umlaut
                   'E&#780;': '&#282;', # E caron
                   'E&#783;': '&#516;', # E double grave
                   'E&#785;': '&#518;', # E inverted breve
                   'E&#807;': '&#552;', # E cedilla
                   'E&#808;': '&#280;', # E ogonek
                   'G&#769;': '&#500;', # G acute accent
                   'G&#770;': '&#284;', # G cirmuflex accent
                   'G&#774;': '&#286;', # G breve
                   'G&#775;': '&#288;', # G dot above
                   'G&#780;': '&#486;', # G caron
                   'G&#807;': '&#290;', # G cedilla
                   'H&#770;': '&#292;', # H cirmuflex accent
                   'H&#780;': '&#542;', # H caron
                   'I&#768;': chr(204), # I grave accent
                   'I&#769;': chr(205), # I acute accent
                   'I&#770;': chr(206), # I cirmuflex accent
                   'I&#771;': '&#296;', # I tilde
                   'I&#772;': '&#298;', # I macron
                   'I&#774;': '&#300;', # I breve
                   'I&#775;': '&#304;', # I dot above
                   'I&#776;': chr(207), # I diaresis/umlaut
                   'I&#780;': '&#463;', # I caron
                   'I&#783;': '&#520;', # I double grave
                   'I&#785;': '&#522;', # I inverted breve
                   'I&#808;': '&#302;', # I ogonek
                   'J&#770;': '&#308;', # J cirmuflex accent
                   'K&#780;': '&#488;', # K caron
                   'K&#807;': '&#310;', # K cedilla
                   'L&#769;': '&#313;', # L acute accent
                   'L&#780;': '&#317;', # L caron
                   'L&#807;': '&#315;', # L cedilla
                   'N&#768;': '&#504;', # N grave accent
                   'N&#769;': '&#323;', # N acute accent
                   'N&#771;': chr(209), # N tilde
                   'N&#775;': '&#7748;', # N dot above
                   'N&#780;': '&#327;', # N caron
                   'N&#807;': '&#325;', # N cedilla
                   'O&#768;': chr(210), # O grave accent
                   'O&#769;': chr(211), # O acute accent
                   'O&#770;': chr(212), # O cirmuflex accent
                   'O&#771;': chr(213), # O tilde
                   'O&#772;': '&#332;', # O macron
                   'O&#774;': '&#334;', # O breve
                   'O&#775;': '&#558;', # O dot above
                   'O&#776;': chr(214), # O diaresis/umlaut
                   'O&#779;': '&#336;', # O double acute
                   'O&#780;': '&#465;', # O caron
                   'O&#783;': '&#524;', # O double grave
                   'O&#785;': '&#526;', # O inverted breve
                   'O&#808;': '&#490;', # O ogonek
                   'R&#769;': '&#340;', # R acute accent
                   'R&#780;': '&#344;', # R caron
                   'R&#783;': '&#528;', # R double grave
                   'R&#785;': '&#530;', # R inverted breve
                   'R&#807;': '&#342;', # R cedilla
                   'S&#769;': '&#346;', # S acute accent
                   'S&#770;': '&#348;', # S cirmuflex accent
                   'S&#780;': '&#352;', # S caron
                   'S&#806;': '&#536;', # S comma below
                   'S&#807;': '&#350;', # S cedilla
                   'T&#780;': '&#356;', # T caron
                   'T&#806;': '&#538;', # T comma below
                   'T&#807;': '&#354;', # T cedilla
                   'U&#768;': chr(217), # U grave accent
                   'U&#769;': chr(218), # U acute accent
                   'U&#770;': chr(219), # U cirmuflex accent
                   'U&#771;': '&#360;', # U tilde
                   'U&#772;': '&#362;', # U macron
                   'U&#774;': '&#364;', # U breve
                   'U&#776;': chr(220), # U diaresis/umlaut
                   'U&#778;': '&#366;', # U ring above
                   'U&#779;': '&#368;', # U double acute
                   'U&#780;': '&#467;', # U caron
                   'U&#783;': '&#532;', # U double grave
                   'U&#785;': '&#534;', # U inverted breve
                   'U&#808;': '&#370;', # U ogonek
                   'W&#770;': '&#372;', # W cirmuflex accent
                   'Y&#769;': chr(221), # Y acute accent
                   'Y&#770;': '&#374;', # Y cirmuflex accent
                   'Y&#776;': '&#376;', # Y diaresis/umlaut
                   'Y&#772;': '&#562;', # Y macron
                   'Z&#769;': '&#377;', # Z acute accent
                   'Z&#775;': '&#379;', # Z dot above
                   'Z&#780;': '&#381;', # Z caron
                   'a&#768;': chr(224), # a grave accent
                   'a&#769;': chr(225), # a acute accent
                   'a&#770;': chr(226), # a cirmuflex accent
                   'a&#771;': chr(227), # a tilde
                   'a&#772;': '&#257;', # a macron
                   'a&#774;': '&#259;', # a breve
                   'a&#775;': '&#551;', # a dot above
                   'a&#776;': chr(228), # a diaresis/umlaut
                   'a&#778;': chr(229), # a ring above
                   'a&#780;': '&#462;', # a caron
                   'a&#783;': '&#513;', # a double grave
                   'a&#785;': '&#515;', # a inverted breve
                   'a&#808;': '&#261;', # a ogonek
                   'c&#769;': '&#263;', # c acute accent
                   'c&#770;': '&#265;', # c cirmuflex accent
                   'c&#775;': '&#267;', # c dot above
                   'c&#780;': '&#269;', # c caron
                   'c&#807;': chr(231), # c cedilla
                   'd&#780;': '&#271;', # d caron (displayed as an apostrophe)
                   'e&#768;': chr(232), # e grave accent
                   'e&#769;': chr(233), # e acute accent
                   'e&#770;': chr(234), # e cirmuflex accent
                   'e&#772;': '&#275;', # e macron
                   'e&#774;': '&#277;', # e breve
                   'e&#775;': '&#279;', # e dot above
                   'e&#776;': chr(235), # e diaresis/umlaut
                   'e&#780;': '&#283;', # e caron
                   'e&#783;': '&#517;', # e double grave
                   'e&#785;': '&#519;', # e inverted breve
                   'e&#807;': '&#553;', # e cedilla
                   'e&#808;': '&#281;', # e ogonek
                   'g&#769;': '&#501;', # g acute accent
                   'g&#770;': '&#285;', # g cirmuflex accent
                   'g&#774;': '&#287;', # g breve
                   'g&#775;': '&#289;', # g dot above
                   'g&#780;': '&#487;', # g caron
                   'g&#807;': '&#291;', # g cedilla
                   'h&#770;': '&#293;', # h cirmuflex accent
                   'h&#780;': '&#543;', # h caron
                   'i&#768;': chr(236), # i grave accent
                   'i&#769;': chr(237), # i acute accent
                   'i&#770;': chr(238), # i cirmuflex accent
                   'i&#771;': '&#297;', # i tilde
                   'i&#772;': '&#299;', # i macron
                   'i&#774;': '&#301;', # i breve
                   'i&#776;': chr(239), # i diaresis/umlaut
                   'i&#780;': '&#464;', # i caron
                   'i&#783;': '&#521;', # i double grave
                   'i&#785;': '&#523;', # i inverted breve
                   'i&#808;': '&#303;', # i ogonek
                   'j&#770;': '&#309;', # j cirmuflex accent
                   'j&#780;': '&#496;', # j caron
                   'k&#780;': '&#489;', # k caron
                   'k&#807;': '&#311;', # k cedilla
                   'l&#769;': '&#314;', # l acute accent
                   'l&#780;': '&#318;', # L caron
                   'l&#807;': '&#316;', # l cedilla
                   'n&#768;': '&#505;', # n grave accent
                   'n&#769;': '&#324;', # n acute accent
                   'n&#771;': chr(241), # n tilde
                   'n&#775;': '&#7749;', # n dot above
                   'n&#780;': '&#328;', # n caron
                   'n&#807;': '&#326;', # n cedilla
                   'o&#768;': chr(242), # o grave accent
                   'o&#769;': chr(243), # o acute accent
                   'o&#770;': chr(244), # o cirmuflex accent
                   'o&#771;': chr(245), # o tilde
                   'o&#772;': '&#333;', # o macron
                   'o&#774;': '&#335;', # o breve
                   'o&#775;': '&#559;', # o dot above
                   'o&#776;': chr(246), # o diaresis/umlaut
                   'o&#779;': '&#337;', # o double acute
                   'o&#780;': '&#466;', # o caron
                   'o&#783;': '&#525;', # o double grave
                   'o&#785;': '&#527;', # o inverted breve
                   'o&#808;': '&#491;', # o ogonek
                   'r&#769;': '&#341;', # r acute accent
                   'r&#780;': '&#345;', # r caron
                   'r&#783;': '&#529;', # r double grave
                   'r&#785;': '&#531;', # r inverted breve
                   'r&#807;': '&#343;', # r cedilla
                   's&#769;': '&#347;', # s acute accent
                   's&#770;': '&#349;', # s cirmuflex accent
                   's&#780;': '&#353;', # s caron
                   's&#806;': '&#537;', # s comma below
                   's&#807;': '&#351;', # s cedilla
                   't&#780;': '&#357;', # t caron
                   't&#806;': '&#539;', # t comma below
                   't&#807;': '&#355;', # t cedilla
                   'u&#768;': chr(249), # u grave accent
                   'u&#769;': chr(250), # u acute accent
                   'u&#770;': chr(251), # u cirmuflex accent
                   'u&#771;': '&#361;', # u tilde
                   'u&#772;': '&#363;', # u macron
                   'u&#774;': '&#365;', # u breve
                   'u&#776;': chr(252), # u diaresis/umlaut
                   'u&#778;': '&#367;', # u ring above
                   'u&#779;': '&#369;', # u double acute
                   'u&#780;': '&#468;', # u caron
                   'u&#783;': '&#533;', # u double grave
                   'u&#785;': '&#535;', # u inverted breve
                   'u&#808;': '&#371;', # u ogonek
                   'w&#770;': '&#373;', # w cirmuflex accent
                   'y&#769;': chr(253), # y acute accent
                   'y&#770;': '&#375;', # y cirmuflex accent
                   'y&#772;': '&#563;', # y macron
                   'y&#776;': chr(255), # y diaresis/umlaut
                   'z&#769;': '&#378;', # z acute accent
                   'z&#775;': '&#380;', # z dot above
                   'z&#780;': '&#382;'  # z caron
                   }
        return replace

_VALID_FIELD_NAME = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)?$')

def ISFDBBadUnicodePatternMatch(field_name):
        if not _VALID_FIELD_NAME.match(field_name):
                raise ValueError('Invalid field name: %s' % field_name)
        unicode_map = ISFDBUnicodeTranslation()
        # Assumes unicode_map will have at least one entry
        pattern_match = ''
        for key in unicode_map:
                if pattern_match:
                        pattern_match += ' or '
                pattern_match += "%s like binary '%%%s%%'" % (field_name, key)
        return pattern_match

def suspectUnicodePatternMatch(field_name):
        if not _VALID_FIELD_NAME.match(field_name):
                raise ValueError('Invalid field name: %s' % field_name)
        unicode_map = ('&#699;', '&#700;')
        pattern_match = ''
        for key in unicode_map:
                if pattern_match:
                        pattern_match += ' or '
                pattern_match += "%s like '%%%s%%'" % (field_name, key)
        return pattern_match

def dict_to_in_clause(id_dict_1, id_dict_2 = None):
        # Convert the keys of up to 2 dictionaries to a SQL 'IN' clause
        id_list = []
        for record_id in id_dict_1:
                id_list.append(record_id)
        if id_dict_2:
                for record_id in id_dict_2:
                        id_list.append(record_id)
        in_clause = list_to_in_clause(id_list)
        return in_clause

def list_to_in_clause(id_list):
        in_clause = ''
        for id_value in id_list:
                id_string = str(id_value)
                if not in_clause:
                        in_clause = "'%s'" % id_string
                else:
                        in_clause += ",'%s'" % id_string
        return in_clause

def ISFDBMouseover(mouseover_values, display_value, tag = 'td', indicator = SESSION.ui.question_mark,
                   position = 'right', html_escape = True, note = 0):
        if html_escape:
                display_value = ISFDBText(display_value)
        # Adds a mouseover bubble with the specified list of values to
        # the displayed text/link and returns the composite string.
        # Supports different opening and closing HTML tags, typically <td>.
        if not mouseover_values:
                if tag == 'td':
                        return '<td>%s</td>' % display_value
                else:
                        return display_value
        if tag:
                display = '<%s>' % tag
        else:
                display = ''
        if indicator == SESSION.ui.question_mark:
                tooltipwidth = 'tooltipnarrow'
        else:
                tooltipwidth = 'tooltipwide'
        tooltipclass = 'tooltip'
        tooltiptextclass = 'tooltiptext'
        if position == 'right':
                tooltipposition = 'tooltipright'
        else:
                tooltipposition = 'tooltipleft'
        display += '<div class="%s %s">' % (tooltipclass, tooltipposition)
        display += '%s<sup class="mouseover">%s</sup>' % (display_value, indicator)
        display += '<span class="%s %s %s">' % (tooltiptextclass, tooltipwidth, tooltipposition)
        count = 0
        for mouseover_value in mouseover_values:
                if count:
                        display += '<br>'
                # Do not HTML-escape notes which can contain HTML
                if note:
                        display += mouseover_value
                else:
                        display += ISFDBText(mouseover_value)
                count += 1
        display += '</span></div>'
        if tag:
                display += '</%s>'% tag
        return display

def invalidURL(url):
        if PYTHONVER == 'python2':
                from urlparse import urlparse
        else:
                from urllib.parse import urlparse
        error = invalidURLcharacters(url, 'URL', 'escaped')
        if error:
                return error
        parsed_url = urlparse(url)
        if parsed_url[0] not in ('http', 'https'):
                return '%s URLs must start with http or https' % error
        if not parsed_url[1]:
                return '%s Domain name not specified' % error
        return ''

def invalidURLcharacters(url, field_name, escaped_flag):
        invalid_characters = ['<', '>', '"']
        if escaped_flag == 'escaped':
                final_invalid_chars = []
                for invalid_character in invalid_characters:
                        final_invalid_chars.append(XMLescape(invalid_character))
        elif escaped_flag == 'unescaped':
                final_invalid_chars = invalid_characters
        else:
                return 'Software issue - contact the site administrator'
        # Append space which has to be added after XMLescape; otherwise it would be stripped as a trailing space
        final_invalid_chars.append(' ')
        for invalid_char in final_invalid_chars:
                if invalid_char in url:
                        if invalid_char == ' ':
                                display_char = 'Spaces'
                        else:
                                display_char = invalid_char
                        return 'Invalid %s. %s not allowed in %ss' % (field_name, display_char, field_name)
        return ''

def WikiExists():
        query = """select count(*) from information_schema.tables
                where table_schema = 'isfdb' and table_name = 'mw_page'"""
        CNX = MYSQL_CONNECTOR()
        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHONE()
        if record[0][0]:
                return 1
        else:
                return 0

def WikiLink(user_name):
        return '<a href="%s://%s/index.php/User_Talk:%s">%s</a>' % (PROTOCOL, WIKILOC, Portable_urllib_quote(user_name), ISFDBText(user_name))

def ISFDBWikiTemplate(template):
        return '%s://%s/index.php?title=Template:%s' % (PROTOCOL, WIKILOC, template)

def ISFDBWikiPage(page):
        return '%s://%s/index.php/%s' % (PROTOCOL, WIKILOC, page)

def popularNonLatinLanguages(types):
        # Each language is associated with a tuple of report IDs.
        # The numbers in the tuple are the report ID of the
        # title-specific, publication-specific, author-specific and series-specific
        # cleanup reports respectively.
        languages = {
                   'Bulgarian': (138, 162, 183, 258),
                   'Chinese': (139, 163, 184, 259),
                   'Greek': (140, 164, 185, 260),
                   'Japanese': (141, 165, 186, 261),
                   'Russian': (142, 166, 187, 262)
                   }
        if types == 'titles':
                position = 0
        elif types == 'pubs':
                position = 1
        elif types == 'authors':
                position = 2
        elif types == 'series':
                position = 3
        else:
                raise ValueError('Unknown type: %s' % types)
        results = []
        for language in languages:
                report_ids = languages[language]
                report_id = report_ids[position]
                results.append((language, report_id))
        return results

def transliteratedReports(types):
        # Each language is associated with a tuple of report IDs.
        # The first number in the tuple is the report ID of the
        # title-specific cleanup report. The second number is the
        # report ID of the publication-specific cleanup report.
        # The third number is the report ID of the author-specific
        # cleanup report.
        languages = {
                   'Bulgarian': (124, 148, 169),
                   'Chinese': (125, 149, 170),
                   'Czech': (126, 150, 171),
                   'English': (127, 151, 172),
                   'Greek': (128, 152, 173),
                   'Hungarian': (129, 153, 174),
                   'Japanese': (130, 154, 175),
                   'Lithuanian': (131, 155, 176),
                   'Polish': (132, 156, 177),
                   'Romanian': (133, 157, 178),
                   'Russian': (134, 158, 179),
                   'Serbian': (135, 159, 180),
                   'Turkish': (136, 160, 181)
                   }
        if types == 'titles':
                position = 0
        elif types == 'pubs':
                position = 1
        elif types == 'authors':
                position = 2
        else:
                raise ValueError('Unknown type: %s' % types)
        results = []
        for language in languages:
                report_ids = languages[language]
                report_id = report_ids[position]
                results.append((language, report_id))
        return results

def ISFDBtranslatedReports():
        reports = {
                264: 17,
                265: 36,
                266: 22,
                267: 26,
                268: 16,
                269: 53,
                270: 59,
                271: 37
                }
        return reports

def ISFDBprintTime():
        print('<p><b>Current ISFDB time:</b> %s' % str(datetime.now()).split('.')[0])

def ISFDBdaysFromToday(future_date):
        if future_date == '8888-00-00' or future_date == '0000-00-00':
                return 0

        # Here's the old code:
        #
        #   today_date = datetime.today()
        #   normalized_future_date = datetime.strptime(future_date, "%Y-%m-%d")
        #
        # Problem is that this is always 1 day off. The future_date is a string in
        # YYYY-MM-DD format. The strptime call converts it to datetime format, but with
        # HH:MM:SS zeroed out: 2026-01-05 00:00:00
        #
        # But today_date has a full timestamp, for instance: 2026-01-04 16:00:00
        # When days_from_today is calculated, with the times above, the delta between
        # the dates is 8 hours, which is less than 24 hours, which returns a difference
        # of zero days. There is actually no time today which would result in 
        # tomorrow's date generating a delta of 1 day. Hence it always returned a
        # value that was one day off.

        # Get today's date in YYYY-MM-DD format (as a string)
        full_date = datetime.now()
        current_date = str(full_date.date())
        try:
                # Convert both today and future_date into datetimes
                today_date = datetime.strptime(current_date, "%Y-%m-%d")
                normalized_future_date = datetime.strptime(future_date, "%Y-%m-%d")
        except ValueError:
                return 0 # Invalid date format
        days_from_today = normalized_future_date - today_date
        return days_from_today.days

def ISFDBprintSubmissionTable(CNX, status):
        from login import GetUserData
        ISFDBprintTime()
        print('<table class="generic_table">')
        print('<tr align="left" class="generic_table_header">')
        print('<th>Submission</th>')
        print('<th>Type</th>')
        print('<th>Time Submitted</th>')
        print('<th>Submitter</th>')

        if status == 'I':
                print('<th>Time Approved</th>')
        if status == 'R':
                print('<th>Time Rejected</th>')

        if status == 'N':
                print('<th>Holder</th>')
        else:
                print('<th>Reviewer</th>')

        print('<th>Affected Record</th>')

        if status == 'R':
                print('<th>Reason</th>')
        elif status == 'N':
                print('<th>Cancel</th>')

        unreject = 0
        (userid, username, usertoken) = GetUserData()
        if status == 'R' and SQLisUserModerator(userid):
                unreject = 1
                print('<th>Unreject?</th>')

        print('</tr>')
        record = CNX.DB_FETCHMANY()
        color = 0
        while record:
                ISFDBprintSubmissionRecord(record, color, status, unreject)
                color = color ^ 1
                record = CNX.DB_FETCHMANY()
        print('</table>')

def ISFDBprintSubmissionRecord(record, eccolor, status, unreject):
        if eccolor:
                print('<tr align=left class="table1">')
        else:
                print('<tr align=left class="table2">')

        subType=record[0][SUB_TYPE]
        subTypeName=SUBMAP[subType][1]
        subId=record[0][SUB_ID]

        print('<td><a href="%s:/%s/view_submission.cgi?%s">%s</a></td>' % (PROTOCOL, HTFAKE, subId, subId))

        displayName = 'Unable to determine'
        try:
                doc = minidom.parseString(XMLunescape2(record[0][SUB_DATA]))
                doc2 = doc.getElementsByTagName(subTypeName)
                displayName = ISFDBSubmissionType(subTypeName, subType, doc2)
                (subjectLink, new_record) = getSubjectLink(record[0], doc2, subType)
                submitter = GetElementValue(doc2, 'Submitter')
                submitter = str.replace(submitter, ' ', '_')
        except Exception as e:
                e = traceback.format_exc()
                subjectLink = '<b>XML PARSE ERROR: %s</b>' % e
                submitter = SQLgetUserName(record[0][SUB_SUBMITTER])

        print('<td>%s</td>' % displayName)

        print('<td>%s</td>' % record[0][SUB_TIME])

        print('<td>%s</td>' % WikiLink(submitter))

        if status in ('I', 'R'):
                if record[0][SUB_REVIEWED]:
                        print('<td>%s</td>' % record[0][SUB_REVIEWED])
                else:
                        print('<td>&nbsp;</td>')

        if status == 'N':
                if record[0][SUB_HOLDID]:
                        holder = SQLgetUserName(record[0][SUB_HOLDID])
                        print('<td>%s</td>' % WikiLink(holder))
                else:
                        print('<td>&nbsp;</td>')
        else:
                if record[0][SUB_REVIEWER]:
                        approver = SQLgetUserName(record[0][SUB_REVIEWER])
                        print('<td>%s</td>' % WikiLink(approver))
                else:
                        print('<td>&nbsp;</td>')

        print('<td><i>%s</i></td>' % subjectLink)

        if status == 'R':
                if record[0][SUB_REASON]:
                        print('<td>%s</td>' % ISFDBText(record[0][SUB_REASON]))
                else:
                        print('<td>&nbsp;</td>')
        elif status == 'N':
                print('<td><a href="%s:/%s/cancelsubmission.cgi?%d">Cancel submission</a></td>' % (PROTOCOL, HTFAKE, subId))

        if unreject:
                print('<td>%s</td>' % ISFDBLink('mod/unreject.cgi', subId, 'Unreject'))
        print('</tr>')

def ISFDBSubmissionDoc(sub_data, xml_tag):
        try:
                doc = minidom.parseString(XMLunescape2(sub_data))
        except Exception:
                SESSION.DisplayError('Submission contains invalid XML and cannot be displayed')
                return None
        doc2 = doc.getElementsByTagName(xml_tag)
        return doc2

def ISFDBSubmissionDisplayType(display_tag, xml_tag, sub_type):
        # If the "corrected" display type is not the same as the XML tag, then display the former
        if display_tag != xml_tag:
                displayType = display_tag
        # Otherwise display the full type name stored in SUBMAP
        else:
                displayType = SUBMAP[sub_type][3]
        return displayType

def getSubjectLink(record, doc2, subType):
        subject = GetElementValue(doc2, 'Subject')
        new_record = 0
        if record[SUB_NEW_RECORD_ID]:
                recordNum = record[SUB_NEW_RECORD_ID]
                if record[SUB_TYPE] in (MOD_PUB_NEW, MOD_PUB_CLONE, MOD_VARIANT_TITLE,
                                        MOD_AWARD_NEW, MOD_AWARD_TYPE_NEW, MOD_AWARD_CAT_NEW,
                                        MOD_LANGUAGE_NEW, MOD_TEMPLATE_ADD, MOD_VER_SOURCE_ADD):
                        new_record = 1
        else:
                recordNum = GetElementValue(doc2, SUBMAP[subType][4])
                # Since 'NewPub' is used for "New Pub", "Add Pub to Title", "Import Contents", "Export Contents"
                # and "Clone Pub", we need to check the sub-tags inside the XML to determine the record number
                if subType in (MOD_TITLE_MERGE, MOD_PUBLISHER_MERGE, MOD_AUTHOR_MERGE):
                        recordNum = GetElementValue(doc2, 'KeepId')
                elif subType == MOD_VARIANT_TITLE:
                        recordNum = GetElementValue(doc2, 'Parent')
                elif subType == MOD_PUB_CLONE:
                        recordNum = GetElementValue(doc2, 'ClonedTo')
        subjectLink=subject[:40]
        # This value is None for data deletion submissions since there is no record left to link to
        displayPage = SUBMAP[subType][2]
        if recordNum and displayPage:
                subjectLink='<a href="%s:/%s/%s?%s">%s</a>' % (PROTOCOL, HTFAKE, displayPage, recordNum, subjectLink)
        return (subjectLink, new_record)

def AdvSearchLink(params):
        link = '<a href="%s:/%s/adv_search_results.cgi?START=0%s">' % (PROTOCOL, HTFAKE, EscapeParams(params))
        return link

def EscapeParams(params):
        param_string = ''
        if PYTHONVER == "python2":
                import urllib
                for param in params:
                        param_string += '&amp;%s=%s' % (urllib.quote(param[0]), urllib.quote(param[1]))
        elif PYTHONVER == "python3":
                import urllib.request, urllib.parse, urllib.error
                for param in params:
                        param_string += '&amp;%s=%s' % (urllib.parse.quote(param[0]), urllib.parse.quote(param[1]))
        return param_string

def printRecordID(record_type, record_id, user_id, user = None, edit_mode = 1):
        print(buildRecordID(record_type, record_id, user_id, user, edit_mode))

def buildRecordID(record_type, record_id, user_id, user = None, edit_mode = 1):
        from login import User
        output = '<span class="recordID"><b>%s Record # </b>%d' % (record_type, int(record_id))
        if user_id:
                cgi_scripts = {'Publication': ('editpub', 'pub_history'),
                               'Title': ('edittitle', 'title_history'),
                               'Author': ('editauth', 'author_history'),
                               'Series': ('editseries', 'series_history'),
                               'Publisher': ('editpublisher', 'publisher_history'),
                               'Pub. Series': ('editpubseries', 'pubseries_history'),
                               'Award': ('editaward', 'award_history'),
                               'Award Category': ('editawardcat', 'award_category_history'),
                               'Award Type': ('editawardtype', 'awardtype_history')
                               }
                if record_type in cgi_scripts:
                        if not user:
                                user = User()
                                user.load()
                        user.load_moderator_flag()
                        cgi_script = cgi_scripts[record_type][0]
                        if record_type in ('Award Category', 'Award Type') and not user.moderator:
                                edit_mode = 0
                        if edit_mode:
                                output += ' [<a href="%s:/%s/edit/%s.cgi?%d">Edit</a>]' % (PROTOCOL, HTFAKE, cgi_script, int(record_id))
                                history_script = cgi_scripts[record_type][1]
                                # Only moderators can view Author Edit History at this time
                                if record_type == 'Author' and not user.moderator:
                                        pass
                                else:
                                        output += ' [<a href="%s:/%s/%s.cgi?%d">Edit History</a>]' % (PROTOCOL, HTFAKE, history_script, int(record_id))
        output += '</span>'
        return output

class isfdbUI:
        def __init__(self):
                self.required_paired_tags = ['b', 'blockquote', 'center', 'cite', 'del', 'em', 'i', 'ol', 'pre',
                                    's', 'strong', 'sub', 'sup', 'table', 'td', 'th', 'tr', 'u', 'ul']
                self.optional_paired_tags = ['li', 'p']
                self.paired_tags = self.required_paired_tags + self.optional_paired_tags
                self.self_closing_tags = ['p', 'br', '!--isfdb specific--']
                self.tags_with_attributes = ['a', 'table', 'td']

                self.valid_tags = []
                for tag in self.paired_tags:
                        self.valid_tags.append('<%s>' % tag)
                        self.valid_tags.append('</%s>' % tag)
                for tag in self.self_closing_tags:
                        self.valid_tags.append('<%s>' % tag)
                        self.valid_tags.append('<%s/>' % tag)
                        self.valid_tags.append('<%s />' % tag)
                for tag in self.tags_with_attributes:
                        self.valid_tags.append('<%s ' % tag)
                        self.valid_tags.append('</%s>' % tag)

        def goodHtmlClause(self, table_name, field_name):
                clause = '('
                for tag in self.valid_tags:
                        clause += "%s.%s like '%%%s%%' or " % (table_name, field_name, tag)
                clause = clause[:-4] + ")"
                return clause

        def goodHtmlTagsPresent(self, value):
                for tag in self.valid_tags:
                        if tag in value.lower():
                                return 1
                return 0

        def badHtmlClause(self, table_name, field_name):
                clause = '(('
                for tag in self.valid_tags:
                        clause += "replace("
                clause += "lower(%s)," % field_name
                for tag in self.valid_tags:
                        clause += "'%s','')," % tag
                clause = clause[:-1] + " like '%<%')"
                clause += " or (%s.%s like '%%<a href%%' and %s.%s not like '%%<a href=%%')" % (table_name, field_name, table_name, field_name)
                clause += """ or (%s.%s like '%%<li>%%'
                                and %s.%s not like '%%<ul>%%'
                                and %s.%s not like '%%<ol>%%'))
                                """ % (table_name, field_name, table_name, field_name, table_name, field_name)
                return clause

        def badHtmlTagsPresent(self, value):
                value = value.lower()
                for tag in self.valid_tags:
                        value = value.replace(tag,'')
                if '<' in value:
                        return 1

        def invalidHtmlListPresent(self, value):
                value = value.lower()
                if '<li>' in value and '<ul>' not in value and '<ol>' not in value:
                        return 1

        def mismatchedHtmlTagsPresent(self, value):
                value = value.lower()
                for tag in self.required_paired_tags:
                        open_tag = '<%s>' % tag
                        close_tag = '</%s>' % tag
                        if value.count(open_tag) != value.count(close_tag):
                                return 1
                return 0

        def invalidHtmlInNotes(self, value):
                if self.badHtmlTagsPresent(value):
                        return 'Unrecognized HTML tag(s) present'
                elif self.invalidHtmlListPresent(value):
                        return 'HTML tags: li without ul or ol'
                elif self.mismatchedHtmlTagsPresent(value):
                        return 'Mismatched HTML tags'
                return ''

        def mismatchedBraces(self, value):
                if value.count('{') != value.count('}'):
                        return 'Mismatched braces'
                return ''

        def mismatchedDoubleQuote(self, value):
                if value.count('"') % 2 != 0:
                        return 'Mismatched double quotes'
                return ''

        def unrecognizedTemplate(self, value):
                new_value = value.lower()
                templates = list(SQLLoadAllTemplates().keys())
                templates.append('break')
                for template in templates:
                        non_linking_template = '{{%s}}' % template.lower()
                        new_value = new_value.replace(non_linking_template, '')
                        linking_template = '{{%s|' % template.lower()
                        new_value = new_value.replace(linking_template, '')
                if '{{' in new_value:
                        return 'Unrecognized template'
                return ''

def FormatExternalIDType(type_name, types):
        formatted_type = ''
        for type_number in types:
                if types[type_number][0] == type_name:
                        type_full_name = types[type_number][1]
                        formatted_type = '<abbr class="template" title="%s">%s</abbr>:' % (type_full_name, type_name)
                        break
        return formatted_type

def FormatExternalIDSite(sites, type_id, id_value):
        site_count = 0
        for site in sites:
                if site[IDSITE_TYPE_ID] == type_id:
                        site_count += 1
                        url = site[IDSITE_URL]
        if site_count == 0:
                formatted_id = id_value
        elif site_count == 1:
                formatted_id = ' %s' % FormatExternalIDLink(url, id_value, id_value)
        else:
                formatted_id = ' %s' % id_value
                for site in sites:
                        if site[IDSITE_TYPE_ID] == type_id:
                                formatted_id += ' %s' % FormatExternalIDLink(site[IDSITE_URL], id_value, site[IDSITE_NAME])
                if '.amazon.' in url:
                        formatted_id += ' (US/UK earn commissions)'
        return formatted_id

def FormatExternalIDLink(url, value, display_value):
        return '<a href="%s" target="_blank">%s</a>' % (url % str.replace(str(value),' ',''), display_value)

def LIBsameParentAuthors(title):
        pseudonym = 0
        if title[TITLE_PARENT]:
                parentauthors = SQLTitleAuthors(title[TITLE_PARENT])
                pseudonymauthors = SQLTitleAuthors(title[TITLE_PUBID])
                if set(parentauthors) != set(pseudonymauthors):
                        pseudonym = 1
        return pseudonym

def LIBbuildRecordList(record_type, records):
        output = ''
        first = 1
        for record in records:
                if record_type == 'author':
                        record_id = record[AUTHOR_ID]
                        record_name = record[AUTHOR_CANONICAL]
                        cgi_script = 'ea.cgi'
                elif record_type == 'series':
                        record_id = record[SERIES_PUBID]
                        record_name = record[SERIES_NAME]
                        cgi_script = 'pe.cgi'
                elif record_type == 'pub_series':
                        record_id = record[PUB_SERIES_ID]
                        record_name = record[PUB_SERIES_NAME]
                        cgi_script = 'pubseries.cgi'
                elif record_type == 'publisher':
                        record_id = record[PUBLISHER_ID]
                        record_name = record[PUBLISHER_NAME]
                        cgi_script = 'publisher.cgi'
                if not first:
                        output += ', '
                else:
                        first = 0
                output += ISFDBLink(cgi_script, record_id, record_name, False, '')
        return output

def ISFDBPossibleDuplicates(title):
        title_authors = SQLTitleBriefAuthorRecords(title[TITLE_PUBID])
        possible_duplicates = []
        # Retrieve a list of title records whose titles are the same as the passed-in title's
        targets = SQLFindExactTitles(title[TITLE_TITLE])
        for target in targets:
                # Skip the title record whose title ID is the same as the passed in title's
                if target[TITLE_PUBID] == title[TITLE_PUBID]:
                        continue
                if ISFDBCompareTwoTitles(title, target, 0):
                        target_authors = SQLTitleBriefAuthorRecords(target[TITLE_PUBID])
                        # Only titles with identical authors are potential duplicates
                        if set(title_authors) == set(target_authors):
                                possible_duplicates.append((target,target_authors))
        return possible_duplicates

def ISFDBCompareTwoTitles(title, target, mode):
        match = 0
        title_type = title[TITLE_TTYPE]
        target_type = target[TITLE_TTYPE]
        # Define a list of title types that are "containers", i.e. can contain other titles
        containers = ("COLLECTION", "ANTHOLOGY", "OMNIBUS", "CHAPBOOK", "NONFICTION")
        # Define a list of title types that can be contained in containers
        contained = ("SHORTFICTION", "ESSAY", "POEM", "SERIAL")
        # If one title is a container and the other one is a "contained" title, they are not duplicates
        if title_type in contained and target_type in containers:
                pass
        elif title_type in containers and target_type in contained:
                pass
        # Exclude all REVIEW titles
        elif title_type == "REVIEW" or target_type == "REVIEW":
                pass
        # COVERART, INTERIORART and INTERVIEW titles should only be compared to other titles of the same type
        elif title_type == "COVERART" and target_type != "COVERART":
                pass
        elif title_type != "COVERART" and target_type == "COVERART":
                pass
        elif title_type == "INTERIORART" and target_type != "INTERIORART":
                pass
        elif title_type != "INTERIORART" and target_type == "INTERIORART":
                pass
        elif title_type == "INTERVIEW" and target_type != "INTERVIEW":
                pass
        elif title_type != "INTERVIEW" and target_type == "INTERVIEW":
                pass
        # If one of the titles is a variant of the other, they are not duplicates
        elif title[TITLE_PARENT] == target[TITLE_PUBID]:
                pass
        elif target[TITLE_PARENT] == title[TITLE_PUBID]:
                pass
        # For Exact Mode, SHORTFICTION/NOVEL, SHORTFICTION, COLLECTION/CHAPBOOK,
        # NOVEL/COLLECTION, NOVEL/OMNIBUS and NOVEL/POEM pairs are not considered potential duplicates
        elif mode == 0 and ((title_type == "SHORTFICTION" and target_type == "NOVEL") or (title_type == "NOVEL" and target_type == "SHORTFICTION")):
                pass
        elif mode == 0 and ((title_type == "COLLECTION" and target_type == "CHAPBOOK") or (title_type == "CHAPBOOK" and target_type == "COLLECTION")):
                pass
        elif mode == 0 and ((title_type == "COLLECTION" and target_type == "NOVEL") or (title_type == "NOVEL" and target_type == "COLLECTION")):
                pass
        elif mode == 0 and ((title_type == "OMNIBUS" and target_type == "NOVEL") or (title_type == "NOVEL" and target_type == "OMNIBUS")):
                pass
        elif mode == 0 and ((title_type == "POEM" and target_type == "NOVEL") or (title_type == "NOVEL" and target_type == "POEM")):
                pass
        # If the two titles have different language codes, they are not duplicates
        elif title[TITLE_LANGUAGE] and target[TITLE_LANGUAGE] and (title[TITLE_LANGUAGE] != target[TITLE_LANGUAGE]):
                pass
        elif mode == 2:
                if _similarTitles(title[TITLE_TITLE], target[TITLE_TITLE]):
                        match = 1
        else:
                match = 1

        return match

def _similarTitles(string1, string2):
        newstr1 = string1.lower()
        newstr1 = newstr1.replace(' ', '')
        newstr2 = string2.lower()
        newstr2 = newstr2.replace(' ', '')
        if newstr1 == newstr2:
                return 1

        if len(newstr1) > len(newstr2):
                maxlen = len(newstr2)
        else:
                maxlen = len(newstr1)

        counter = 0
        total = 0
        while counter < maxlen:
                if newstr1[counter] == newstr2[counter]:
                        total += 1
                counter += 1

        counter = 0
        while counter < maxlen:
                if newstr1[(len(newstr1)-1)-counter] == newstr2[(len(newstr2)-1)-counter]:
                        total += 1
                counter += 1

        if len(newstr1) > len(newstr2):
                #ratio = float(total)/float(len(newstr1))
                ratio = float(total)/float(len(newstr2))
        else:
                #ratio = float(total)/float(len(newstr2))
                ratio = float(total)/float(len(newstr1))

        #print '<br>RATIO:', newstr1, newstr2, ratio
        if ratio > 0.85:
                return 1
        else:
                return 0

def debugUnicodeString(input, filename):
        f = open(filename, "w")
        f.write(input)
        f.close()

if PYTHONVER == 'python2':
        import urllib
        import urllib2
        from urlparse import urlparse
else:
        import urllib.parse
        import urllib.request
        from urllib.parse import urlparse

def Portable_urllib_quote(target):
        if PYTHONVER == 'python2':
                retval = urllib.quote(target)
        else:
                retval = urllib.parse.quote(target)
        return(retval)

def Portable_urllib_unquote(target):
        if PYTHONVER == 'python2':
                retval = urllib.unquote(target)
        else:
                retval = urllib.parse.unquote(target)
        return(retval)

def IsfdbFieldStorage():
        if PYTHONVER == 'python2':
                form = cgi.FieldStorage()
        else:
                form = cgi.FieldStorage(encoding="iso-8859-1")
        return form
