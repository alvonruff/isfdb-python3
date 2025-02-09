/* 
   change_serbian_language.sql is a MySQL script intended to
   change the value of the latin_script field for the
   Serbian language from "No" to "Yes". Modern Serbian uses
   both Latin and Cyrillic.

   Version: $Revision: 418 $
   Date:    $Date: 2020-07-20 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2020 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE tags set tag_name = 'juvenile horror' where tag_name = 'Juvenile horror';
