/* 
   update_COBISS_identifiers.sql is a MySQL script intended to
   update the Web site URL for COBISS.SR and COBISS.BG external idenifiers.


   Version: $Revision: 15 $
   Date:    $Date: 2018-05-18 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2025 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update identifier_sites set site_url = 'https://plus.cobiss.net/cobiss/bg/en/bib/%s#full' where identifier_type_id = 33;

update identifier_sites set site_url = 'https://plus.cobiss.net/cobiss/sr/en/bib/%s#full' where identifier_type_id = 34;

