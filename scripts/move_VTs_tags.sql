/* 
   move_VTs_tags.sql is a MySQL script intended to
   move VTs' tags to their parent titles.

   Version: $Revision: 1.1 $
   Date:    $Date: 2014/02/02 20:36:57 $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
update tag_mapping,titles set tag_mapping.title_id=titles.title_parent where tag_mapping.title_id=titles.title_id and titles.title_parent!=0;