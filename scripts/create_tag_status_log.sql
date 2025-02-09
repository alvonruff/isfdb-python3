/* 
   create_tag_status_log.sql is a MySQL script intended to
   create a table of tag status (public/private) changes

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2021 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create table IF NOT EXISTS tag_status_log (
	change_id int(11) NOT NULL auto_increment,
	tag_id int(11),
	user_id int(11) NOT NULL,
	new_status tinyint,
	timestamp datetime,
	PRIMARY KEY (change_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE INDEX tag_id ON tag_status_log(tag_id);
CREATE INDEX timestamp ON tag_status_log(timestamp);
