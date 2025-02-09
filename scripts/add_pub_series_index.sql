/* 
   add_publisher_index.sql is a MySQL script intended to add
   a publication series index to the "pubs" table

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2019 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create index pub_series_id on pubs (pub_series_id);
