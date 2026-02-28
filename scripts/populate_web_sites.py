#!_PYTHONLOC
from __future__ import print_function
#
#         (C) COPYRIGHT 2009-2026   Ahasuerus, Al von Ruff
#           ALL RIGHTS RESERVED
#
#         The copyright notice above does not evidence any actual or
#         intended publication of such source code.
#
#         Version: $Revision: 1.1 $
#         Date: $Date: 2009/10/10 22:45:23 $


import cgi
import sys
import os
import string
from SQLparsing import *

debug = 0

def populate():

        pop = [('http://www.abebooks.com/servlet/SearchResults?isbn=%s', 'AbeBooks.com')]
        pop.append(('http://www.alibris.com/booksearch?isbn=%s', 'alibris'))
        pop.append(('http://www.amazon.com/gp/product/%s?ie=UTF8&tag=isfdbinternes-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=%s', 'Amazon US'))
        pop.append(('http://www.amazon.co.uk/exec/obidos/ASIN/%s/isfdb-21', 'Amazon UK'))
        pop.append(('http://www.amazon.ca/dp/%s', 'Amazon CA'))
        pop.append(('http://www.amazon.de/dp/%s', 'Amazon DE'))
        pop.append(('http://www.amazon.fr/dp/%s', 'Amazon FR'))
        pop.append(('http://search.barnesandnoble.com/booksearch/isbnInquiry.asp?EAN=%s', 'Barnes & Noble'))
        pop.append(('http://www.biggerbooks.com/bk_detail.aspx?isbn=%s', 'BiggerBooks.com'))
        pop.append(('http://bookshop.blackwell.com/jsp/welcome.jsp?action=search&type=isbn&term=%s', 'Blackwell'))
        pop.append(('http://www.booksamillion.com/ncom/books?isbn=%s', 'Books-A-Million'))
        pop.append(('http://www.ecampus.com/bk_detail.asp?ISBN=%s', 'eCampus.com'))
        pop.append(('http://www.powells.com/biblio?isbn=%s', 'Powells'))
        pop.append(('http://www.textbookx.com/detail-book-%s.html', 'TextBook.com'))
        pop.append(('http://www.worldcat.org/isbn/%s', 'WorldCat'))
        return pop

if __name__ == '__main__':

        CNX = MYSQL_CONNECTOR()

        pop = populate()
        for site in pop:
                site_url = CNX.DB_ESCAPE_STRING(site[0])
                site_name = CNX.DB_ESCAPE_STRING(site[1])
                update = "insert into websites (site_url, site_name) values('%s','%s')" % (site_url, site_name)
                print(update)
                if debug == 0:
                        CNX.DB_QUERY(update)
