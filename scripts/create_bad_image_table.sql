/* 
   create_bad_image_table.sql is a MySQL script intended to
   create a table of bad images.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
create table IF NOT EXISTS bad_images (
	pub_id int(11) NOT NULL,
	image_url mediumtext,
	PRIMARY KEY (pub_id)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
