/* 
   fix_notes_with_mismatched_angle_brackets.sql is a MySQL script intended to
   fix Notes records with mismatched angle brackets

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE notes set note_note='' where note_id=222143;
DELETE from notes where note_id=343;
UPDATE authors set note_id=NULL where author_id=973;