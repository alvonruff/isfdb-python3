/* 
   create_view_tables.sql is a MySQL script intended to update
   all eligible third party Web site links from HTTP to HTTPS.

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2022   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE websites
set site_url = 'https://www.amazon.com/gp/product/%s?ie=UTF8&tag=isfdb-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=%s'
where site_name = 'Amazon US';

UPDATE websites
set site_url = 'https://www.amazon.co.uk/exec/obidos/ASIN/%s/isfdb-21'
where site_name = 'Amazon UK';

UPDATE websites
set site_url = 'https://www.amazon.ca/dp/%s'
where site_name = 'Amazon Canada';

UPDATE websites
set site_url = 'https://www.amazon.de/dp/%s'
where site_name = 'Amazon Germany';

UPDATE websites
set site_url = 'https://www.amazon.fr/dp/%s'
where site_name = 'Amazon France';

UPDATE websites
set site_url = 'https://catalogue.bnf.fr/rechercher.do?motRecherche=%s'
where site_name = 'Bibliotheque nationale de France';

UPDATE websites
set site_url = 'https://www.booktopia.com.au/prod%s.html'
where site_name = 'Booktopia';

UPDATE websites
set site_url = 'https://www.angusrobertson.com.au/books/p/%s'
where site_name = 'Angus & Robertson';

UPDATE websites
set site_url = 'https://www.fishpond.com.au/advanced_search_result.php?keywords=%s'
where site_name = 'Fishpond';

UPDATE websites
set site_url = 'https://www.abebooks.com/servlet/SearchResults?isbn=%s'
where site_name = 'AbeBooks.com';

UPDATE websites
set site_url = 'https://www.alibris.com/booksearch?isbn=%s'
where site_name = 'alibris';

UPDATE websites
set site_url = 'https://www.barnesandnoble.com/s/%s'
where site_name = 'Barnes & Noble';

UPDATE websites
set site_url = 'https://www.biggerbooks.com/book/%s'
where site_name = 'BiggerBooks.com';

UPDATE websites
set site_url = 'https://blackwells.co.uk/bookshop/product/%s'
where site_name = 'Blackwell';

UPDATE websites
set site_url = 'https://www.booksamillion.com/search?query=%s&where=All'
where site_name = 'Books-A-Million';

UPDATE websites
set site_url = 'https://www.ecampus.com/bk_detail.asp?ISBN=%s'
where site_name = 'eCampus.com';

UPDATE websites
set site_url = 'https://www.textbookx.com/detail-book-%s.html'
where site_name = 'TextBook.com';

UPDATE websites
set site_url = 'https://www.worldcat.org/isbn/%s'
where site_name = 'WorldCat';

UPDATE websites
set site_url = 'https://www.smashwords.com/isbn/%s'
where site_name = 'Smashwords';

UPDATE websites
set site_url = 'https://openlibrary.org/isbn/%s'
where site_name = 'Open Library';

UPDATE websites
set site_url = 'https://books.google.com/books?vid=ISBN%s'
where site_name = 'Google Books';

UPDATE websites
set site_url = 'https://www.librarything.com/isbn/%s'
where site_name = 'LibraryThing';

UPDATE websites
set site_url = 'https://www.goodreads.com/book/isbn/%s'
where site_name = 'Goodreads';

UPDATE websites
set site_url = 'https://www.theeuropeanlibrary.org/tel4/search?query=%s'
where site_name = 'European Library';

UPDATE websites
set site_url = 'https://iss.ndl.go.jp/api/openurl?rft.isbn=%s&locale=en'
where site_name = 'National Diet Library';

UPDATE websites
set site_url = 'https://www.powells.com/searchresults?keyword=%s'
where site_name = 'Powells';
