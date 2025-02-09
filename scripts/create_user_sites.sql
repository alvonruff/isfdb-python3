/* 
   create_user_sites.sql is a MySQL script intended to add
   table "user_sites" to the MySQL database.

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in.

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2009   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE TABLE IF NOT EXISTS `user_sites` (
  `user_site_id` int(11) NOT NULL auto_increment,
  `site_id` int(11),
  `user_id` int(11),
  `user_choice` int(11) default '1',
  PRIMARY KEY  (`user_site_id`),
  KEY `user_id` (`user_id`),
  KEY `site_id` (`site_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;