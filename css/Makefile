#
#     (C) COPYRIGHT 2008-2025   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 583 $
#     Date: $Date: 2020-12-27 18:42:13 -0500 (Sun, 27 Dec 2020) $


# Need to create index.html

include ../INSTALLDIRS

INSTALL = $(INSTALL_HTML)

TARGETS	= apple-touch-icon.png \
	  apple-touch-icon-precomposed.png \
	  biblio.css \
	  checkmark.png \
	  favicon.ico \
	  isfdb.gif \
	  isfdb_logo.jpg \
	  index.html \
	  IsfdbBanner1.jpg \
	  IsfdbBanner2.jpg \
	  IsfdbBanner3.jpg \
	  IsfdbBanner4.jpg \
	  IsfdbBanner5.jpg \
	  IsfdbBanner6.jpg \
	  IsfdbBanner7.jpg \
	  IsfdbBanner8.jpg \
	  IsfdbBanner9.jpg \
	  IsfdbBanner10.jpg \
	  IsfdbBanner11.jpg \
	  IsfdbBanner12.jpg \
	  question_mark_icon.gif \
	  adv_search.js \
	  edit_js.js \
	  edit_pub.js \
	  edit_author.js \
	  edit_award.js \
	  edit_other.js \
	  edit_title.js \
	  isfdb_main.js

install:
	python index_install.py
	cp $(TARGETS) $(INSTALL)
	rm -f *.pyc

clean: clobber

clobber:
	rm -f localdefs.*
	rm -f index.html
	rm -f biblio.css
