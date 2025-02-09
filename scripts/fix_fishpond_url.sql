/* 
   fix_fishpond_url.sql is a MySQL script intended to  fix FishPond URLs

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE websites SET site_url='http://www.fishpond.com.au/advanced_search_result.php?keywords=%s'
where site_name='Fishpond';
