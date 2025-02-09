/* 
   update_websites.sql is a MySQL script intended to:
    1. Remove Shelfari from the list of sites that we can link to
    2. Remove obsolete references to "European Library (Complex)" from user_sites
    3. Change the spelling of Goodreads to Goodreads
    4. Add National Diet Library as a supported sites
    5. Add the Library of Congress as a supported site
    6. Add Amazon JP (Japan) as a supported site

   Version: $Revision: 1.1 $
   Date:    $Date: 2017/04/06 19:40:49 $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

delete from websites where site_name = 'Shelfari';
delete from user_sites where site_id = 20;

delete from user_sites where site_id = 24;

update websites set site_name = 'Goodreads' where site_name = 'Goodreads';

INSERT INTO websites (site_id, site_name, site_url)
VALUES (20,'National Diet Library','http://iss.ndl.go.jp/api/openurl?rft.isbn=%s&locale=en');

INSERT INTO websites (site_id, site_name, site_url)
VALUES (24,'Library of Congress','https://catalog.loc.gov/vwebv/search?searchArg=%s&searchCode=ISBL&searchType=1');

INSERT INTO websites (site_id, site_name, site_url)
VALUES (31,'Amazon JP','https://www.amazon.co.jp/dp/%s');
