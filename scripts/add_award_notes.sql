/* 
   add_award_notes.sql is a MySQL script intended to
   alter table "awards" to add field award_note_id

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE awards ADD COLUMN award_note_id INT(11);
