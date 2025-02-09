/* 
   create_trans_author_table.sql is a MySQL script intended to
   create a table of transliterated author titles

   Version: $Revision: 418 $
   Date:    $Date: 2013-06-29 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2023 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create table IF NOT EXISTS web_api_users (
	user_id int(11) NOT NULL,
	PRIMARY KEY (user_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
