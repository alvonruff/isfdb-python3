/* 
   create_identifiers.sql is a MySQL script intended to
   create the following three tables:
	identifier_types
	identifier_sites
	identifiers
   It also populates the first two tables
	

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

create table IF NOT EXISTS identifier_types (
	identifier_type_id int(11) NOT NULL auto_increment,
	identifier_type_name tinytext,
	identifier_type_full_name text,
	PRIMARY KEY (identifier_type_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

create table IF NOT EXISTS identifier_sites (
	identifier_site_id int(11) NOT NULL auto_increment,
	identifier_type_id int(11),
	site_position tinyint(3),
	site_url text,
	site_name text,
	PRIMARY KEY (identifier_site_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE INDEX type ON identifier_sites (identifier_type_id);

create table IF NOT EXISTS identifiers (
	identifier_id int(11) NOT NULL auto_increment,
	identifier_type_id int(11),
	identifier_value text,
        pub_id int(11),
	PRIMARY KEY (identifier_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE INDEX pub ON identifiers (pub_id);

CREATE INDEX type_value ON identifiers (identifier_type_id, identifier_value(20));


INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('ASIN', 'Amazon Standard Identification Number');

INSERT INTO identifier_types (identifier_type_name,identifier_type_full_name)
VALUES ('BL', 'The British Library');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('BNB', 'The British National Bibliography');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('BNF', 'Bibliothèque nationale de France');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('COPAC', 'UK/Irish union catalog');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('DNB', 'Deutsche Nationalbibliothek');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('FantLab', 'Laboratoria Fantastiki');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('Goodreads', 'Goodreads social cataloging site');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('JNB', 'The Japanese National Bibliography');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('LCCN', 'Library of Congress Control Number');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('NDL', 'National Diet Library');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('OCLC/WorldCat', 'Online Computer Library Center');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('Open Library', 'Open Library');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('SFBG', 'Catalog of books published in Bulgaria');

INSERT INTO identifier_types (identifier_type_name, identifier_type_full_name)
VALUES ('BN', 'Barnes and Noble');


INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 1, 'https://www.amazon.ca/dp/%s', 'CA');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 2, 'https://www.amazon.de/dp/%s', 'DE');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 3, 'https://www.amazon.fr/dp/%s', 'FR');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 4, 'https://www.amazon.co.jp/dp/%s', 'JP');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 5, 'https://www.amazon.co.uk/dp/%s', 'UK');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (1, 6, 'https://www.amazon.com/dp/%s', 'US');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (2, 1,
'http://explore.bl.uk/primo_library/libweb/action/dlDisplay.do?vid=BLVU1&amp;docId=BLL01%s');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (3, 1,
'http://search.bl.uk/primo_library/libweb/action/dlSearch.do?vid=BLBNB&amp;institution=BL&amp;query=any,exact,%s');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (4, 1, 'http://catalogue.bnf.fr/ark:/12148/%s');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (5, 1, 'http://copac.jisc.ac.uk/id/%s?style=html', 'Web view');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url, site_name)
VALUES (5, 2, 'http://copac.jisc.ac.uk/id/%s', 'XML view');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (6, 1, 'http://d-nb.info/%s');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (7, 1, 'https://fantlab.ru/edition%s');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (8, 1, 'http://www.goodreads.com/book/show/%s');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (9, 1, 'https://iss.ndl.go.jp/api/openurl?ndl_jpno=%s&amp;locale=en');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (10, 1, 'http://lccn.loc.gov/%s');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (11, 1, 'http://id.ndl.go.jp/bib/%s/eng');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (12, 1, 'http://www.worldcat.org/oclc/%s');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (13, 1, 'https://openlibrary.org/books/%s');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (14, 1, 'http://www.sfbg.us/book/%s');

INSERT INTO identifier_sites (identifier_type_id, site_position, site_url)
VALUES (15, 1, 'http://www.barnesandnoble.com/s/%s');

