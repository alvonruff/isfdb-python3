/* 
   add_title_non_genre_flag.sql is a MySQL script intended to
   alter table "titles" to add field title_non_genre

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE titles ADD COLUMN title_non_genre ENUM('Yes', 'No');
UPDATE titles set title_non_genre = 'Yes' where title_ttype = 'NONGENRE';
UPDATE titles set title_ttype = 'NOVEL' where title_ttype = 'NONGENRE';
ALTER TABLE titles CHANGE title_ttype title_ttype ENUM('ANTHOLOGY','BACKCOVERART',
'COLLECTION','COVERART','INTERIORART','EDITOR','ESSAY','INTERVIEW','NOVEL','NONFICTION',
'OMNIBUS','POEM','REVIEW','SERIAL','SHORTFICTION','CHAPTERBOOK');
