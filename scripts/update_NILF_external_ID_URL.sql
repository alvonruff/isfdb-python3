/* 
   update_NILF_external_ID_URL.sql is a MySQL script intended to
   update the  a new external idenifier type
	

   Version: $Revision: 15 $
   Date:    $Date: 2018-05-18 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2022 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE identifier_sites SET site_url = 'https://www.fantascienza.com/catalogo/volumi/NILF%s' where site_url = 'http://nilf.it/%s/';

