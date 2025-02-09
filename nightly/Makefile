#
#     (C) COPYRIGHT 2005-2013   Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 418 $
#     Date: $Date: 2019-05-15 10:10:07 -0400 (Wed, 15 May 2019) $


LOCAL:
	cat TARGETS | sed -e s/DIR/local/g > .TARGETS
	make -f local.mk 

TAMU:
	cat TARGETS | sed -e s/DIR/tamu/g > .TARGETS
	make -f tamu.mk 

SITE:
	cat TARGETS | sed -e s/DIR/site/g > .TARGETS
	make -f site.mk 

install:
	make -f local.mk install

clean:
	make -f local.mk clean
	rm -f *.cgi
	rm -f *.pyc
	rm -f .TARGETS
clobber:
	make -f local.mk clobber
	rm -f *.cgi
	rm -f *.pyc