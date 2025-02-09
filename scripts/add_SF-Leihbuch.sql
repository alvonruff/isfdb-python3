/* 
   add_NooSFere.sql is a MySQL script intended to add
   add_NooSFere as a new external idenifier type
	

   Version: $Revision: 15 $
   Date:    $Date: 2018-06-13 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2019 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('SF-Leihbuch', 'Science Fiction-Leihbuch-Datenbank');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (27, 1, 'http://www.sf-leihbuch.de/index.cfm?bid=%s');
