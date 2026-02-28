#
#     (C) COPYRIGHT 2005-2026   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1265 $
#     Date: $Date: 2026-02-25 07:25:05 -0500 (Wed, 25 Feb 2026) $

PYTHON2 = /usr/bin/python
PYTHON3 = /usr/bin/python3

install:
	cd common && $(MAKE) install;
	cd biblio && $(MAKE) LOCAL;
	cd biblio && $(MAKE) install;
	cd edit   && $(MAKE) LOCAL;
	cd edit   && $(MAKE) install;
	cd mod    && $(MAKE) LOCAL;
	cd mod    && $(MAKE) install;
	cd nightly && $(MAKE) LOCAL;
	cd nightly && $(MAKE) install;
	cd css    && $(MAKE) install;
	cd rest   && $(MAKE) LOCAL;
	cd rest   && $(MAKE) install;

clean:
	cd common && $(MAKE) clean;
	cd biblio && $(MAKE) clean;
	cd edit && $(MAKE) clean;
	cd mod && $(MAKE) clean;
	cd css && $(MAKE) clean;
	cd rest && $(MAKE) clean;
	cd tests && $(MAKE) clean;

export:
	/bin/bash export.sh

#
#   Use: "make python2" to switch to python2
#   Use: "make python3" to switch to python3
#
#   Switching the python major version requires:
#
#         "make clean"
#         "make -B install"
#
#   after the switch to rebuild the cgi files
#

python2:
	echo $(PYTHON2) > .pythonver
	echo "Now using Python2"

python3:
	echo $(PYTHON3) > .pythonver
	echo "Now using Python3"

