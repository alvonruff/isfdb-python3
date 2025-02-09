/* 
   clean_dup_pseudos.sql is a MySQL script intended to clean up
   duplicate entries in the pseudonyms table, i.e. where an author has 
   been made the pseudonym of the same other name more than once.
   It does this simply by deleting the higer-numbered pseudo_id row, so
   may need running multiple times to clear all duplicates.
   It can be run as necessary until whatever bugs allow such 
   duplicates to be created have been fixed.

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2009   Bill Longley on behalf of ISFDB.
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

delete from pseudonyms
where pseudo_id in (
    select lastdup from (
        select author_id, pseudonym, count(*) numdups, max(pseudo_id) lastdup 
        from pseudonyms
        group by author_id, pseudonym
        having count(*) > 1
    ) dups
)
