/* 
   create_templates_table.sql is a MySQL script intended to
   create a table of ISFDB-supported templates

   Version: $Revision: 418 $
   Date:    $Date: 2022-05-01 10:10:07 -0400 (Tue, 3 May 2022) $

  (C) COPYRIGHT 2022 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create table IF NOT EXISTS templates (
	template_id int(11) NOT NULL auto_increment,
	template_name tinytext,
	template_display text,
	template_type enum('Internal URL', 'External URL', 'Substitute String'),
	template_url text,
	template_mouseover text,
	PRIMARY KEY (template_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
