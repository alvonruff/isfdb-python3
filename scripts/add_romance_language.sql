/* 
   add_romance_language.sql is a MySQL script intended to add
   'Romance language' to ISFDB. The code will be used for titles written
   using Romance dialects and minor languages which are not explicitly
   listed in ISO 639-2.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2019 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO languages (lang_id, lang_code, lang_name) VALUES (156, 'roa', 'Romance language');
