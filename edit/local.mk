#
#     (C) COPYRIGHT 2005-2026   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1256 $
#     Date: $Date: 2026-02-11 08:03:50 -0500 (Wed, 11 Feb 2026) $


include .TARGETS
include ../INSTALLDIRS

INSTALL = $(INSTALL_CGI)/edit
VERSION = $(shell cat ../.pythonver)


MYLIBS	= cleanup_lib.py \
	  isfdblib.py \
	  isfdblib_help.py \
	  isfdblib_print.py

LIBS	= authorClass.py \
	  awardClass.py \
	  awardcatClass.py \
	  awardtypeClass.py \
	  recognizeddomainClass.py \
	  titleClass.py \
	  pubClass.py \
	  publisherClass.py \
	  pubseriesClass.py \
	  seriesClass.py \
	  templateClass.py \
	  verificationsourceClass.py \
	  isbn.py \
	  library.py \
	  navbar.py \
	  viewers.py \
	  login.py \
	  SQLparsing.py \
	  isfdb.py \
	  sfe3.py

all:	$(TARGETS)
	cp $(MYLIBS) local
	cp $(LIBS) local

local/%.cgi:	%.py
		python install.py $* local $(VERSION)

check_dirs:
		if test -d $(INSTALL); \
		then echo $(INSTALL) exists; \
		else mkdir $(INSTALL); \
		fi

install:	all check_dirs
		rm -f $(INSTALL)/*.pyc
		cp local/* $(INSTALL)
		chmod 755 $(INSTALL)/*.cgi
		chmod 644 $(INSTALL)/*.py

clean:
	rm -f local/*.cgi
	rm -f local/*.pyc

clobber:
	rm -f $(LIBS)
	rm -rf local

