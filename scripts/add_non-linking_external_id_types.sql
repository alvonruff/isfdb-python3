/* 
   add_non-linking_external_id_types.sql is a MySQL script intended to
   add 5 non-linking external idenifier types
	

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2019 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('Reginald-1', 'R. Reginald. Science Fiction and Fantasy Literature: A Checklist, 1700-1974, with Contemporary Science Fiction Authors II. Gale Research Co., 1979, 1141p.');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('Reginald-3', 'Robert Reginald. Science Fiction and Fantasy Literature, 1975-1991: A Bibliography of Science Fiction, Fantasy, and Horror Fiction Books and Nonfiction Monographs. Gale Research Inc., 1992, 1512 p.');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('Bleiler Gernsback', 'Everett F. Bleiler, Richard Bleiler. Science-Fiction: The Gernsback Years. Kent State University Press, 1998, xxxii+730pp');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('Bleiler Supernatural', 'Everett F. Bleiler. The Guide to Supernatural Fiction. Kent State University Press, 1983, xii+723 p.');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('Bleiler Early Years', 'Richard Bleiler, Everett F. Bleiler. Science-Fiction: The Early Years. Kent State University Press, 1991, xxiii+998 p.');
