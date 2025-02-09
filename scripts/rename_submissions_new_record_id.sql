/* 
   rename_submissions_new_record_id.sql is a MySQL script intended to change the
   name of the field "new_record_id" to "affected_record_id" in the table
   "submissions"

   Version: $Revision: 15 $
   Date:    $Date: 2020-03-04 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2020 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE submissions CHANGE COLUMN new_record_id affected_record_id int(11);

ALTER TABLE submissions DROP INDEX new_record_id, ADD INDEX affected_record_id (affected_record_id);
