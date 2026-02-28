/* 
   update_BL_links_for_2026.sql is a MySQL script intended to update
   British Library links after the restoration of their Web site.

   Version: $Revision: 1 $
   Date:    $Date: 2023-07-03 16:32:38 -0400 (Mon, 7 Jul 2023) $

  (C) COPYRIGHT 2026   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update websites set site_url='https://catalogue.bl.uk/nde/search?query=%s&tab=Everything&search_scope=MyInst_and_CI&searchInFulltext=false&vid=44BL_MAIN:BLL01_NDE&lang=en' where site_name='British Library';
