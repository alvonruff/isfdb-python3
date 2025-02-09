/* 
   dedup_title_relationships.sql is a MySQL script intended to remove 
   duplicates from the title relationships table.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2013   Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create table temptr
as select title_id, review_id, min(tr_id) tr_id
from title_relationships 
group by title_id, review_id;

truncate table title_relationships;

insert into title_relationships (title_id, review_id, tr_id)
select title_id, review_id, tr_id
from temptr;

drop table temptr;

