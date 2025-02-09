/* 
   add_cleanup_id_2.sql is a MySQL script intended to
   alter table "cleanup" to add field cleanup_id_2

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE cleanup MODIFY report_type INT(11);
ALTER TABLE cleanup ADD COLUMN record_id_2 INT(11);
