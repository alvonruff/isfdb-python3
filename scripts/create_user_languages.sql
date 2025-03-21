/* 
   create_user_languages.sql is a MySQL script intended to add
   table "user_languages" to the MySQL database.

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in.

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2009   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE TABLE IF NOT EXISTS `user_languages` (
  `user_lang_id` int(11) NOT NULL auto_increment,
  `user_id` int(11),
  `lang_id` int(11),
  `user_choice` int(11),
  PRIMARY KEY  (`user_lang_id`),
  KEY `user_id` (`user_id`),
  KEY `lang_id` (`lang_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;