/* 
   create_cleanup_table.sql is a MySQL script intended to
   create a table of bad records for cleanup purposes. It
   will be re-populated every day by the nightly job.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
create table IF NOT EXISTS cleanup (
        cleanup_id int(11) NOT NULL AUTO_INCREMENT,
	record_id int(11),
        report_type tinyint(3),
	data mediumtext,
	PRIMARY KEY (cleanup_id),
        KEY (report_type)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
