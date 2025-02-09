/* 
   add_2_bleiler_references.sql is a MySQL script intended to
   add Bleiler's "The Guide to Supernatural Fiction" and
   "Science-Fiction: The Early Years" as secondary verification
   sources

   Version: $Revision: 1 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2018 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

insert into reference
(reference_id, reference_label, reference_fullname, pub_id, reference_url)
VALUES (12, 'Bleiler Supernatural', 'The Guide to Supernatural Fiction', 0,
'http://www.isfdb.org/wiki/index.php/Reference:BleilerSupernatural');

insert into reference
(reference_id, reference_label, reference_fullname, pub_id, reference_url)
VALUES (15, 'Bleiler Early Years', 'Science-Fiction: The Early Years', 0,
'http://www.isfdb.org/wiki/index.php/Reference:BleilerEarlyYears');
