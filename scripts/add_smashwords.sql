/* 
   add_smashwords.sql is a MySQL script intended to add Smashwords 
   as another "Other Sites" option. 

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2011 Bill Longley and Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url)
VALUES (16,'Smashwords','http://www.smashwords.com/isbn/%s');
