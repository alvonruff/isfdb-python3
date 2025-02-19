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

UPDATE identifier_sites ids, identifier_types idt
set ids.site_url = 'https://www.goodreads.com/book/show/%s'
where idt.identifier_type_name = 'Goodreads'
and ids.identifier_type_id = idt.identifier_type_id;

UPDATE identifier_sites ids, identifier_types idt
set ids.site_url = 'https://lccn.loc.gov/%s'
where idt.identifier_type_name = 'LCCN'
and ids.identifier_type_id = idt.identifier_type_id;

UPDATE identifier_sites ids, identifier_types idt
set ids.site_url = 'https://www.worldcat.org/oclc/%s'
where idt.identifier_type_name = 'OCLC/WorldCat'
and ids.identifier_type_id = idt.identifier_type_id;

UPDATE identifier_sites ids, identifier_types idt
set ids.site_url = 'https://d-nb.info/%s'
where idt.identifier_type_name = 'DNB'
and ids.identifier_type_id = idt.identifier_type_id;

UPDATE identifier_sites ids, identifier_types idt
set ids.site_url = 'https://id.ndl.go.jp/bib/%s/eng'
where idt.identifier_type_name = 'NDL'
and ids.identifier_type_id = idt.identifier_type_id;

UPDATE identifier_sites ids, identifier_types idt
set ids.site_url = 'https://www.barnesandnoble.com/s/%s'
where idt.identifier_type_name = 'BN'
and ids.identifier_type_id = idt.identifier_type_id;
