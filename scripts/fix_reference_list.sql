/* 
   fix_reference_list.sql is a MySQL script intended to clean up
   Currey and Primary (Transient) so that their reference IDs match 
   their position in the list. It is only supposed to be run ONCE 
   so protection against "fixing" them again is built in.

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2009   Bill Longley on behalf of ISFDB.
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/
update reference 
set reference_id = 11 
where reference_id = 13
and   reference_label = 'Currey';

update reference 
set reference_id = 12 
where reference_id = 17
and   reference_label = 'Primary (Transient)';