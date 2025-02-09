/* 
   create_trans_series_table.sql is a MySQL script intended to
   create a table of transliterated series names

   Version: $Revision: 15 $
   Date:    $Date: 2019-03-05 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2019 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
create table IF NOT EXISTS sfe3_authors (
	sfe3_authors_id int(11) NOT NULL auto_increment,
	url text,
	author_name text,
	resolved int(2),
	PRIMARY KEY (sfe3_authors_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

create index url on sfe3_authors (url(50));
