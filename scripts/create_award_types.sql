/* 
   create_award_types.sql is a MySQL script intended to
   create and populate a table of award types for use 
	 in the awards table.

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2011-2013 Bill Longley and Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
create table IF NOT EXISTS award_types (
	award_id int(11) NOT NULL auto_increment,
	award_code varchar(5),
	award_name mediumtext,
	PRIMARY KEY (award_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
insert into award_types VALUES 
	(1, 'An', 'Analog Award'),
	(2, 'Ap', 'Apollo Award'),
	(3, 'Ar', "Asimov's Readers' Poll"),
	(4, 'As', 'Aurealis Award'),
	(5, 'Au', 'Aurora Award'),
	(6, 'Ax', "Asimov's Undergraduate Award"),
	(7, 'Bf', 'British Fantasy Award'),
	(8, 'Bl', 'Balrog Award'),
	(9, 'Bs', 'British Science Fiction Association Award'),
	(10, 'Ca', 'John W. Campbell Award'),
	(11, 'Cb', 'Carl Brandon Society Award'),
	(12, 'Cc', 'Compton Crook Award'),
	(13, 'Cl', 'Arthur C. Clarke Award'),
	(14, 'Cy', 'Chesley Award'),
	(15, 'Dr', 'Deathrealm Award'),
	(16, 'Dt', 'Ditmar Award'),
	(17, 'En', 'Endeavour Award'),
	(18, 'Ga', 'Gandalf Award'),
	(19, 'Gd', 'Golden Duck Award'),
	(20, 'Gg', 'Gaughan Award'),
	(21, 'Hf', 'Hall of Fame Award'),
	(22, 'Hm', 'HOMer Award'),
	(23, 'Hu', 'Hugo Award'),
	(24, 'If', 'International Fantasy Award'),
	(25, 'Im', 'Imaginaire Award'),
	(26, 'Ih', 'International Horror Guild Award'),
	(27, 'Jc', 'John W. Campbell Award'),
	(28, 'Lc', 'Locus Poll'),
	(29, 'Lm', 'Lambda Award'),
	(30, 'My', 'Mythopoeic Award'),
	(31, 'Ne', 'Nebula Award'),
	(32, 'Pk', 'Philip K. Dick Award'),
	(33, 'Pr', 'Prometheus Award'),
	(34, 'Rh', 'Retro Hugo Award'),
	(35, 'Ry', 'Rhysling Award'),
	(36, 'Sc', 'SF Chronicle Award'),
	(37, 'Sf', 'SFBC Award'),
	(38, 'Sk', 'Skylark Award'),
	(39, 'Sn', 'Sunburst Award'),
	(40, 'St', 'Bram Stoker Award'),
	(41, 'Su', 'Sturgeon Award'),
	(42, 'Sw', 'Sidewise Award'),
	(43, 'Tp', 'James Tiptree, Jr. Award'),
	(44, 'Wf', 'World Fantasy Award'),
	(45, 'Wh', 'James White Award');
	
