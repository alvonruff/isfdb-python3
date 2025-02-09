/* 
   create_missing_author_urls_table.sql is a MySQL script intended to
   create a table of missing URLs for authors.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
create table IF NOT EXISTS missing_author_urls (
	missing_id int(11) NOT NULL auto_increment,
	url_type smallint,
	url mediumtext,
	author_id int(11),
	resolved tinyint(1),
	PRIMARY KEY (missing_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
