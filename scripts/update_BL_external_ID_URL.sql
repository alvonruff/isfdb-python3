/* 
   update_BL_external_ID_URL.sql is a MySQL script intended to
   update the Web site URL for BL external idenifiers. Note that the new URL schema is temporary since BL is still recovering from the 2023 hacking attack.


   Version: $Revision: 15 $
   Date:    $Date: 2018-05-18 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2025 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update identifier_sites set site_url = 'https://bll01.primo.exlibrisgroup.com/discovery/fulldisplay?docid=alma99%s0100000&context=L&vid=44BL_INST:BLL01' where identifier_type_id = 2;
