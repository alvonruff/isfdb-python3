/* 
   add_award_indices.sql is a MySQL script intended to
   add indices by award category and award type to table "awards".

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create index award_cat ON awards(award_cat_id);
create index award_type ON awards(award_type_id);
