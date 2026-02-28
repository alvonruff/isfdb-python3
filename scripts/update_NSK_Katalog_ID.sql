/* 
   add_NSK_Katalog_ID.sql is a MySQL script intended to add NSK Katalog (National
   and University Library in Zagreb) as an external idenifier type
	

   Version: $Revision: 418 $
   Date:    $Date: 2024-11-23 10:10:07 -0400 (Sat, 23 Nov 2024) $

  (C) COPYRIGHT 2026 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


UPDATE identifier_sites
SET site_url = "https://katalog.nsk.hr/permalink/385BUKINET_ZANSK/%s"
where identifier_type_id = 36;


