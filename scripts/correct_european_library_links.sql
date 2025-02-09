/* 
   correct_european_library_links.sql is a MySQL script intended to  
   delete one of the two European Library rows in the websites tables
   and correct the other one.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

DELETE from websites where site_name='European Library (complex)';
UPDATE websites SET site_name='European Library' where site_name='European Library (simple)';
UPDATE websites SET site_url='http://www.theeuropeanlibrary.org/tel4/search?query=%s'
where site_name='European Library';

