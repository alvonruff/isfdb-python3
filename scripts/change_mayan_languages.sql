/* 
   change_mayan_languages.sql is a MySQL script intended to change
   the spelling of 'Mayan languages' to 'Mayan languages'

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2018 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE languages set lang_name='Mayan language' where lang_name='Mayan languages';
