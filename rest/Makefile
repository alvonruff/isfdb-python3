#
#     (C) COPYRIGHT 2005-2008   Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1243 $
#     Date: $Date: 2026-02-07 09:19:16 -0500 (Sat, 07 Feb 2026) $

LOCAL:
	cat TARGETS | sed -e s/DIR/local/g > .TARGETS
	make -f local.mk 

TAMU:
	cat TARGETS | sed -e s/DIR/tamu/g > .TARGETS
	make -f tamu.mk 

SITE:
	cat TARGETS | sed -e s/DIR/site/g > .TARGETS
	make -f site.mk 

lint:
	bash ../common/dolint.sh

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
