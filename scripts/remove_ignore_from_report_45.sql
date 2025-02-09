/* 
   remove_ignore_from_report_45.sql is a MySQL script intended to
   remove the ignore flags for cleanup report 45 (Variant Title Type Mismatches)

   Version: $Revision: 15 $
   Date:    $Date: 2018-07-12 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2018 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE cleanup set resolved=NULL where report_type=45;
