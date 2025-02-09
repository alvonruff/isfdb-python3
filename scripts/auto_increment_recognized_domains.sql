/* 
   auto_increment_recognized_domains.sql is a MySQL script intended to change
   field "domain_id" in table "recognized_domains" to use auto_increment

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in.

   Version: $Revision: 1 $
   Date:    $Date: 2023-07-03 16:32:38 -0400 (Mon, 7 Jul 2023) $

  (C) COPYRIGHT 2023   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE recognized_domains MODIFY COLUMN domain_id INT auto_increment;
