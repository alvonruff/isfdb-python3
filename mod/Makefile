#
#     (C) COPYRIGHT 2005-2006   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 17 $
#     Date: $Date: 2017-10-31 18:57:31 -0400 (Tue, 31 Oct 2017) $


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

