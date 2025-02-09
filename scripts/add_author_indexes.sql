/* 
   add_author_indexes.sql is a MySQL script intended to
   add a new index (author_id) to table "webpages" and
   a new index (author_id) to table "emails"

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE INDEX author_id USING BTREE ON webpages(author_id);
CREATE INDEX author_id USING BTREE ON emails(author_id);

