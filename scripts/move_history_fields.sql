/* 
   move_history_fields.sql is a MySQL script intended to increment the values
   in field history_field, table history, from 15 to 16 and from 14 to 15.
   This is needed because 14 is the new value used by the language code.

   Version: $Revision: 1.1 $
   Date:    $Date: 2012/12/25 01:10:12 $

  (C) COPYRIGHT 2012 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update history set history_field=16 where history_field=15;

update history set history_field=15 where history_field=14;
