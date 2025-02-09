/* 
   update_amazon_tags.sql is a MySQL script intended to
   update all Amazon tags to be up-to-date
	

   Version: $Revision: 1.1 $
   Date:    $Date: 2017/06/29 17:27:59 $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update websites set site_url = 
'http://www.amazon.com/gp/product/%s?ie=UTF8&tag=isfdb-20&linkCode=as2&camp=1789&creative=9325&creativeASIN=%s'
where site_url like '%isfdbinternes-20%';

update identifier_sites set site_url =
'https://www.amazon.com/dp/%s?ie=UTF8&tag=isfdb-20&linkCode=as2&camp=1789&creative=9325'
where site_url like '%www.amazon.com/%';

update identifier_sites set site_url = 'https://www.amazon.co.uk/dp/%s?ie=UTF8&tag=isfdb-21'
where site_url like '%www.amazon.co.uk/%';
