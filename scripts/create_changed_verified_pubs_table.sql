/* 
   create_changed_verified_pubs_table.sql is a MySQL script intended to
   create a table of changed verified publications

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create table IF NOT EXISTS changed_verified_pubs (
	change_id int(11) NOT NULL auto_increment,
	pub_id int(11),
	sub_id int(11),
        verifier_id int(11),
        change_time datetime,
	PRIMARY KEY (change_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE INDEX recent_user ON changed_verified_pubs (verifier_id, change_time);
