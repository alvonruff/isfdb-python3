/* 
   insert_reference.sql is a MySQL script intended to add
   new reference sources to the reference list. This version will 
   add Bleiler78, OCLC and some extra Primary verification options.

   Note that Currey and Primary (Transient) are expected to have been 
   fixed first (via scripts/fix_reference_list.sql 1.1).

   It is only supposed to be run ONCE so protection against 
   inserting duplicates is built in. Note when creating new versions
   that you will have to keep the reference IDs in step in each insert,
   and do not attempt to create reference_ids that already exist.

   Version: $Revision: 15 $
   Date:    $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

  (C) COPYRIGHT 2009   Bill Longley on behalf of ISFDB.
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

insert into reference
( reference_id
, reference_label
, reference_fullname
, reference_url)
select 
'13'
, 'Bleiler78'
, 'The Checklist of Science-Fiction and Supernatural Fiction'
, 'http://www.isfdb.org/wiki/index.php/Reference:Bleiler78'
from reference
where not exists (select 1 from reference 
                  where reference_id = 13)
LIMIT 1;

insert into reference
( reference_id
, reference_label
, reference_fullname
, reference_url)
select 
'14'
, 'OCLC/Worldcat'
, 'OCLC/Worldcat'
, 'http://www.isfdb.org/wiki/index.php/Help:Using_Worldcat_data'
from reference
where not exists (select 1 from reference 
                  where reference_id = 14)
LIMIT 1;

insert into reference
( reference_id
, reference_label
, reference_fullname
)
select'15'
, 'Primary2'
, 'The actual book or magazine - but you are the second person to verify'
from reference
where not exists (select 1 from reference 
                  where reference_id = 15)
LIMIT 1;

insert into reference
( reference_id
, reference_label
, reference_fullname
)
select'16'
, 'Primary3'
, 'The actual book or magazine - but you are the third person to verify'
from reference
where not exists (select 1 from reference 
                  where reference_id = 16)
LIMIT 1;

insert into reference
( reference_id
, reference_label
, reference_fullname
)
select'17'
, 'Primary4'
, 'The actual book or magazine - but you are the fourth person to verify'
from reference
where not exists (select 1 from reference 
                  where reference_id = 17)
LIMIT 1;


insert into reference
( reference_id
, reference_label
, reference_fullname
)
select'18'
, 'Primary5'
, 'The actual book or magazine - but you are the fifth person to verify'
from reference
where not exists (select 1 from reference 
                  where reference_id = 18)
LIMIT 1;
