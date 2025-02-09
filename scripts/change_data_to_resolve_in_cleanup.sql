/* 
   change_data_to_resolve_in_cleanup.sql is a MySQL script intended to
   alter table "cleanup" as follows: rename column "data" to "resolve and
   change its type from mediumtext to tinyint

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE cleanup CHANGE data resolved TINYINT(1);
