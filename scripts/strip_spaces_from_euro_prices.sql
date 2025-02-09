/* 
   strip_spaces_from_euro_prices.sql is a MySQL script intended to
   strip trailing spaces after the Euro sign in the price field
	

   Version: $Revision: 15 $
   Date:    $Date: 2018-05-18 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2018 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


UPDATE pubs set pub_price = REPLACE(pub_price, concat(CHAR(0x80),' '), CHAR(0x80))
where pub_price like concat('%',CHAR(0x80),' ','%');

