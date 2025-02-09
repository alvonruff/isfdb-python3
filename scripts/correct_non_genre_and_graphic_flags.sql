/* 
   correct_non_genre_and_graphic_flags.sql is a MySQL script intended to
   correct the "non-genre" and "graphic format" flags for REVIEW and
   INTERVIEW titles

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update titles set title_non_genre='No' where title_ttype='REVIEW' or title_ttype='INTERVIEW';

update titles set title_graphic='No' where title_ttype='REVIEW' or title_ttype='INTERVIEW';

