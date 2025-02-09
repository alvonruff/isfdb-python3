/* 
   add_award_cat_order.sql is a MySQL script intended to
   alter table "award_cats" to add field award_cat_order
   and add default ordering values

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2014 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE award_cats ADD COLUMN award_cat_order INT(11);
UPDATE award_cats SET award_cat_order = 1 WHERE award_cat_name = 'Best Novel';
UPDATE award_cats SET award_cat_order = 2 WHERE award_cat_name = 'Novel';
UPDATE award_cats SET award_cat_order = 3 WHERE award_cat_name = 'Superior Achievement in a Novel';
UPDATE award_cats SET award_cat_order = 4 WHERE award_cat_name = 'SF Novel';
UPDATE award_cats SET award_cat_order = 5 WHERE award_cat_name = 'Best SF Novel';
UPDATE award_cats SET award_cat_order = 6 WHERE award_cat_name = 'Best Fantasy Novel';
UPDATE award_cats SET award_cat_order = 7 WHERE award_cat_name = 'Fantasy Novel';
UPDATE award_cats SET award_cat_order = 8 WHERE award_cat_name = 'Best Horror Novel';
UPDATE award_cats SET award_cat_order = 9 WHERE award_cat_name = 'Horror Novel';
UPDATE award_cats SET award_cat_order = 10 WHERE award_cat_name = 'Best Horror/Dark Fantasy Novel';
UPDATE award_cats SET award_cat_order = 11 WHERE award_cat_name = 'Best First Novel';
UPDATE award_cats SET award_cat_order = 12 WHERE award_cat_name = 'First Novel';
UPDATE award_cats SET award_cat_order = 13 WHERE award_cat_name = 'Superior Achievement in a First Novel';
UPDATE award_cats SET award_cat_order = 14 WHERE award_cat_name = 'Best Young Adult Novel';
UPDATE award_cats SET award_cat_order = 15 WHERE award_cat_name = 'Novella';
UPDATE award_cats SET award_cat_order = 16 WHERE award_cat_name = 'Best Novella';
UPDATE award_cats SET award_cat_order = 17 WHERE award_cat_name = 'Superior Achievement in Long Fiction';
UPDATE award_cats SET award_cat_order = 18 WHERE award_cat_name = 'Best Novella/Novelette';
UPDATE award_cats SET award_cat_order = 19 WHERE award_cat_name = 'Novelette';
UPDATE award_cats SET award_cat_order = 20 WHERE award_cat_name = 'Best Novelette';
UPDATE award_cats SET award_cat_order = 21 WHERE award_cat_name = 'Short Fiction';
UPDATE award_cats SET award_cat_order = 22 WHERE award_cat_name = 'Best Short Fiction';
UPDATE award_cats SET award_cat_order = 23 WHERE award_cat_name = 'Superior Achievement in Short Fiction';
UPDATE award_cats SET award_cat_order = 24 WHERE award_cat_name = 'Short Story';
UPDATE award_cats SET award_cat_order = 25 WHERE award_cat_name = 'Best Short Story';
UPDATE award_cats SET award_cat_order = 26 WHERE award_cat_name = 'Best Collection';
UPDATE award_cats SET award_cat_order = 27 WHERE award_cat_name = 'Superior Achievement in a Fiction Collection';
UPDATE award_cats SET award_cat_order = 28 WHERE award_cat_name = 'Best Anthology';
UPDATE award_cats SET award_cat_order = 29 WHERE award_cat_name = 'Superior Achievement in an Anthology';
UPDATE award_cats SET award_cat_order = 30 WHERE award_cat_name = 'Best Non-Fiction';
UPDATE award_cats SET award_cat_order = 31 WHERE award_cat_name = 'Superior Achievement in Non-Fiction';
UPDATE award_cats SET award_cat_order = 32 WHERE award_cat_name = 'Best Art Book';
UPDATE award_cats SET award_cat_order = 33 WHERE award_cat_name = 'Best Editor';
UPDATE award_cats SET award_cat_order = 34 WHERE award_cat_name = 'Editor';
