/* 
   add_award_type_fields.sql is a MySQL script intended to
   alter table "webpages" to add column "award_type_id" and
   table "award_types" to add columns "award_type_wikipedia"
   and "award_type_note_id"

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2013 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE webpages ADD award_type_id INT(11) AFTER title_id;
ALTER TABLE award_types ADD award_type_wikipedia mediumtext AFTER award_name;
ALTER TABLE award_types ADD award_type_note_id INT(11) AFTER award_type_wikipedia;
ALTER TABLE award_types CHANGE award_id award_type_id int(11);
ALTER TABLE award_types CHANGE award_code award_type_code varchar(5);
ALTER TABLE award_types CHANGE award_name award_type_name mediumtext;
