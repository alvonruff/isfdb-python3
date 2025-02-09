/* 
   add_webpages_indexes.sql is a MySQL script intended to
   add indexes for all fields to table "webpages"

   Version: $Revision: 418 $
   Date:    $Date: 2019-12-12 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2019 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE INDEX publisher_id USING BTREE ON webpages(publisher_id);

CREATE INDEX pub_series_id USING BTREE ON webpages(pub_series_id);

CREATE INDEX title_id USING BTREE ON webpages(title_id);

CREATE INDEX award_type_id USING BTREE ON webpages(award_type_id);

CREATE INDEX series_id USING BTREE ON webpages(series_id);

CREATE INDEX award_cat_id USING BTREE ON webpages(award_cat_id);

