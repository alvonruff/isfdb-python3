/* 
   Merge_Award_Categories is a MySQL script intended to reduce the number of 
   duplicate award categories before we move them to their own table.

   Version: $Revision: 1.2 $
   Date:    $Date: 2013/05/12 07:51:33 $

  (C) COPYRIGHT 2013   Bill Longley and Ahasuerus
      ALL RIGHTS RESERVED

  The copyright notice above does not evidence any actual or
  intended publication of such source code.
*/

update awards
set award_atype	= 'Children\'s (8-12 years) Long Fiction'
where award_ttype = 'As'	
and (award_atype = 'Children\'s (8-12) Long Fiction'
 or  award_atype = 'Childrens (8-12 years) Long Fiction');
 
update awards
set award_atype	= 'Children\'s (8-12 years) Short Fiction'
where award_ttype = 'As'	
and (award_atype = 'Children\'s (8-12) Short Fiction'
 or  award_atype = 'Childrens (8-12 years) Short Fiction');
 
update awards
set award_atype	= 'Peter McNamara Convenors\' Award for Excellence'
where award_ttype = 'As'	
and (award_atype = 'PETER McNAMARA CONVENORS\' AWARD'
 or  award_atype = 'Peter McNamara Conveners\' Award for Excellence');
 
update awards
set award_atype	= 'SF Novel'
where award_ttype = 'As'	
and (award_atype = 'SCIENCE FICTION NOVEL');
  
update awards
set award_atype	= 'SF Short Story'
where award_ttype = 'As'	
and (award_atype = 'SCIENCE FICTION SHORT STORY');
  
update awards
set award_atype	= 'William Atheling Jr. Award for Criticism or Review'
where award_ttype = 'At'	
and (award_atype = 'William Atheling Jr Award for Criticism or Review');
  
update awards
set award_atype	= 'The PS Publishing Best Small Press Award'
where award_ttype = 'Bf'	
and (award_atype = 'The PS Publishing Best Small Press Award:');
  
update awards
set award_atype	= 'Ray Bradbury Award'
where award_ttype = 'Br'	
and (award_atype = 'Bradbury Award (President\'s Award for Dramatic Presentation)'
 or  award_atype = 'Ray Bradbury Award for Dramatic Screenwriting'); 
 
update awards
set award_atype	= 'Artwork'
where award_ttype = 'Bs'	
and (award_atype = 'Art work');
 
update awards
set award_atype	= 'Nonfiction'
where award_ttype = 'Bs'	
and (award_atype = 'Non-Fiction'); 
  
update awards
set award_atype	= 'Best Cover Illustration - Hardcover'
where award_ttype = 'Cy'	
and (award_atype = 'Best Cover Illustration - Hardback Book' 
 or award_atype = 'Best Hardback Cover');
  
update awards
set award_atype	= 'Best Cover Illustration - Paperback'
where award_ttype = 'Cy'	
and (award_atype = 'Best Cover Illustration - Paperback Book'
 or award_atype = 'Best Paperback Cover');
  
update awards
set award_atype	= 'Best Gaming-Related Illustration'
where award_ttype = 'Cy'	
and (award_atype = 'Best Gaming and Related Illustration');
  
update awards
set award_atype	= 'Best Unpublished Illustration - Monochrome'
where award_ttype = 'Cy'	
and (award_atype = 'Best Unpublished Monochrome');
  
update awards
set award_atype	= 'Best Unpublished Illustration - Color'
where award_ttype = 'Cy'	
and (award_atype = 'Best Unpublished Color');
  
update awards
set award_atype	= 'Best Australian Fan Writer'
where award_ttype = 'Dt'	
and (award_atype = 'Best Australian Fanwriter');
  
update awards
set award_atype	= 'Best Dramatic Presentation: Long Form'
where award_ttype = 'Hu'	
and (award_atype = 'Best Dramatic Presentation, Long Form');
  
update awards
set award_atype	= 'Best Dramatic Presentation: Short Form'
where award_ttype = 'Hu'	
and (award_atype = 'Best Dramatic Presentation, Short Form');
  
update awards
set award_atype	= 'Living Legend Award'
where award_ttype = 'Ih'	
and (award_atype = 'Living Legend');

update awards
set award_atype	= 'Best New Writer'
where award_ttype = 'Jc';

update awards
set award_atype	= 'Best Non-Fiction'
where award_ttype = 'Lc'	
and (award_atype = 'Best Non-Fiction Book');

update awards
set award_atype	= 'Best Publisher - hardcover'
where award_ttype = 'Lc'	
and (award_atype = 'Best Publisher - hardbound');

update awards
set award_atype	= 'Best SF Novel'
where award_ttype = 'Lc'	
and (award_atype = 'Best Science Fiction Novel');

update awards
set award_atype	= 'Lesbian and Gay Science Fiction, Fantasy and Horror'
where award_ttype = 'Lm'	
and (award_atype = 'Lesbian and Gay Science Fiction, Fantasy & Horror');

update awards
set award_atype	= 'Mythopoeic Fantasy Award for Children\'s Literature'
where award_ttype = 'My'	
and (award_atype = 'Mythopoeic Fantasy Award for Childrens Literature');

update awards
set award_atype	= 'Special Award, Non-Professional'
where award_ttype = 'Wf'
and (award_atype = 'Special Award (Non-Pro)');

update awards
set award_atype	= 'Special Award, Professional'
where award_ttype = 'Wf'
and (award_atype = 'Special Award (Pro)');


