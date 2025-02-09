/* 
   correct_amazon_identifier_urls.sql is a MySQL script intended to
   escape apostrophes in links to Amazon web sites.
	

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2018 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE identifier_sites set site_url='https://www.amazon.co.uk/dp/%s?ie=UTF8&amp;tag=isfdb-21' where site_name='UK';

UPDATE identifier_sites set
site_url='https://www.amazon.com/dp/%s?ie=UTF8&amp;tag=isfdb-20&amp;linkCode=as2&amp;camp=1789&amp;creative=9325'
where site_name='US';
