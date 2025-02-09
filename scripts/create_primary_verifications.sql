/* 
   create_primary_verifications.sql is a MySQL script intended to
   create a table of primary verifications and move all primary
   verifications to it

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create table IF NOT EXISTS primary_verifications (
	verification_id int(11) NOT NULL auto_increment,
	pub_id int(11),
        user_id int(11),
        ver_time datetime,
        ver_transient tinyint,
	PRIMARY KEY (verification_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE INDEX pub ON primary_verifications (pub_id);
CREATE INDEX user ON primary_verifications (user_id);
CREATE INDEX time ON primary_verifications (ver_time);

insert into primary_verifications (pub_id, user_id, ver_time)
select pub_id, user_id, ver_time from verification
where reference_id in (1,15,16,17,18) and ver_status = 1;

insert into primary_verifications (pub_id, user_id, ver_time, ver_transient)
select pub_id, user_id, ver_time, 1 from verification
where reference_id = 12 and ver_status = 1;

delete from verification where reference_id in (1,12,15,16,17,18);

delete from reference where reference_id in (1,12,15,16,17,18);
