/* 
   add_apostrophe_to_directory.sql is a MySQL script intended to
   add a new "letter" to the directory table to cover an apostrophe as
   second letter in the author last name.

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2011 Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
UPDATE directory 
SET directory_mask = directory_mask + 67108864
WHERE directory_INDEX IN (
SELECT DISTINCT Substr(author_lastname,1,1)
from authors
WHERE SUBSTR(author_lastname,2,1) = "'"
)
AND directory_mask < 67108864
