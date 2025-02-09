/* 
   create_view_tables.sql is a MySQL script intended to add
   tables "author_views" and "title_views" to the MySQL database,
   then populate them with the data from "authors" and "titles".

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in.

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2022   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

CREATE TABLE IF NOT EXISTS author_views (
  author_id int(11) NOT NULL,
  views int(11),
  annual_views int(11),
  PRIMARY KEY  (author_id)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS title_views (
  title_id int(11) NOT NULL,
  views int(11),
  annual_views int(11),
  PRIMARY KEY  (title_id)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

INSERT INTO author_views (author_id, views, annual_views)
SELECT author_id, author_views, author_annualviews
FROM authors;

INSERT INTO title_views (title_id, views, annual_views)
SELECT title_id, title_views, title_annualviews
FROM titles;
