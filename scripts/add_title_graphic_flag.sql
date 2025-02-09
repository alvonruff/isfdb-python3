/* 
   add_title_graphic_flag.sql is a MySQL script intended to
   alter table "titles" to add field title_graphic

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE titles ADD COLUMN title_graphic ENUM('Yes', 'No');
