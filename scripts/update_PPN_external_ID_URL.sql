/* 
   update_PPN_external_ID_URL.sql is a MySQL script intended to
   update the Web site URL for PPN external idenifiers


   Version: $Revision: 15 $
   Date:    $Date: 2018-05-18 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2024 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update identifier_sites set site_url = 'https://picarta.oclc.org/psi/xslt/DB=3.9/XMLPRS=Y/PPN?PPN=%s' where identifier_type_id = 16;
