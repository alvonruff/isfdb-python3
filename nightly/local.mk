#
#     (C) COPYRIGHT 2013-2023   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1139 $
#     Date: $Date: 2023-07-12 18:51:22 -0400 (Wed, 12 Jul 2023) $


include .TARGETS
include ../INSTALLDIRS

INSTALL = $(INSTALL_HTML)/nightly

MYLIBS	= awards.py \
	  containers_cleanup.py \
	  database_corruption.py \
	  database_stats.py \
	  dup_authors.py \
	  front_page_pubs.py \
	  html_cleanup.py \
	  links_in_notes.py \
          nightly_cleanup.py \
          nightly_weekly_common.py \
	  shared_cleanup_lib.py \
	  slow_queries.py \
	  suspect_data.py \
	  translations_cleanup.py \
	  transliterations.py \
	  unicode_cleanup.py \
	  wiki.py

LIBS	= authorClass.py \
	  awardClass.py \
	  awardcatClass.py \
	  awardtypeClass.py \
	  titleClass.py \
	  pubClass.py \
	  publisherClass.py \
	  pubseriesClass.py \
	  recognizeddomainClass.py \
	  seriesClass.py \
	  templateClass.py \
	  verificationsourceClass.py \
	  install.py \
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

local/%.py:	%.py
		python install_nightly.py $* local /usr/bin/python

local/%.jpg:	%.jpg
		cp $*.jpg local

check_dirs:
		if test -d $(INSTALL); \
		then echo $(INSTALL) exists; \
		else mkdir $(INSTALL); \
		fi

install:	all check_dirs
		rm -f $(INSTALL)/*.pyc
		cp local/* $(INSTALL)
		chmod 744 $(INSTALL)/*.py

clean:
	rm -f local/*.pyc

clobber:
	rm -f $(LIBS)
	rm -rf local

