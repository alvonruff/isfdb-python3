/* 
   update_BL_ID_URLs.sql is a MySQL script intended to change the URLs
   of External IDs for the British Library. The previous URL pattern was
   https://bll01.primo.exlibrisgroup.com/discovery
   /fulldisplay?docid=alma99%s0100000&context=L&vid=44BL_INST:BLL01
   The new patter is
   https://catalogue.bl.uk/permalink/44BL_MAIN/n6kovr/alma99%s0109251
	

   Version: $Revision: 418 $
   Date:    $Date: 2024-11-23 10:10:07 -0400 (Sat, 23 Nov 2024) $

  (C) COPYRIGHT 2026 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


UPDATE identifier_sites
SET site_url = "https://catalogue.bl.uk/permalink/44BL_MAIN/n6kovr/alma99%s0109251"
where identifier_type_id = 2;
