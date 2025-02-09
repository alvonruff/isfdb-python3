/* 
   add_3_ISO_languages.sql is a MySQL script intended to add
   3 ISO 639-2 languages: South American Indian language (sai),
   Interlingua (ina) and Guarani (grn) to ISFDB

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2019 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO languages (lang_id, lang_code, lang_name) VALUES (152, 'sai', 'South American Indian language');
INSERT INTO languages (lang_id, lang_code, lang_name) VALUES (153, 'ina', 'Interlingua');
INSERT INTO languages (lang_id, lang_code, lang_name) VALUES (154, 'grn', 'Guarani');
