/* 
   Create_Quill_and_Scwartz_awards.sql is a MySQL script intended
   to create entries for the Quill Award and Ruth and Sylvia Schwartz Children's Book Award

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

insert into award_types (award_type_id, award_type_code, award_type_name, award_type_wikipedia,	award_type_note_id, award_type_by, award_type_for) VALUES (52, 'Qu', 'Quill Award', NULL, NULL, NULL, NULL);
insert into award_types (award_type_id, award_type_code, award_type_name, award_type_wikipedia,	award_type_note_id, award_type_by, award_type_for) VALUES (53, 'Sh', 'Ruth and Sylvia Schwartz Children\'s Book Award', NULL, NULL, NULL, NULL);
