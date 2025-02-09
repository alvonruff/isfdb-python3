/* 
   add_field_len.sql is a MySQL script intended to change the length of three
   three fields from varcar(64) to mediumtext. The fields are:
   pub_series_name in table pub_series
   series_title in table series_title
   publisher_name in table publishers

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2012 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

alter table pub_series modify pub_series_name mediumtext;
create index pub_series_name on pub_series (pub_series_name(50));

alter table series modify series_title mediumtext;

drop index publisher_name on publishers;
alter table publishers modify publisher_name mediumtext;
create index publisher_name on publishers (publisher_name(50));
