/* 
   split_storylen_field.sql is a MySQL script intended to split
   the storylen field in the titles table into 4 fields. See
   FR 163 for details.

   Version: $Revision: 1.1 $
   Date:    $Date: 2017/01/16 23:19:35 $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE titles ADD title_nvz enum('Yes','No') DEFAULT 'No';

ALTER TABLE titles ADD title_jvn enum('Yes','No') DEFAULT 'No';

ALTER TABLE titles ADD title_content varchar(32);

update titles set title_nvz = 'Yes' where title_storylen = 'nvz';

update titles set title_jvn = 'Yes' where title_storylen = 'jvn';

update titles set title_content = SUBSTRING(title_storylen,2,30) where SUBSTRING(title_storylen,1,1) = '/';

update titles set title_storylen = NULL where title_storylen = 'nvz' or title_storylen = 'jvn';

update titles set title_storylen = NULL where SUBSTRING(title_storylen,1,1) = '/';
