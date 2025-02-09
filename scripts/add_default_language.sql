/* 
   add_default_language.sql is a MySQL script intended to add a new
   column to user_preferences to let a user indicate a default language

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2011 Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE user_preferences
ADD default_language INT(11) AFTER display_all_languages;
