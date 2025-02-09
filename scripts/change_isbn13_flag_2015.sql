/* 
   change_isbn13_flag_2015.sql is a MySQL script intended to  
   change the ISBN13 flag to link to third party sites using
   ISBN13 rather than ISBN10.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE websites SET site_isbn13=1 where site_name='Barnes & Noble';
UPDATE websites SET site_isbn13=1 where site_name='GoodReads';
UPDATE websites SET site_isbn13=1 where site_name='WorldCat';
UPDATE websites SET site_isbn13=1 where site_name='Google Books';
UPDATE websites SET site_isbn13=1 where site_name='Fishpond';
UPDATE websites SET site_isbn13=1 where site_name='COPAC';
UPDATE websites SET site_isbn13=1 where site_name='LibraryThing';
UPDATE websites SET site_isbn13=1 where site_name='Shelfari';
UPDATE websites SET site_isbn13=1 where site_name='Powells';
UPDATE websites SET site_isbn13=1 where site_name='TextBook.com';
UPDATE websites SET site_isbn13=1 where site_name='eCampus.com';
UPDATE websites SET site_isbn13=1 where site_name='Books-A-Million';

UPDATE websites SET site_url='http://www.booksamillion.com/search?query=%s&where=All' where site_name='Books-A-Million';

UPDATE websites SET site_url='https://portal.dnb.de/opac.htm?query=%s&method=simpleSearch' where site_name='Deutsche Nationalbibliothek';

UPDATE websites SET site_isbn13=1 where site_name='AbeBooks.com';
UPDATE websites SET site_isbn13=1 where site_name='alibris';
UPDATE websites SET site_isbn13=1 where site_name='BiggerBooks.com';
UPDATE websites SET site_isbn13=1 where site_name='Blackwell';

UPDATE websites SET
 site_url='http://catalogue.bnf.fr/servlet/AccueilConnecte?recherche=equation&Equation=ibn+=+%s' where
 site_name='Bibliotheque nationale de France';

UPDATE websites SET site_isbn13=1 where site_name='Bibliotheque nationale de France';

UPDATE websites SET site_isbn13=1 where site_name='Deutsche Nationalbibliothek';
