/* 
   create_trans_pub_series_table.sql is a MySQL script intended to
   create a table of transliterated publication series names

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
create table IF NOT EXISTS trans_pub_series (
	trans_pub_series_id int(11) NOT NULL auto_increment,
	trans_pub_series_name mediumtext,
	pub_series_id int(11),
	PRIMARY KEY (trans_pub_series_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
