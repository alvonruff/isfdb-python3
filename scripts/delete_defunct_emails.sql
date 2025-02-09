/* 
   delete_defunct_emails.sql is a MySQL script intended to
   delete authors' e-mail addresses for previously deleted
   authors.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
delete from emails where not exists (select 1 from authors where authors.author_id=emails.author_id);
	
