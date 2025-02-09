/* 
   delete_non_existing_pub_contents.sql is a MySQL script intended to
   delete pub_content entries for non-existing pubs.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
delete from pub_content where not exists (select 1 from pubs pu where pub_content.pub_id = pu.pub_id);