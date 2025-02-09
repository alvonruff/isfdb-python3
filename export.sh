#!/bin/bash
#
#     (C) COPYRIGHT 2005-2008   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#
#     Version: $Revision: 12 $
#     Date: $Date: 2017-10-30 18:32:28 -0400 (Mon, 30 Oct 2017) $

set -x
#######################################
# Remove any old exported versions
#######################################
rm -f isfdb2.tar.gz
rm -rf isfdb2
mkdir isfdb2

#######################################
# Copy the common files and hide data
# in localdefs.py
#######################################
cp -r common isfdb2
echo HTMLLOC = \"xxx\" > isfdb2/common/localdefs.py
echo HTFAKE = \"xxx\" >> isfdb2/common/localdefs.py
echo DBASEHOST = \"xxx\" >> isfdb2/common/localdefs.py
echo HTMLHOST = \"xxx\" >> isfdb2/common/localdefs.py
echo COOKIEHOST = \"xxx\" >> isfdb2/common/localdefs.py
echo USERNAME = \"xxx\" >> isfdb2/common/localdefs.py
echo PASSWORD = \"xxx\" >> isfdb2/common/localdefs.py
echo DBASE = \"xxx\" >> isfdb2/common/localdefs.py
echo UNICODE = \"xxx\" >> isfdb2/common/localdefs.py
echo DO_ANALYTICS = 0 >> isfdb2/common/localdefs.py

cp INSTALLDIRS isfdb2

#######################################
# Copy the biblio files 
#######################################
cp -r biblio isfdb2
cd isfdb2/biblio && make clobber
cd -

#######################################
# Copy the edit files 
#######################################
cp -r edit isfdb2
cd isfdb2/edit && make clobber
cd -

#######################################
# Copy the mod files 
#######################################
cp -r mod isfdb2
cd isfdb2/mod && make clobber
cd -

#######################################
# Copy the rest files 
#######################################
cp -r rest isfdb2
cd isfdb2/rest && make clobber
cd -

rm -rf isfdb2/biblio/CVS
rm -rf isfdb2/edit/CVS
rm -rf isfdb2/mod/CVS
rm -rf isfdb2/common/CVS

#######################################
# Copy the CSS and script files 
#######################################
cp -r css isfdb2
cd isfdb2/css && make clobber
cd -
cp -r scripts isfdb2
cd isfdb2/scripts && make clobber
cd -

cp Makefile isfdb2
cp README isfdb2
cp LICENSE isfdb2

tar -cvf isfdb2.tar isfdb2
gzip isfdb2.tar
