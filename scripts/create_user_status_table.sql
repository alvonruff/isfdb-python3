/* 
   create_user_status_table.sql is a MySQL script intended to
   create a user status table

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2016 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create table IF NOT EXISTS user_status (
	user_status_id int(11) NOT NULL auto_increment,
	user_id int(11),
        last_changed_ver_pubs datetime,
        last_viewed_ver_pubs datetime,
	PRIMARY KEY (user_status_id),
        KEY (user_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
