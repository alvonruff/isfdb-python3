/* 
   change_BNB.sql is a MySQL script intended to
   change the URLs for BNB identifiers.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update identifier_sites set site_url =
'http://search.bl.uk/primo_library/libweb/action/search.do?fn=search&vl(freeText0)=%s'
where site_url like '%vid=BLBNB%';
