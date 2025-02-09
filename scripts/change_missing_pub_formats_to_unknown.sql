/* 
   change_missing_pub_formats_to_unknown.sql is a MySQL script intended to
   change empty or NULL publication format values to 'unknown'

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014   Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update pubs set pub_ptype='unknown' where pub_ptype IS NULL or pub_ptype='';
