/* 
   create_reports_table.sql is a MySQL script intended to add
   table "reports" to the MySQL database.

   Version: $Revision: 15 $
   Date:    $Date: 2018-08-05 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2018   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE TABLE IF NOT EXISTS reports (
  row_id int(11) NOT NULL auto_increment,
  report_id int(11),
  report_param int(11),
  report_data mediumtext,
  PRIMARY KEY (row_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
