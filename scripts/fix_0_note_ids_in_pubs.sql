/* 
   fix_0_note_ids_in_pubs.sql is a MySQL script intended to
   change 0 values in the note_id in table pubs to NULL

   Version: $Revision: 1 $
   Date:    $Date: 2012-12-28 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2023 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE pubs SET note_id = NULL where note_id = 0;
