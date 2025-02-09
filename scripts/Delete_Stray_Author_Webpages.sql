/* 
   Delete_Stray_Author_Webpage.sql is a MySQL script intended to 
   remove author webpages left behind when the author was deleted.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2013   Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

delete from webpages 
where author_id is not null
and not exists (
	select 1 from authors a
	where a.author_id = webpages.author_id);

