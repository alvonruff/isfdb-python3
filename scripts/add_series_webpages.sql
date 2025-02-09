/* 
   add_series_webpages.sql is a MySQL script intended to
   alter table "webpages" to add column "series_id" and
   table "series" to add column "series_note_id"

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE webpages ADD series_id INT(11) AFTER award_type_id;
ALTER TABLE series ADD series_note_id INT(11) AFTER series_parent_position;
