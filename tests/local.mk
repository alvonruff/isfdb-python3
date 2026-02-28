#
#     (C) COPYRIGHT 2026   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1256 $
#     Date: $Date: 2026-02-11 08:03:50 -0500 (Wed, 11 Feb 2026) $

VERSION = $(shell cat ../.pythonver)

NOT_TESTS = authorClass.py \
	awardcatClass.py \
	awardClass.py \
	awardtypeClass.py \
	install.py \
	isbn.py \
	isfdb.py \
	library.py \
	localdefs.py \
	login.py \
	navbar.py \
	pubClass.py \
	publisherClass.py \
	pubseriesClass.py \
	pylintrc \
	recognizeddomainClass.py \
	seriesClass.py \
	sfe3.py \
	SQLparsing.py \
	templateClass.py \
	titleClass.py \
	verificationsourceClass.py \
	viewers.py

clean:
	rm -f local/*.cgi
	rm -f local/*.pyc
	rm -f $(NOT_TESTS)

clobber:
	rm -f $(NOT_TESTS)
