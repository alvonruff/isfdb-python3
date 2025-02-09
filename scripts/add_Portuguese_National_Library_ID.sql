/* 
   add_Portuguese_National_Library_ID.sql is a MySQL script intended to
   add Portuguese National Library (PORBASE) as an external idenifier
	

   Version: $Revision: 418 $
   Date:    $Date: 2019-12-02 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2020 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('PORBASE', 'Biblioteca Nacional de Portugal');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (29, 1, 'http://id.bnportugal.gov.pt/bib/porbase/%s');

