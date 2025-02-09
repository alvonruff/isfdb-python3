/* 
   create_deleted_secondary_verifications.sql is a MySQL script intended to
   create a table of deleted secondary verifications

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2020 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create table IF NOT EXISTS deleted_secondary_verifications (
	deletion_id int(11) NOT NULL auto_increment,
	pub_id int(11),
	reference_id int(11),
        verifier_id int(11),
        verification_time datetime,
        deleter_id int(11),
        deletion_time datetime,
	PRIMARY KEY (deletion_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE INDEX deletion_time USING BTREE ON deleted_secondary_verifications(deletion_time);

CREATE INDEX verifier USING BTREE ON deleted_secondary_verifications(verifier_id, deletion_time);