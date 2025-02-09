/* 
   add_date_indices.sql is a MySQL script intended to
   add date indices to 2 tables: titles and pubs

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2018 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE INDEX title_date USING BTREE ON titles(title_copyright);

CREATE INDEX pub_date USING BTREE ON pubs(pub_year);
