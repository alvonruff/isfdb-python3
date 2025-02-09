/* 
   create_award_titles_table.sql is a MySQL script intended to
   create a table of titles with awards

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2018 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
create table IF NOT EXISTS award_titles_report (
	award_title_id int(11) NOT NULL auto_increment,
	title_id int(11),
	score int(11),
	year int(11),
	decade varchar(20),
	title_type ENUM('ANTHOLOGY','BACKCOVERART','CHAPBOOK','COLLECTION',
'COVERART','INTERIORART','EDITOR','ESSAY','INTERVIEW','NOVEL',
'NONFICTION','OMNIBUS','POEM','REVIEW','SERIAL','SHORTFICTION'),
	PRIMARY KEY (award_title_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE INDEX year ON award_titles_report (year);

CREATE INDEX decade ON award_titles_report (decade);

CREATE INDEX title_type ON award_titles_report (title_type);
