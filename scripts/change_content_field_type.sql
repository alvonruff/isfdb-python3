/* 
   change_content_field_type.sql.sql is a MySQL script intended to
   alter table "titles" to change the type of the "title_content"
   field from VARCHAR(32) to TINYTEXT

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2018 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE titles MODIFY COLUMN title_content TINYTEXT;
