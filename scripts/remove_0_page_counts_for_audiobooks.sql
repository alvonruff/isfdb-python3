/* 
   remove_0_page_counts_for_audiobooks.sql is a MySQL script intended to add
   remove "0" page counts for audio books

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2018 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update pubs set pub_pages = NULL where pub_pages = '0' and pub_ptype like '%audio%';
