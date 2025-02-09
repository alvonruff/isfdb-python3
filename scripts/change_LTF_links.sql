/* 
   change_LTF_links.sql is a MySQL script intended to rename LTF links


   Version: $Revision: 418 $
   Date:    $Date: 2021-09-16 10:10:07 -0400 (Thu, 16 Sep 2021) $

  (C) COPYRIGHT 2021 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE identifier_sites SET site_url = 'https://tercerafundacion.net/biblioteca/ver/libro/%s' where site_url like '%tercerafunda%';
