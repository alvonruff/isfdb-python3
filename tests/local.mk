#
#     (C) COPYRIGHT 2005-2023   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1139 $
#     Date: $Date: 2023-07-12 18:51:22 -0400 (Wed, 12 Jul 2023) $


VERSION = $(shell cat ../.pythonver)

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
	 sfe3.py \
	 isfdb.py \
	 library.py \
	 localdefs.py \
	 navbar.py \
	 install.py \
	 viewers.py

all:	

local/%.cgi:	%.py
		python install.py $* local $(VERSION)

install:

clean:
	rm -f $(LIBS)
	rm -f local/*.cgi
	rm -f local/*.pyc
	rm -rf __pycache__

clobber:
	rm -f $(LIBS)
	rm -f local/*.cgi
	rm -f local/*.pyc
	rm -rf __pycache__
