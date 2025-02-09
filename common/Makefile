#
#     (C) COPYRIGHT 2005-2023   Al von Ruff and Ahasuerus
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 1139 $
#     Date: $Date: 2023-07-12 18:51:22 -0400 (Wed, 12 Jul 2023) $


BASE_FILES = login.py \
        SQLparsing.py \
        isbn.py \
        isfdb.py \
        library.py \
        navbar.py \
        install.py \
        sfe3.py

CLASS_FILES = authorClass.py \
        awardClass.py \
        awardcatClass.py \
        awardtypeClass.py \
        pubClass.py \
        publisherClass.py \
        pubseriesClass.py \
        recognizeddomainClass.py \
        seriesClass.py \
        templateClass.py \
        titleClass.py \
        verificationsourceClass.py \
        viewers.py

check_dirs:
	if test -d ../biblio/local; \
	then echo biblio/local exists; \
	else mkdir ../biblio/local; \
	fi
	if test -d ../edit/local; \
	then echo edit/local exists; \
	else mkdir ../edit/local; \
	fi
	if test -d ../mod/local; \
	then echo mod/local exists; \
	else mkdir ../mod/local; \
	fi
	if test -d ../rest/local; \
	then echo rest/local exists; \
	else mkdir ../rest/local; \
	fi
	if test -d ../nightly/local; \
	then echo nightly/local exists; \
	else mkdir ../nightly/local; \
	fi

install: check_dirs
	cp $(BASE_FILES) ../biblio
	cp $(CLASS_FILES) ../biblio
	cp localdefs.py ../biblio/local
	cp $(BASE_FILES) ../edit
	cp $(CLASS_FILES) ../edit
	cp localdefs.py ../edit/local
	cp $(BASE_FILES) ../mod
	cp $(CLASS_FILES) ../mod
	cp localdefs.py ../mod/local
	cp $(BASE_FILES) ../rest
	cp $(CLASS_FILES) ../rest
	cp localdefs.py ../rest/local
	cp $(BASE_FILES) ../nightly
	cp $(CLASS_FILES) ../nightly
	cp localdefs.py ../nightly/local
	cp localdefs.py ../css
	cp localdefs.py ../scripts
	cp $(BASE_FILES) ../scripts

clean:
	cd ../biblio && rm -rf $(BASE_FILES) $(CLASS_FILES) local
	cd ../edit && rm -rf $(BASE_FILES) $(CLASS_FILES) local 
	cd ../mod && rm -rf $(BASE_FILES) $(CLASS_FILES) local
	cd ../rest && rm -rf $(BASE_FILES) $(CLASS_FILES) local
	cd ../nightly && rm -rf $(BASE_FILES) $(CLASS_FILES) local
	rm -f ../css/localdefs.py
	rm -f ../scripts/localdefs.py

diff:
	diff install.py  ../biblio
	diff isbn.py ../biblio
	diff isfdb.py ../biblio
	diff localdefs.py ../biblio/local
	diff login.py ../biblio
	diff pubClass.py ../biblio
	diff publisherClass.py ../biblio
	diff pubseriesClass.py ../biblio
	diff templateClass.py ../biblio
	diff verificationsourceClass.py ../biblio
	diff authorClass.py ../biblio
	diff awardClass.py ../biblio
	diff awardcatClass.py ../biblio
	diff awardtypeClass.py ../biblio
	diff seriesClass.py ../biblio
	diff titleClass.py ../biblio
	diff SQLparsing.py ../biblio
	diff library.py ../biblio
	diff navbar.py ../biblio
	diff install.py  ../edit
	diff isbn.py ../edit
	diff isfdb.py ../edit
	diff localdefs.py ../edit/local
	diff login.py ../edit
	diff pubClass.py ../edit
	diff publisherClass.py ../edit
	diff pubseriesClass.py ../edit
	diff recognizeddomainClass.py ../edit
	diff templateClass.py ../edit
	diff verificationsourceClass.py ../edit
	diff authorClass.py ../edit
	diff awardClass.py ../edit
	diff awardcatClass.py ../edit
	diff awardtypeClass.py ../edit
	diff seriesClass.py ../edit
	diff SQLparsing.py ../edit
	diff titleClass.py ../edit
	diff library.py ../edit
	diff navbar.py ../edit
	diff viewers.py ../edit
	diff install.py  ../mod
	diff isbn.py ../mod
	diff isfdb.py ../mod
	diff localdefs.py ../mod/local
	diff login.py ../mod
	diff pubClass.py ../mod
	diff publisherClass.py ../mod
	diff pubseriesClass.py ../mod
	diff templateClass.py ../mod
	diff verificationsourceClass.py ../mod
	diff authorClass.py ../mod
	diff awardClass.py ../mod
	diff awardcatClass.py ../mod
	diff awardtypeClass.py ../mod
	diff seriesClass.py ../mod
	diff SQLparsing.py ../mod
	diff titleClass.py ../mod
	diff library.py ../mod
	diff navbar.py ../mod
	diff viewers.py ../mod
	diff install.py  ../rest
	diff isbn.py ../rest
	diff isfdb.py ../rest
	diff localdefs.py ../rest/local
	diff login.py ../rest
	diff pubClass.py ../rest
	diff publisherClass.py ../rest
	diff pubseriesClass.py ../rest
	diff templateClass.py ../rest
	diff verificationsourceClass.py ../rest
	diff authorClass.py ../rest
	diff awardClass.py ../rest
	diff awardcatClass.py ../rest
	diff awardtypeClass.py ../rest
	diff seriesClass.py ../rest
	diff SQLparsing.py ../rest
	diff titleClass.py ../rest
	diff library.py ../rest
	diff navbar.py ../rest
	diff install.py  ../nightly
	diff isbn.py ../nightly
	diff isfdb.py ../nightly
	diff localdefs.py ../nightly/local
	diff login.py ../nightly
	diff pubClass.py ../nightly
	diff publisherClass.py ../nightly
	diff pubseriesClass.py ../nightly
	diff templateClass.py ../nightly
	diff verificationsourceClass.py ../nightly
	diff authorClass.py ../nightly
	diff awardClass.py ../nightly
	diff awardcatClass.py ../nightly
	diff awardtypeClass.py ../nightly
	diff seriesClass.py ../nightly
	diff SQLparsing.py ../nightly
	diff titleClass.py ../nightly
	diff library.py ../nightly
	diff navbar.py ../nightly
