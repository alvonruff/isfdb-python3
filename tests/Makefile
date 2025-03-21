#
#     (C) COPYRIGHT 2025   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 21 $
#     Date: $Date: 2017-10-31 19:57:53 -0400 (Tue, 31 Oct 2017) $

PYTHON = /usr/bin/python3

LOCAL:
	make -f local.mk 

install:

run:
	$(PYTHON) TEST_authorClass.py > LOG
	$(PYTHON) TEST_awardcatClass.py >> LOG
	$(PYTHON) TEST_awardClass.py >> LOG
	$(PYTHON) TEST_awardtypeClass.py >> LOG
	$(PYTHON) TEST_pubClass.py >> LOG

clean:
	make -f local.mk clean
	rm -f *.cgi
	rm -f *.pyc

clobber:
	make -f local.mk clobber
	rm -f *.cgi
	rm -f *.pyc

