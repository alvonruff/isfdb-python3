/* 
   add_BLIC.sql is a MySQL script intended to add linking to BLIC by ISBN

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url)
VALUES (32,'British Library','http://explore.bl.uk/primo_library/libweb/action/dlSearch.do?vid=BLVU1&institution=BL&query=isbn,exact,%s');
