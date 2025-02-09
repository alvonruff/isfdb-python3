/* 
   add_pub_webpages.sql is a MySQL script intended to
   alter table "webpages" to add column "pub_id"

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2019 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE webpages ADD pub_id INT(11);

CREATE INDEX pub_id USING BTREE ON webpages(pub_id);
