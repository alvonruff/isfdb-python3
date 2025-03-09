#!_PYTHONLOC
#
#     (C) COPYRIGHT 2009-2025   Al von Ruff, Ahasuerus and Dirk Stoecker
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 419 $
#     Date: $Date: 2019-05-15 10:54:53 -0400 (Wed, 15 May 2019) $

from SQLparsing import *
from library import *


def dup_authors():
        # Report 9999: Suspected Duplicate Authors. This report is run monthly
        # because it takes many hours to compile.
        for letter in tuple(string.ascii_uppercase):
                author_similarity(letter, 9999)

def author_similarity(letter, report_type):
        CNX = MYSQL_CONNECTOR()
        # Retrieve all authors whose names start with the specified letter
        query = """select author_id, author_canonical
            from authors a where a.author_canonical like '%s%%'
            and not exists(select 1 from pseudonyms p
            where a.author_id=p.pseudonym)""" % CNX.DB_ESCAPE_STRING(letter)

        CNX.DB_QUERY(query)
        record = CNX.DB_FETCHMANY()
        names = {}
        while record:
                author_id = record[0][0]
                name = record[0][1]
                names[author_id] = name
                record = CNX.DB_FETCHMANY()

        # Note on alternative string similarity algorithms as they apply to the ISFDB author table:
        #   Damerau-Levenshtein is the lowest, relative cost 13
        #   Levenstein is the second slowest, relative cost 7
        #   Jaro-Winkler is 1.6, but finds a lot of false positives
        #   Jaro distance is also 1.6 and has a good hit rate
        #   difflib's SequenceMatcher is 2.7 and finds fewer duplicates than Jaro distance
        #   Hamming distance is 0.2 seconds, by far the fastest, but finds a somewhat
        #   different set of potential duplicates compared to Jaro distance
        # We use Hamming distance for now since it is the fastest algorithm. Later on
        # we may also use Jaro distance if we can make it fast enough

        processed = []
        found = []
        for author_id1 in sorted(names, key = names.get):
                name1 = names[author_id1]
                for author_id2 in names:
                        if author_id1 == author_id2:
                                continue
                        if author_id2 in processed:
                                continue
                        name2 = names[author_id2]
                        distance = hamming_distance(name1, name2)
                        if distance == 1:
                                query = """select 1 from cleanup where report_type=%d
                                        and ((record_id=%d and record_id_2=%d)
                                        or (record_id=%d and record_id_2=%d))
                                        and resolved=1""" % (int(report_type), author_id1, author_id2, author_id2, author_id1)
                                CNX.DB_QUERY(query)
                                # Only add to the cleanup table if this record pair hasn't been "resolved"
                                if CNX.DB_NUMROWS():
                                        continue
                                update = """insert into cleanup (record_id, report_type, record_id_2)
                                values(%d, %d, %d)""" % (author_id1, int(report_type), author_id2)
                                CNX.DB_QUERY(update)
                processed.append(author_id1)

def hamming_distance(name1, name2):
        # Flip flop the names if the first one is shorter than the second
        if len(name2) > len(name1):
                name1, name2 = name2, name1

        # Calculate the distance as the difference in length
        # plus different characters
        distance = len(name1) - len(name2)
        for i, j in enumerate(name2):
                if j != name1[i]:
                        distance += 1
        return distance
