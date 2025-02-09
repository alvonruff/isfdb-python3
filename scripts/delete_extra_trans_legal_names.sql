/* 
   delete_extra_trans_legal_names.sql is a MySQL script intended to
   delete records from the trans_legal_names table which are
   associated with author records that are no longer in the database

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

delete from trans_legal_names where not exists
(select 1 from authors a where a.author_id=trans_legal_names.author_id);
