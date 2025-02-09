/* 
   add_catalog_id.sql is a MySQL script intended to add a
   Catalog ID field to the pubs table. See FR 1116 for details.

   Version: $Revision: 1 $
   Date:    $Date: 2017-12-12 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE pubs ADD pub_catalog mediumtext;
