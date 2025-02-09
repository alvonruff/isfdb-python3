/* 
   create_legal_names_table.sql is a MySQL script intended to
   create a table of transliterated legal names

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
create table IF NOT EXISTS trans_legal_names (
	trans_legal_name_id int(11) NOT NULL auto_increment,
	trans_legal_name mediumtext,
	author_id int(11),
	PRIMARY KEY (trans_legal_name_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
