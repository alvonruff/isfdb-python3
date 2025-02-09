/* 
   update_BL_links.sql is a MySQL script intended to update British Library links
   with a temporary URL pending restoration of their Web site.

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in.

   Version: $Revision: 1 $
   Date:    $Date: 2023-07-03 16:32:38 -0400 (Mon, 7 Jul 2023) $

  (C) COPYRIGHT 2024   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update websites set site_url='https://bll01.primo.exlibrisgroup.com/discovery/search?query=any,contains,%s&tab=LibraryCatalog&search_scope=Not_BL_Suppress&vid=44BL_INST:BLL01&lang=en&offset=0' where site_name='British Library';
