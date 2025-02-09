/* 
   delete_bad_mapping_entries.sql is a MySQL script intended to
   delete records from canonical_author and pub_authors that are
   associated with no longer existing titles and publications

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

delete from canonical_author where not exists
(select 1 from titles t where t.title_id=canonical_author.title_id);

delete from pub_authors where not exists
(select 1 from pubs where pubs.pub_id=pub_authors.pub_id);

delete from authors where author_id=213489;
