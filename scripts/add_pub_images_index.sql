/* 
   add_pub_images_index.sql is a MySQL script intended to
   add a new index (pub_image) to table "pubs"

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE INDEX pub_image USING BTREE ON pubs(pub_frontimage(50));

