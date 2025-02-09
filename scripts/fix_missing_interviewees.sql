/* 
   fix_missing_interviewees.sql is a MySQL script intended to clean up
   REVIEW titles where the reviewed author has been left blank due to 
   Bug 1743292.  

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2009   Bill Longley on behalf of ISFDB.
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

insert into canonical_author (title_id, author_id, ca_status)
select t.title_id, ca2.author_id, 2
from titles t, titles t2, canonical_author ca2
where t.title_ttype = 'INTERVIEW'
and t2.title_ttype = 'INTERVIEW'
and t.title_id = t2.title_parent
and ca2.title_id = t2.title_id
and ca2.ca_status = 2
and NOT EXISTS (select 1 from canonical_author ca
                WHERE t.title_id = ca.title_id
                and ca.ca_status = 2)
