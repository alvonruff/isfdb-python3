/* 
   update_websites2.sql is a MySQL script intended to:
    1. Fix BiggerBooks links
    2. Make Library of Congress and NDL links use ISBN13s

   Version: $Revision: 1.1 $
   Date:    $Date: 2017/04/07 00:55:14 $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update websites set site_url = 'http://www.biggerbooks.com/book/%s' where site_name = 'BiggerBooks.com';

update websites set site_isbn13 = 1 where site_name = 'Library of Congress';

update websites set site_isbn13 = 1 where site_name = 'National Diet Library';
