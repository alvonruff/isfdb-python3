/* 
   change_JNB.sql is a MySQL script intended to
   change the JNB identifier type to "JNB/JPNO".

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update identifier_types set identifier_type_name = 'JNB/JPNO' where identifier_type_name = 'JNB';
