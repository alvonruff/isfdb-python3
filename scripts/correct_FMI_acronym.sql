/* 
   correct_FMI_acronym.sql is a MySQL script intended to change the acronym of
   The FictionMags Index External ID Type from "FIM" to "FMI"
	

   Version: $Revision: 418 $
   Date:    $Date: 2024-11-23 10:10:07 -0400 (Sat, 23 Nov 2024) $

  (C) COPYRIGHT 2024 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


UPDATE identifier_types set identifier_type_name = 'FMI' where identifier_type_name = 'FIM';

