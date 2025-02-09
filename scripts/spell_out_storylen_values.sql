/* 
   empty_storylen_in_titles.sql is a MySQL script intended to
   spell out the storylen values in the titles table

   Version: $Revision: 1.1 $
   Date:    $Date: 2017/01/24 00:43:31 $

  (C) COPYRIGHT 2017 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update titles set title_storylen = 'short story' where title_storylen = 'ss';

update titles set title_storylen = 'novella' where title_storylen = 'nv';

update titles set title_storylen = 'novelette' where title_storylen = 'nt';
