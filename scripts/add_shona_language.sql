/* 
   add_shona_language.sql is a MySQL script intended to add Shona to the list of recognized languages. 

   Version: $Revision: 15 $
   Date:    $Date: 2018-09-05 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2018 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO languages (lang_id, lang_code, lang_name) VALUES (114, 'sna','Shona');
