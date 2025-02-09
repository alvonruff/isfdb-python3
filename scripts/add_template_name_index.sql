/* 
   add_pub_images_index.sql is a MySQL script intended to
   add a new index (pub_image) to table "pubs"

   Version: $Revision: 418 $
   Date:    $Date: 2022-05-10 10:10:07 -0400 (Tue, 10 May 2022) $

  (C) COPYRIGHT 2022 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE INDEX template_name USING BTREE ON templates(template_name(20));

