/* 
   Separate_Norton_Award.sql is a MySQL script intended to move the awards from "Nebulas" 
   to their own award_type.

   Version: $Revision: 1.1 $
   Date:    $Date: 2013/03/06 12:57:51 $

  (C) COPYRIGHT 2013   Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

insert into award_types (award_type_id, award_type_code, award_type_name, award_type_wikipedia,	award_type_note_id)
VALUES (47, 'No', "Andre Norton Award", "http://en.wikipedia.org/wiki/Andre_Norton_Award", NULL);

update awards
set award_ttype = 'No'
where award_atype like '%Andre Norton%';

