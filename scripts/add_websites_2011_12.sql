/* 
   add_websites_2011_12.sql is a MySQL script intended to add OpenLibrary,
   Google Books, LibraryThing, Shelfari, GoodReads, Deutsche Nationalbibliothek,
   European Library and COPAC to the "Other Sites" section of the Publication
   display page.

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2011 Bill Longley and Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url)
VALUES (17,'Open Library','http://openlibrary.org/isbn/%s');
INSERT INTO websites (site_id, site_name, site_url)
VALUES (18,'Google Books','http://books.google.com/books?vid=ISBN%s');
INSERT INTO websites (site_id, site_name, site_url)
VALUES (19,'LibraryThing','http://www.librarything.com/isbn/%s');
INSERT INTO websites (site_id, site_name, site_url)
VALUES (20,'Shelfari','http://www.shelfari.com/search/books?Isbn=%s');
INSERT INTO websites (site_id, site_name, site_url)
VALUES (21,'GoodReads','http://www.goodreads.com/book/isbn/%s');
INSERT INTO websites (site_id, site_name, site_url)
VALUES (22,'Deutsche Nationalbibliothek','https://portal.d-nb.de/opac.htm?query=%s&method=simpleSearch');
INSERT INTO websites (site_id, site_name, site_url)
VALUES (23,'European Library (simple)','http://search.theeuropeanlibrary.org/portal/en/search/%28%22%s%22%29.query#');
INSERT INTO websites (site_id, site_name, site_url)
VALUES (24,'European Library (complex)','http://search.theeuropeanlibrary.org/portal/en/search/%28%22isbn%22+all+%22%s%22%29.query#');
INSERT INTO websites (site_id, site_name, site_url)
VALUES (25,'COPAC','http://copac.ac.uk/search?&isn=%s&sort-order=ti%2C-date');
