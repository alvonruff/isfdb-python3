/* 
   zero_our_cleanup_report_93.sql is a MySQL script intended to delete all
   entries from cleanup report 93, "Publication Title-Reference Title Mismatches"

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in.

   Version: $Revision: 1 $
   Date:    $Date: 2023-07-03 16:32:38 -0400 (Mon, 7 Jul 2023) $

  (C) COPYRIGHT 2024   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

delete from cleanup where report_type=93;
