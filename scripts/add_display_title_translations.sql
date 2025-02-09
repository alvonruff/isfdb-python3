/* 
   add_display_title_translations.sql is a MySQL script intended to
   alter table "user_preferences" to add the field display_title_translations

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2020 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE user_preferences ADD COLUMN display_title_translations TINYINT(1);

UPDATE user_preferences SET display_title_translations = 1;
