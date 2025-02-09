/* 
   dedup_tag_mappings.sql is a MySQL script intended to remove 
   semi-duplicates (differ by leading space only) from the tag_mappings table.

   Version: $Revision: 418 $
   Date:    $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $

  (C) COPYRIGHT 2013   Bill Longley
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

-- tag_name alien artifact	
UPDATE tag_mapping
set tag_id = 1061	
where tag_id = 3137;
delete from tags where tag_id = 3137;

-- tag_name exploration	
UPDATE tag_mapping
set tag_id = 1241	
where tag_id = 3134;
delete from tags where tag_id = 3134;

-- tag_name fantasy	
UPDATE tag_mapping
set tag_id = 51	
where tag_id = 3132;
delete from tags where tag_id = 3132;

-- tag_name far future	
UPDATE tag_mapping
set tag_id = 241
where tag_id = 3133;
delete from tags where tag_id = 3133;

-- tag_name female main character	
UPDATE tag_mapping
set tag_id = 2357	
where tag_id = 3107;
delete from tags where tag_id = 3107;

-- tag_name first contact	
UPDATE tag_mapping
set tag_id = 461
where tag_id = 2877;
delete from tags where tag_id = 2877;

-- tag_name genetic engineering	
UPDATE tag_mapping
set tag_id = 1511	
where tag_id = 6109;
delete from tags where tag_id = 6109;

-- tag_name juvenile	
UPDATE tag_mapping
set tag_id = 2657	
where tag_id = 6143;
delete from tags where tag_id = 6143;

-- tag_name juvenile ghost story	
UPDATE tag_mapping
set tag_id = 5485	
where tag_id = 6118;
delete from tags where tag_id = 6118;

-- tag_name military sf	
UPDATE tag_mapping
set tag_id = 141	
where tag_id = 3157;
delete from tags where tag_id = 3157;

-- tag_name Regency England	
UPDATE tag_mapping
set tag_id = 5482	
where tag_id = 5483;
delete from tags where tag_id = 5483;

-- tag_name science fiction	
UPDATE tag_mapping
set tag_id = 31	
where tag_id = 3302;
delete from tags where tag_id = 3302;

-- tag_name Space Travel	
UPDATE tag_mapping
set tag_id = 5082
where tag_id = 3396;
delete from tags where tag_id = 3396;

-- tag_name strong female characters	
UPDATE tag_mapping
set tag_id = 2157	
where tag_id = 3131;
delete from tags where tag_id = 3131;

-- tag_name time travel	
UPDATE tag_mapping
set tag_id = 71	
where tag_id = 3138;
delete from tags where tag_id = 3138;

-- tag_name young-adult sf	
UPDATE tag_mapping
set tag_id = 231	
where tag_id = 2881;
delete from tags where tag_id = 2881;

