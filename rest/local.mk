#
#     (C) COPYRIGHT 2005-2018   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 227 $
#     Date: $Date: 2018-10-08 17:00:11 -0400 (Mon, 08 Oct 2018) $

include .TARGETS
include ../INSTALLDIRS

INSTALL = $(INSTALL_CGI)/rest
VERSION = $(shell cat ../.pythonver)

MYLIBS	= pub_output.py

LIBS = login.py \
	SQLparsing.py \
	isbn.py \
	isfdb.py \
	library.py \
	navbar.py \
	install.py \
	pubClass.py \
	isfdblib.py

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
		cp local/* $(INSTALL)
		chmod 755 $(INSTALL)/*.cgi
		chmod 644 $(INSTALL)/*.py

clean:
	rm -f local/*.cgi
	rm -f local/*.pyc

clobber:
	rm -f $(LIBS)
	rm -rf local
