/* 
   restore_non_genre_and_graphic_flags .sql is a MySQL script 
   intended to change the values of the fields 'title_non_genre'
   and "title_graphic' from NULL to No.

   Version: $Revision: 1.1 $
   Date:    $Date: 2016/07/26 02:21:15 $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE titles SET title_non_genre='No' where title_non_genre IS NULL;

UPDATE titles SET title_graphic='No' where title_graphic IS NULL;
