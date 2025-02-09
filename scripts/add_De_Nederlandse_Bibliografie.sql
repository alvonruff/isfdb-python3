/* 
   add_Nederlandse_Bibliografie.sql is a MySQL script intended to
   add De Nederlandse Bibliografie as an external idenifier
	

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('PPN', 'De Nederlandse Bibliografie Pica Productie Nummer');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (16, 1, 'http://picarta.pica.nl/xslt/DB=3.9/XMLPRS=Y/PPN?PPN=%s');

