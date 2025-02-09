/* 
   Separate_Heinlein_Award.sql is a MySQL script intended to move the awards from "Compton Crook Award" 
   to their own award_type.

   Version: $Revision: 1.1 $
   Date:    $Date: 2013/03/06 12:59:01 $

  (C) COPYRIGHT 2013   Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

insert into award_types (award_type_id, award_type_code, award_type_name, award_type_wikipedia,	award_type_note_id)
VALUES (48, 'He', "Robert A. Heinlein Award", "http://en.wikipedia.org/wiki/Robert_A._Heinlein_Award", NULL);

update awards
set award_ttype = 'He'
where award_atype like '%Robert A. Heinlein%';

