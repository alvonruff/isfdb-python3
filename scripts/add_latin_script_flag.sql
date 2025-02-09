/* 
   add_latin_script_flag.sql is a MySQL script intended to
   alter table langiages" to add field latin_script

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2015 Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

ALTER TABLE languages ADD COLUMN latin_script ENUM('Yes', 'No');

update languages set latin_script='No' where lang_name in
                 ('Ancient Greek',
                 'Arabic',
                 'Armenian',
                 'Belarusian',
                 'Bengali',
                 'Bulgarian',
                 'Burmese',
                 'Chinese',
                 'Georgian',
                 'Greek',
                 'Gujarati',
                 'Hebrew',
                 'Hindi',
                 'Japanese',
                 'Kazakh',
                 'Khmer',
                 'Kyrgyz',
                 'Korean',
                 'Macedonian',
                 'Malayalam',
                 'Marathi',
                 'Mongolian',
                 'Persian',
                 'Russian',
                 'Serbian',
                 'Sinhalese',
                 'Tajik',
                 'Tamil',
                 'Thai',
                 'Tibetan',
                 'Ukrainian',
                 'Urdu',
                 'Vietnamese',
                 'Yiddish',
                 'Amharic',
                 'Judeo-Arabic',
                 'Karen',
                 'Panjabi',
                 'Somali',
                 'Sundanese',
                 'Telugu',
                 'Uighur',
                 'Sanskrit',
                 'Serbo-Croatian Cyrillic'
                 );
