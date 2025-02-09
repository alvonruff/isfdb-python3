/* 
   update_BLIC.sql is a MySQL script intended to update the ISBN
   linking logic for the British Library Catalogue

   Version: $Revision: 1.1 $
   Date:    $Date: 2017/06/14 22:26:12 $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE websites SET site_url =
'http://explore.bl.uk/primo_library/libweb/action/search.do?fn=search&vl(freeText0)=%s'
where site_name='British Library';
