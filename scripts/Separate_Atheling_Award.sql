/* 
   Separate_Atheling_Award.sql is a MySQL script intended to move the awards 
   from the Ditmars to their own award_type.

   Version: $Revision: 1.1 $
   Date:    $Date: 2013/03/07 18:28:56 $

  (C) COPYRIGHT 2013   Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

insert into award_types (award_type_id, award_type_code, award_type_name, award_type_wikipedia,	award_type_note_id)
VALUES (49, 'At', "William Atheling Jr Award for Criticism or Review", "http://en.wikipedia.org/wiki/William_Atheling_Jr._Award", NULL);

update awards
set award_ttype = 'At'
where award_atype like '%Atheling%';

