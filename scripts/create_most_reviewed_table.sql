/* 
   create_most_reviewed_table.sql is a MySQL script intended to
   create a table of most reviewed titles

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2018 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
create table IF NOT EXISTS most_reviewed (
	most_reviewed_id int(11) NOT NULL auto_increment,
	title_id int(11),
	year int(11),
	decade varchar(20),
	reviews int(11),
	PRIMARY KEY (most_reviewed_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE INDEX year ON most_reviewed (year);

CREATE INDEX decade ON most_reviewed (decade);
