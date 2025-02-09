/* 
   add_dnb.sql is a MySQL script intended to add Deutsche Nationalbibliothek 
   as another "Other Sites" option. 

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2011 Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

INSERT INTO websites (site_id, site_name, site_url)
VALUES (22,'Deutsche Nationalbibliothek','https://portal.d-nb.de/opac.htm?query=%s&method=simpleSearch');
