/* 
   fix_tag_mapping.sql is a MySQL script intended to fix the tag_mapping table
   which currently has a single row out of sync with the tags table.

   Version: $Revision: 15 $
   Date:    $Date: 2025-02-21 16:32:38 -0400 (Fri, 21 Feb 2025) $

  (C) COPYRIGHT 2025   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

delete from tag_mapping where tagmap_id = 483024;
