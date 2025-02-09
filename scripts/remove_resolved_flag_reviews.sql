/* 
   remove_resolved_flag_reviews.sql is a MySQL script intended to
   remove all Resolved flags in table "cleanup" for report 41

   Version: $Revision: 1.1 $
   Date:    $Date: 2015/01/17 22:24:49 $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update cleanup set resolved=NULL where report_type=41;
