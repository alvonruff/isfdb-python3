/* 
   update_NILF_full_name.sql is a MySQL script intended to update of the NILF
   external idenifier type to include 'Fantascienza'
	

   Version: $Revision: 15 $
   Date:    $Date: 2018-06-13 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2019 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/


UPDATE identifier_types set identifier_type_full_name = 'Numero Identificativo della Letteratura Fantastica / Fantascienza' where identifier_type_name = 'NILF';
