/* 
   add_FIM.sql is a MySQL script intended to add FIM (The FictionMags Index) as an external idenifier type
	

   Version: $Revision: 418 $
   Date:    $Date: 2024-11-23 10:10:07 -0400 (Sat, 23 Nov 2024) $

  (C) COPYRIGHT 2024 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('FIM', 'The FictionMags Index');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (35, 1, "http://www.philsp.com/homeville/FMI/ZZPERMLINK.ASP?NAME='%s'");

