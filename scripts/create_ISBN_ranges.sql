/* 
   create_ISBN_ranges.sql is a MySQL script intended to add
   table "isbn_ranges" to the MySQL database.

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in.

   Version: $Revision: 1 $
   Date:    $Date: 2023-07-03 16:32:38 -0400 (Mon, 7 Jul 2023) $

  (C) COPYRIGHT 2024   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE TABLE IF NOT EXISTS isbn_ranges (
  start_value bigint,
  end_value bigint,
  prefix_length tinyint,
  publisher_length tinyint,
  PRIMARY KEY (start_value)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
