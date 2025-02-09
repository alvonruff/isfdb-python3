/* 
   rename_COPAC_links.sql is a MySQL script intended to rename COPAC links


   Version: $Revision: 418 $
   Date:    $Date: 2021-09-16 10:10:07 -0400 (Thu, 16 Sep 2021) $

  (C) COPYRIGHT 2021 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


UPDATE websites SET site_name = 'Library Hub Discover', site_url = 'https://discover.libraryhub.jisc.ac.uk/search?&isn=%s&sort-order=ti%2C-date' where site_name = 'COPAC';

UPDATE identifier_types SET identifier_type_name = 'COPAC (defunct)' where identifier_type_name = 'COPAC';
