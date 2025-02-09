/* 
   create_authors_by_debut_date.sql is a MySQL script intended to
   create a table of the Authors By Debut Year stats report

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2018 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create table IF NOT EXISTS authors_by_debut_date (
	row_id int(11) NOT NULL auto_increment,
	debut_year int(4),
	author_id int(11),
	title_count int(11),
	PRIMARY KEY (row_id),
	KEY pub_id (debut_year)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
