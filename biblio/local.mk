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

INSTALL = $(INSTALL_CGI)
VERSION = $(shell cat ../.pythonver)

MYLIBS	= advSearchClass.py \
	  biblio.py \
	  calendarClass.py \
	  common.py \
	  isfdblib.py \
	  myverificationsClass.py \
	  utils.py

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
	 login.py \
	 SQLparsing.py \
	 isbn.py \
	 isfdb.py \
	 library.py \
	 navbar.py \
	 install.py \
	 viewers.py

all:	$(TARGETS)
	cp $(MYLIBS) local
	cp $(LIBS) local

local/%.cgi:	%.py
		python install.py $* local $(VERSION)

install:	all
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
