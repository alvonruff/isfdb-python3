/* 
   suppress_help_bubbles.sql is a MySQL script intended to
   alter table "user_preferences" to add field suppress_help_bubbles

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/04/08 02:58:45 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE user_preferences ADD COLUMN suppress_help_bubbles TINYINT(1);