/* 
   change_author_birthplace_len.sql is a MySQL script intended to change the length
   of the author_birthplace column in table authors from varcar(64) to mediumtext.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2013 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

alter table authors modify author_birthplace mediumtext;
