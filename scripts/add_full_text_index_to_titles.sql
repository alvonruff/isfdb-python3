/* 
   add_full_text_index_to_titles.sql is a MySQL script intended to
   add a full text index to the "titles" table

   Version: $Revision: 1 $
   Date:    $Date: 2012-12-28 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2022 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE FULLTEXT INDEX full_text on titles(title_title);
