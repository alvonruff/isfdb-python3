/* 
   change_pubs_3_field_len.sql is a MySQL script intended to change the length of three
   three fields in table 'pubs' from varcar(16) and (32) to varchar(100). The fields are:
   pub_price (was 16)
   pub_isbn (was 32)
   pub_pages (was 16)

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2013 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

alter table pubs modify pub_price varchar(100);
alter table pubs modify pub_isbn varchar(100);
alter table pubs modify pub_pages varchar(100);
