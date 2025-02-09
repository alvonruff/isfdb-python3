/* 
   strip_leading_trailing_spaces.sql is a MySQL script intended to
   strip leading and trailing spaces from the titles of all 
   title records

   Version: $Revision: 1.1 $
   Date:    $Date: 2015/01/15 23:31:06 $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update titles set title_title = TRIM(title_title);
