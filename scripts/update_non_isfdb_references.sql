/* 
   update_non_isfdb_references.sql is a MySQL script intended to
   update non-ISFDB references which poin to third-party sites

   Version: $Revision: 1 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2021 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update reference set reference_url='http://www.isfdb.org/wiki/index.php/Reference:Locus1' where reference_label='Locus1';

update reference set reference_url='http://www.isfdb.org/wiki/index.php/Reference:Contento1' where reference_label='Contento1 (anth/coll)';
