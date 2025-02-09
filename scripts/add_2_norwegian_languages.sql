/* 
   add_2_norwegian_languages.sql is a MySQL script intended to add
   2 Norweian languages - Norwegian (Bokmål) and Norwegian (Nynorsk) -
   to ISFDB

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO languages (lang_id, lang_code, lang_name) VALUES (107, 'nob','Norwegian (Bokmal)');
INSERT INTO languages (lang_id, lang_code, lang_name) VALUES (108, 'nno','Norwegian (Nynorsk)');
