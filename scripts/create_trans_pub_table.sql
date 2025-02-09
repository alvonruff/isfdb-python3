/* 
   create_trans_pub_table.sql is a MySQL script intended to
   create a table of transliterated publication titles

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create table IF NOT EXISTS trans_pubs (
	trans_pub_id int(11) NOT NULL auto_increment,
	trans_pub_title mediumtext,
	pub_id int(11),
	PRIMARY KEY (trans_pub_id),
	KEY pub_id (pub_id),
	KEY trans_pub_title (trans_pub_title(50))
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
