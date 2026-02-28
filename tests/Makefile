#
#     (C) COPYRIGHT 2026   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 21 $
#     Date: $Date: 2017-10-31 19:57:53 -0400 (Tue, 31 Oct 2017) $

#PYTHON = /usr/bin/python2
PYTHON = /usr/bin/python3

run:
	$(PYTHON) TEST_authorClass.py
	$(PYTHON) TEST_awardcatClass.py
	$(PYTHON) TEST_awardClass.py
	$(PYTHON) TEST_awardtypeClass.py
	$(PYTHON) TEST_isbn.py
	$(PYTHON) TEST_isfdb.py
	$(PYTHON) TEST_library.py
	$(PYTHON) TEST_navbar.py
	$(PYTHON) TEST_pubClass.py
	$(PYTHON) TEST_publisherClass.py
	$(PYTHON) TEST_pubseriesClass.py
	$(PYTHON) TEST_recognizeddomainClass.py
	$(PYTHON) TEST_seriesClass.py
	$(PYTHON) TEST_sfe3.py
	$(PYTHON) TEST_SQLparsing.py
	$(PYTHON) TEST_templateClass.py
	$(PYTHON) TEST_titleClass.py
	$(PYTHON) TEST_verificationsourceClass.py
	$(PYTHON) TEST_viewers.py

clean:
	make -f local.mk clean
	rm -f *.cgi
	rm -f *.pyc
	rm -f .TARGETS

clobber:
	make -f local.mk clobber
	rm -f *.cgi
	rm -f *.pyc

