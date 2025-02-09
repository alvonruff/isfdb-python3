/* 
   fix_campbell_award.sql is a MySQL script intended to
   mass change entries in the "awards" table for Campbell
   Memorial ('Ca') records

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update awards set award_atype='Best Science Fiction Novel', award_level=90 where award_ttype='Ca' and award_level=9;
update awards set award_atype='Best Science Fiction Novel' where award_ttype='Ca' and award_level=1 and award_atype='Winner';
update awards set award_atype='Best Science Fiction Novel' where award_ttype='Ca' and award_level=2 and award_atype='Second Place';
update awards set award_atype='Best Science Fiction Novel' where award_ttype='Ca' and award_level=3 and  award_atype='Third Place';
