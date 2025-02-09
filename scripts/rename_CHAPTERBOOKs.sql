/* 
   rename_CHAPTERBOOKs.sql is a MySQL script intended to
   alter tables titles and pubs. We will change the
   enumerated value of CHAPTERBOOK to CHAPBOOK in the
   definition of column pub_ctype in table pubs and
   column title_ttype in table titles

   Version: $Revision: 1.2 $
   Date:    $Date: 2015/02/13 05:06:35 $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE titles CHANGE title_ttype title_ttype ENUM('ANTHOLOGY','BACKCOVERART',
'COLLECTION','COVERART','INTERIORART','EDITOR','ESSAY','INTERVIEW','NOVEL','NONFICTION',
'OMNIBUS','POEM','REVIEW','SERIAL','SHORTFICTION','CHAPTERBOOK', 'CHAPBOOK');

UPDATE titles set title_ttype = 'CHAPBOOK' where title_ttype = 'CHAPTERBOOK';

ALTER TABLE titles CHANGE title_ttype title_ttype ENUM('ANTHOLOGY','BACKCOVERART',
'COLLECTION','COVERART','INTERIORART','EDITOR','ESSAY','INTERVIEW','NOVEL','NONFICTION',
'OMNIBUS','POEM','REVIEW','SERIAL','SHORTFICTION','CHAPBOOK');

ALTER TABLE pubs CHANGE pub_ctype pub_ctype ENUM('ANTHOLOGY','CHAPTERBOOK','COLLECTION',
'MAGAZINE','NONFICTION','NOVEL','OMNIBUS','FANZINE','CHAPBOOK');

UPDATE pubs set pub_ctype = 'CHAPBOOK' where pub_ctype = 'CHAPTERBOOK';

ALTER TABLE pubs CHANGE pub_ctype pub_ctype ENUM('ANTHOLOGY','COLLECTION',
'MAGAZINE','NONFICTION','NOVEL','OMNIBUS','FANZINE','CHAPBOOK');
