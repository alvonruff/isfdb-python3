/* 
   add_australian_stores.sql is a MySQL script intended to add 
   fishpond.com.au and Booktopia as "Other Sites" options.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url) VALUES (27,'Fishpond','http://www.fishpond.com.au/?keywords=%s');
INSERT INTO websites (site_id, site_name, site_url) VALUES (28,'Booktopia','http://www.booktopia.com.au/prod%s.html');
ALTER TABLE websites ADD COLUMN site_isbn13 tinyint(3);
UPDATE websites SET site_isbn13=1 WHERE site_name in ('Booktopia', 'Smashwords');
