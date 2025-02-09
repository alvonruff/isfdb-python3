/* 
   add_new_record_id_to_submissions.sql is a MySQL script intended to
   alter table "submissions" to add field "new_pub_id"

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE submissions ADD COLUMN new_record_id INT(11);