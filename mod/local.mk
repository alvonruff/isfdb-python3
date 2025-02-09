#
#     (C) COPYRIGHT 2005-2023   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1139 $
#     Date: $Date: 2023-07-12 18:51:22 -0400 (Wed, 12 Jul 2023) $


include .TARGETS
include ../INSTALLDIRS

INSTALL = $(INSTALL_CGI)/mod

MYLIBS	= common.py \
	  isfdblib.py

LIBS	= authorClass.py \
	  awardClass.py \
	  awardcatClass.py \
	  awardtypeClass.py \
	  pubClass.py \
	  recognizeddomainClass.py \
	  seriesClass.py \
	  publisherClass.py \
	  pubseriesClass.py \
	  titleClass.py \
	  templateClass.py \
	  verificationsourceClass.py \
	  isbn.py \
	  isfdb.py \
	  library.py \
	  navbar.py \
	  viewers.py \
	  login.py \
	  SQLparsing.py

all:	$(TARGETS)
	cp $(MYLIBS) local
	cp $(LIBS) local

local/%.cgi:	%.py
		python install.py $* local /usr/bin/python

check_dirs:
		if test -d $(INSTALL); \
		then echo $(INSTALL) exists; \
		else mkdir $(INSTALL); \
		fi

install:	all check_dirs
		cp local/* $(INSTALL)
		chmod 755 $(INSTALL)/*.cgi
		chmod 644 $(INSTALL)/*.py

clean:
	rm -f local/*.cgi
	rm -f local/*.pyc

clobber:
	rm -f $(LIBS)
	rm -rf local

