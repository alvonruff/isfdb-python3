#
#     (C) COPYRIGHT 2005-2025   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 12 $
#     Date: $Date: 2017-10-30 18:32:28 -0400 (Mon, 30 Oct 2017) $

include INSTALLDIRS

INSTALL = $(INSTALL_CGI)
PYTHON2 = /usr/bin/python
PYTHON3 = /usr/bin/python3

install:
	mv common/localdefs.py common/localdefs2.py
	cp $(INSTALL)/localdefs.py common
	cd common && $(MAKE) install;
	mv common/localdefs2.py common/localdefs.py
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
	cd nightly && $(MAKE) clean;
	rm -f .pythonver

export:
		/bin/bash export.sh

python2:
	echo $(PYTHON2) > .pythonver
	mv common/localdefs.py common/localdefs2.py
	cp $(INSTALL)/localdefs.py common
	cd common && python setver.py 2;
	cp common/localdefs.py $(INSTALL)
	mv common/localdefs2.py common/localdefs.py
	echo "Now using Python2"

python3:
	echo $(PYTHON3) > .pythonver
	mv common/localdefs.py common/localdefs2.py
	cp $(INSTALL)/localdefs.py common
	cd common && python setver.py 3;
	cp common/localdefs.py $(INSTALL)
	mv common/localdefs2.py common/localdefs.py
	echo "Now using Python3"
