/* 
   empty_storylen_in_titles.sql is a MySQL script intended to
   change the empty ("") storylen values in the titles table
   to NULLS

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update titles set title_storylen = NULL where title_storylen = '';
