/* 
   rename_Australian_National_Library_ID is a MySQL script intended to
   rename the "Australian National Library" external idenifier
	

   Version: $Revision: 418 $
   Date:    $Date: 2019-12-02 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2019 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


UPDATE identifier_types set identifier_type_name = 'NLA' where identifier_type_id = 28;

UPDATE identifier_types set identifier_type_full_name = 'National Library of Australia' where identifier_type_id = 28;

