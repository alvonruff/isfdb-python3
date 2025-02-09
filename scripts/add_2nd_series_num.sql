/* 
   add_2nd_series_num.sql is a MySQL script intended to
   alter table "titles" to add field title_seriesnum_2
   In addition, it changes the values of the series_id and
   title_seriesnum fields from 0 to NULL to correct
   title records which were previously affected by a
   bug in the Title Merge code

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

UPDATE titles SET series_id=NULL WHERE series_id=0;
UPDATE titles SET title_seriesnum=NULL WHERE title_seriesnum=0;
ALTER TABLE titles ADD COLUMN title_seriesnum_2 VARCHAR(4);