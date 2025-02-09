/* 
   delete_merged_notes.sql is a MySQL script intended to
   delete notes entries for previosly merged notes.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
delete from notes where note_id in (420907, 367006, 306472, 306326, 236594, 209602, 209600, 91605, 53371, 23811);
