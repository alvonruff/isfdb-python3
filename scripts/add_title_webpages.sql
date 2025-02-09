/* 
   add_title_webpages.sql is a MySQL script intended to
   alter table "webpages" to include column "title_id".

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2011 Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE webpages ADD title_id INT(11) AFTER pub_series_id;
