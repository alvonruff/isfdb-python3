#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2007-2025   Al von Ruff, Ahasuerus and Bill Longley
#         ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1166 $
#     Date: $Date: 2024-02-08 14:50:44 -0500 (Thu, 08 Feb 2024) $


import string
from isfdb import *
from isfdblib import *
from library import ISFDBCompareTwoTitles


def CheckOneList(titles, mode):
        counter = 0
        found = 0
        for title in titles:
                first = 1
                delete_list = []
                offset = counter+1
                for target in titles[counter+1:]:
                        match = ISFDBCompareTwoTitles(title, target, mode)
                        if match:
                                title_authors = SQLTitleBriefAuthorRecords(title[TITLE_PUBID])
                                target_authors = SQLTitleBriefAuthorRecords(target[TITLE_PUBID])
                                # Only titles with identical authors are potential duplicates
                                if set(title_authors) == set(target_authors):
                                        found = 1
                                        if first:
                                                print('<form METHOD="POST" ACTION="/cgi-bin/edit/tv_merge.cgi">')
                                                PrintDuplicateTableColumns()
                                                PrintDuplicateTitleRecord(title, 0, title_authors)
                                                first = 0
                                        PrintDuplicateTitleRecord(target, 0, target_authors)
                                        delete_list.append(offset)
                        offset += 1

                fudge = 0
                for item in delete_list:
                        del titles[item-fudge]
                        fudge += 1
                counter += 1

                if first == 0:
                        print('</table>')
                        print('<p>')
                        print('<input TYPE="SUBMIT" VALUE="Merge Selected Records">')
                        print('</form>')
                        print('<p>')
        return found

        
if __name__ == '__main__':

        author_id = SESSION.Parameter(0, 'int')
        author_data = SQLloadAuthorData(author_id)
        titles = SQLloadAnyTitles(author_id)
        if not titles:
                SESSION.DisplayError('Record Does Not Exist')

        mode = SESSION.Parameter(1, 'int', 0, (0, 1, 2))

        if (mode == 2) and (len(titles) > 1000):
                SESSION.DisplayError('Aggressive mode disabled for authors with more than 1,000 titles for performance reasons')

        PrintPreSearch('Duplicate Finder for %s' % author_data[AUTHOR_CANONICAL])
        PrintNavBar('edit/find_dups.cgi', author_id)

        print('<div id="HelpBox">')
        print('<b>Help on merging titles: </b>')
        print('<a href="%s://%s/index.php/Editing:Merging_Titles">Editing:Merging_Titles</a><p>' % (PROTOCOL, WIKILOC))
        print('</div>')

        if mode == 2:
                print('<h2>Mode: Aggressive Title Match</h2>')
                print('Note that this mode will generate the most false positives.')
                print("""You can also try stricter %s or even stricter
                        %s.""" % (ISFDBLink('edit/find_dups.cgi', '%d+1' % author_id, 'Similar Title Mode'),
                                  ISFDBLink('edit/find_dups.cgi', author_id, 'Exact Title Mode')))
        elif mode == 1:
                print('<h2>Mode: Similar Title Match</h2>')
                if len(titles) <= 1000:
                        print("""You can also try %s or the most comprehensive
                                %s""" % (ISFDBLink('edit/find_dups.cgi', author_id, 'Exact Title Mode'),
                                         ISFDBLink('edit/find_dups.cgi', '%d+2' % author_id, 'Aggressive Title Mode')))
                else:
                        print("""You can also try %s. Aggressive mode is disabled for authors
                                with more than 1,000 titles for performance
                                reasons.""" % ISFDBLink('edit/find_dups.cgi', author_id, 'Exact Title Mode'))
        else:
                print('<h2>Mode: Exact Title Match</h2>')
                if len(titles) <= 1000:
                        print("""You can also try the more comprehensive %s or the most comprehensive 
                                 %s""" % (ISFDBLink('edit/find_dups.cgi', '%d+1' % author_id, 'Similar Title Mode'),
                                          ISFDBLink('edit/find_dups.cgi', '%d+2' % author_id, 'Aggressive Title Mode')))
                else:
                        print("""You can also try the more comprehensive %s. Aggressive mode is disabled for
                                 authors with more than 1,000 titles for performance
                                 reasons.""" % ISFDBLink('edit/find_dups.cgi', '%d+1' % author_id, 'Similar Title Mode'))
        print('<p>Be sure to check the title types and languages carefully before merging.')
        print('<p><hr>')

        found = 0
        if mode != 2:
                # Define the words (articles and common prepositions) which will need to be removed for "Similar Mode"
                remove_words = ("the", "a", "an", "as", "at", "by", "for", "from", "in", \
                                "into", "of", "off", "out", "over", "than", "then", "to", "up", "with")
                
                # Create a dictionary of words that will need to be replaced for "Similar Mode"
                replace_words = {'&': 'and',
                                 '0': 'zero',
                                 '10': 'ten',
                                 '11': 'eleven',
                                 '12': 'twelve',
                                 '13': 'thirteen',
                                 '14': 'fourteen',
                                 '15': 'fifteen',
                                 '16': 'sixteen',
                                 '17': 'seventeen',
                                 '18': 'eighteen',
                                 '19': 'nineteen',
                                 chr(150): '-',
                                 chr(151): '-'}
                # Create a dictionary of single digits and their substitution values to be used later
                digits = {'1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', \
                          '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}
                # Merge the 1-10 substitution pairs into the "replace_words" dictionary
                replace_words.update(digits)
                
                # Build a dictionary of "tens"
                tens = {'20': 'twenty', '30': 'thirty', '40': 'forty', '50': 'fifty', \
                        '60': 'sixty', '70': 'seventy', '80': 'eighty', '90': 'ninety'}
                
                # Add "21", "75", etc to "replace_words"
                for first_digit in tens:
                        replace_words[first_digit] = tens[first_digit]
                        for second_digit in digits:
                                number = first_digit[0] + second_digit
                                composite_word = tens[first_digit] + digits[second_digit]
                                replace_words[number] = composite_word
                
                # Add "100", "500", etc to "replace_words"
                for digit in digits:
                        number = digit + '00'
                        composite_word = digits[digit] + 'hundred'
                        replace_words[number] = composite_word
                
                # Build a dictionary with each work's title used as a key; the value is a list of title records with the same title
                title_dict = {}
                for title in titles:
                        # Convert the title to lowercase
                        title_title = title[TITLE_TITLE].lower()
                        # If the requested mode is "Similar Mode", regularize the title
                        if mode == 1:
                                parsed_title = title_title.split()
                                # Remove all words in the "remove_words" list
                                for word in remove_words:
                                        while word in parsed_title:
                                                parsed_title.remove(word)
                                # Replace all words in the "replace_words" dictionary with their replacement values
                                for replace_word in replace_words:
                                        while replace_word in parsed_title:
                                                parsed_title[parsed_title.index(replace_word)] = replace_words[replace_word]
                                # Re-assemble the string from the parsed list, removing spaces
                                title_title = "".join(parsed_title)
                                # Remove all punctuation characters
                                title_title = title_title.translate(str.maketrans("",""), string.punctuation)
                        if title_title not in title_dict:
                                title_dict[title_title] = [title]
                        else:
                                title_dict[title_title].append(title)
                # For each unique title, check if its records are potential duplicates
                for title_title in sorted(title_dict.keys()):
                        if len(title_dict[title_title]) > 1:
                                found = found + CheckOneList(title_dict[title_title], mode)
        else:
                found = CheckOneList(titles, mode)

        if not found:
                print('<h2>No duplicate candidates found.</h2>')


        PrintPostSearch(0, 0, 0, 0, 0, 0)
