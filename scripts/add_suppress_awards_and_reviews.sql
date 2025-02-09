/* 
   add_suppress_awards_and_reviews.sql is a MySQL script intended to
   alter table "user_preferences" to add two field:
   suppress_awards and suppress_reviews

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE user_preferences ADD COLUMN suppress_awards TINYINT(1);
ALTER TABLE user_preferences ADD COLUMN suppress_reviews TINYINT(1);