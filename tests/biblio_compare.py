

#######################################################################################
# DEFINES
#######################################################################################

BROWSER    = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
HTMLLOC    = "www.isfdb2.org"
COMPARELOC = "www.isfdb.org"

#######################################################################################
# UTILITIES
#######################################################################################

headers = {
    'User-Agent': BROWSER
}


def fixCopyright(image):
        image = image.replace('Copyright &copy; 1995-2026 Al von Ruff and the ISFDB team', 'Copyright &copy; 1995-2025 Al von Ruff and the ISFDB team')
        return image

def fixURL(image):
        image = image.replace(HTMLLOC, COMPARELOC)
        return image

################################################
# The order of reviews is order by their
# publication year. But the internal order
# of the reviews is currently nondeterministic
################################################

def StripReviews(image):

        startSignature = '<h3 class="contentheader">Reviews</h3>'
        stopSignature  = '</ul>'

        startIndex = image.rfind(startSignature)
        if startIndex == -1:
                return image

        stopIndex = image[startIndex:].rfind(stopSignature)
        stopIndex = startIndex + stopIndex + 6
        subString = image[startIndex:stopIndex]
        image =  image.replace(subString, '')

        return image

################################################
# This will strip out the SQLlogging messages
# on the system if GLOBAL_DEBUG == 1
################################################

def StripSQLdebug(image):

        startSignature = '<div class="VerificationBox">'
        stopSignature  = '<div id="bottom">'
        eraseSignature  = "</div></div>>"

        startIndex = image.rfind(startSignature)
        if startIndex == -1:
                return image

        stopIndex = image.rfind(stopSignature)
        stopIndex -= (len(eraseSignature)-6)
        subString = image[startIndex:stopIndex]
        image =  image.replace(subString, '')
        return image

################################################
# This will strip out CloudFlare scripts
################################################

def StripScript(image):

        startSignature = "<script>(function()"
        stopSignature  = "</script></body>"
        eraseSignature  = "</script>"

        startIndex = image.rfind(startSignature)
        if startIndex == -1:
                return image

        stopIndex = image.rfind(stopSignature)
        stopIndex += len(eraseSignature)
        subString = image[startIndex:stopIndex]
        image =  image.replace(subString, '')
        return image

def StripScriptFunction(image):
        import re

        re.sub(r'<script[^>]*email-decode\.min\.js[^>]*></script>', '', html)
        return image

def getPage(target, arg, site, postprocess, filename):
        import requests

        targetURL = 'https://%s/cgi-bin/%s?%s' % (site, target, arg)
        response = requests.get(targetURL, headers=headers)
        #print(response.status_code)
        #print(response.headers)
        image = response.text

        for alteration in postprocess:
                if alteration == "strip_trailing_script":
                        image = StripScript(image)
                elif alteration == "strip_sql_debug":
                        image = StripSQLdebug(image)
                elif alteration == "fix_url":
                        image = fixURL(image)
                elif alteration == "fix_copyright":
                        image = fixCopyright(image)
                elif alteration == "strip_reviews":
                        image = StripReviews(image)

        with open(filename, 'w', encoding="iso-8859-1") as f:
                f.write(image)

        return(image)

def isTitleNew(line):
        import re

        match = re.search(r'title\.cgi\?(\d+)', line)
        if match:
                from SQLparsing import SQLloadTitle

                title_id = match.group(1)  # '3588101'
                record = SQLloadTitle(title_id)
                if record == []:
                        return 1
                else:
                        return 0
        else:
                return 0


def isAuthorNew(line):
        import re

        match = re.search(r'ea\.cgi\?(\d+)', line)
        if match:
                from SQLparsing import SQLloadAuthorData

                author_id = match.group(1)  # 259811
                record = SQLloadAuthorData(author_id)
                if record == []:
                        return 1
                else:
                        return 0
        else:
                return 0

def outputDiff(line):
        import sys
        
        # Remove the DIFF header
        if ('GOLDEN' in line):
                line = line.replace("--- GOLDEN", '')
                return
        if ('TARGET' in line):
                line = line.replace("+++ TARGET", '')
                return

        # Only output the lines that start with -/+, not the context
        if line[0] == '-' or line[0] == '+':

                # Cloudflare modifies email lines. Toss those
                if '<a href="/cdn-cgi' in line:
                        print("*** IGNORE: CloudFlare insert")
                        return
                if 'cloudflare-static/email-decode' in line:
                        print("*** IGNORE: CloudFlare insert")
                        return
                if '<a href="mailto:' in line:
                        print("*** IGNORE: mailto line")
                        return
                if '__cf_email__' in line:
                        print("*** IGNORE: __cf_email__ line")
                        return

                # Look for new entries on the isfdb side
                if line[0] == '-':
                        if 'cgi-bin/title.cgi?' in line:
                                if isTitleNew(line):
                                        print("*** IGNORE: Reference to new title")
                                        return
                        if 'cgi-bin/ea.cgi?' in line:
                                if isAuthorNew(line):
                                        print("*** IGNORE: Reference to new title")
                                        return

                sys.stdout.write(line)

def compare_files(file1_path, file2_path, complex):
        import difflib

        with open(file1_path, 'r', encoding="iso-8859-1") as f1:
                f1_content = f1.readlines()
        with open(file2_path, 'r', encoding="iso-8859-1") as f2:
                f2_content = f2.readlines()

        diff = difflib.unified_diff(
                f1_content, f2_content,
                fromfile=file1_path,
                tofile=file2_path,
                lineterm='' # Use an empty lineterm for uniform output
        )

        lines = 0
        for line in diff:
                lines += 1
                if complex:
                        outputDiff(line)
        return(lines)

def simpleTest(script, target_list):
        import time

        print("\n#####################################################")
        print("Testing: ", script)
        print("#####################################################")
        error_list = []
        totFail = 0
        totPass = 0
        for target in target_list:
                print("Testing target:", target)
                targetImage = getPage(script, str(target),  HTMLLOC, ["fix_url", "strip_sql_debug", "fix_copyright", "strip_reviews"], "TARGET")
                goldenImage = getPage(script, str(target),  COMPARELOC, ["strip_trailing_script", "strip_reviews"], "GOLDEN")
                if recordIsNew(targetImage, script):
                        continue
                errors = compare_files("GOLDEN", "TARGET", 0)
                if errors:
                        totFail += 1
                        print("    FAIL")
                        error_list.append(target)
                else:
                        totPass += 1
                        print("    PASS")
                # Sleep to avoid CloudFlare rate limit
                time.sleep(1)
        if totFail:
                print("*** Errors:", totFail)
                print("*** ID Error List:", error_list)
                complexTest(script, error_list)
        print("TOTAL FAILURES FOR %s: %d" % (script, totFail))
        return(totFail, totPass)

def recordIsNew(image, script):
        if script == 'title.cgi':
                if '<h3>Unknown Title Record</h3>' in image:
                        print("*** This is a reference to a new title. Ignore error.")
                        return 1
        return 0

def complexTest(script, target_list):
        import time

        print("\n#####################################################")
        print("Detailed Diff View of Failures: ", script)
        print("#####################################################")
        for target in target_list:
                print("Testing target:", target)
                targetImage = getPage(script, str(target),  HTMLLOC, ["fix_url", "strip_sql_debug", "fix_copyright", "strip_reviews"], "TARGET")
                goldenImage = getPage(script, str(target),  COMPARELOC, ["strip_trailing_script", "strip_reviews"], "GOLDEN")
                if recordIsNew(targetImage, script):
                        continue
                errors = compare_files("GOLDEN", "TARGET", 1)
                if errors:
                        print("*** ERROR: ", script, target)
                        #print("*** Total Diffs:", errors)
                print("#####################################################")
                # Sleep to avoid CloudFlare rate limit
                time.sleep(1)
        return

#######################################################################################
# TESTS
#######################################################################################

def buildTitleList():

        title_list = []

        ###############################################################
        # Top 20 Highest Ranked Titles from the 1950s
        ###############################################################
        #   1117 The Stars My Destination
        #   2283 A Canticle for Leibowitz
        #   1499 More Than Human
        #   2248 Childhood's End
        #   1511 Mission of Gravity
        #   2122 The Demolished Man
        #   1972 Fahrenheit 451
        #   1629 The Lion, the Witch and the Wardrobe
        #  49838 Flowers for Algernon
        #  41108 The Nine Billion Names of God
        #   1112 Starship Troopers
        #   2276 A Case of Conscience
        #   1515 A Mirror for Observers
        #   7666 The Big Time
        #  55890 Sam Hall
        #  40913 The Star
        #  41176 The Man Who Sold the Moon
        #  21571 The Martian Chronicles
        #   1883 Gather, Darkness!
        #  55685 The Big Front Yard
        ###############################################################
        ti_list = [1117, 2283, 1499, 2248, 1511, 2122, 1972, 1629, 49838, 41108, 1112, 2276, 1515, 7666, 55890, 40913, 41176, 21571, 1883, 55685]
        title_list = title_list + ti_list

        ###############################################################
        # Top 20 Highest Ranked Titles from the 1960s
        ###############################################################
        #   2036 Dune
        #   7662 The Left Hand of Darkness
        #  14350 The Lord of the Rings
        #   1095 Stranger in a Strange Land
        #   1502 The Moon Is a Harsh Mistress
        #   1149 Stand on Zanzibar
        #  41692 Repent, Harlequin!" Said the Ticktockman
        #  28672 The Foundation Trilogy
        #   1611 Lord of Light
        #    939 Up the Line
        #  40866 Time Considered As a Helix of Semi-Precious Stones
        #  29365 The Last Castle
        #   7924 The Last Unicorn
        #  41588 A Boy and His Dog
        #   1867 Glory Road
        #  11826 The Dragon Masters
        #   1574 The Man in the High Castle
        #  41361 Gonna Roll the Bones
        #   2493 This Immortal
        #  14913 Nightwings
        ###############################################################
        ti_list = [2036, 7662, 14350, 1095, 1502, 1149, 41692, 28672, 1611, 939, 40866, 29365, 7924, 41588, 1867, 11826, 1574, 41361, 2493, 14913]
        title_list = title_list + ti_list

        ###############################################################
        # Top 20 Highest Ranked Titles from the 1970s
        ###############################################################
        #   1884 Gateway
        #   7659 The Dispossessed: An Ambiguous Utopia
        #   1319 Rendezvous with Rama
        #   1298 Ringworld
        #   1911 The Forever War
        #  49824 Jeffty Is Five
        #   1439 On Wings of Song
        #   2048 Dreamsnake
        #   1148 The Stand
        #  45192 Sandkings
        #  41070 The Persistence of Vision
        #    861 The White Dragon
        #    998 Titan
        #   1861 The Gods Themselves
        #  25261 The Chronicles of Thomas Covenant the Unbeliever
        #   1813 Harpist in the Wind
        #  41611 The Bicentennial Man
        #   1004 A Time of Changes
        #   2031 Dying Inside
        #  50107 Fireship
        ###############################################################
        ti_list = [1884, 7659, 1319, 1298, 1911, 49824, 1439, 1439, 2048, 1148, 45192, 41070, 861, 998, 1861, 25261, 1813, 41611, 1004, 2031, 50107]
        title_list = title_list + ti_list

        ###############################################################
        # 20 Titles whose Language is set to a unicode-intensive language.
        ###############################################################
        #  3211392 Akkadian
        #  2210922 Arabic
        #  1779018 Chinese
        #  2218756 Czech
        #   895314 Finnish
        #     7389 French
        #  1192592 German
        #  3372044 Greek
        #  1946124 Hebrew
        #  1842153 Icelandic
        #  1428497 Japanese
        #  3211096 Korean
        #  1694589 Norwegian
        #  2429809 Old Norse
        #   837545 Polish
        #   953669 Russia
        #  1053527 Serbian
        #  2718243 Spanish
        #  2712595 Swedish
        #  2440659 Ukranian
        ###############################################################
        ti_list = [3211392, 2210922, 1779018, 2218756, 895314, 7389, 1192592, 3372044, 1946124, 1842153, 1428497, 3211096, 1694589, 2429809, 837545, 953669, 1053527, 2718243, 2712595, 2440659]
        title_list = title_list + ti_list

        return(title_list)

def buildAuthorList():

        author_list = []

        ###############################################################
        # Top 20 Highest Ranked Authors and Editors from the 1950s
        ###############################################################
        #   29 Robert A. Heinlein
        #   17 Arthur C. Clarke
        #  194 Ray Bradbury
        #   56 Theodore Sturgeon
        #    6 Alfred Bester
        #    7 James Blish
        #   14 John W. Campbell, Jr.
        #   38 Fritz Leiber
        #   41 Walter M. Miller, Jr.
        #    3 Poul Anderson
        #  301 C. S. Lewis
        #  285 C. M. Kornbluth
        #  233 Hal Clement
        #  458 Willy Ley
        #    5 Isaac Asimov
        #   67 Edward E. Smith
        #   55 Clifford D. Simak
        #   51 Eric Frank Russell
        #   18 L. Sprague de Camp
        # 1085 Ray Van Houten
        ###############################################################
        ae_list = [29, 17, 194, 56, 6, 7, 14, 38, 41, 3, 301, 285, 233, 458, 5, 67, 55, 51, 18, 1085]
        author_list = author_list + ae_list

        ###############################################################
        # Top 20 Highest Ranked Authors and Editors from the 1960s
        # (Not appearing earlier)
        ###############################################################
        #   69 Roger Zelazny
        #   54 Robert Silverberg
        #   25 Harlan Ellison
        #   30 Frank Herbert
        #    3 Poul Anderson
        #   37 Ursula K. Le Guin
        #   22 Samuel R. Delany
        #   11 John Brunner
        #   42 Larry Niven
        #  820 Frederik Pohl
        #   14 John W. Campbell, Jr.
        #  136 Jack Vance
        #  176 Anne McCaffrey
        #   23 Philip K. Dick
        #  302 J. R. R. Tolkien
        #  131 Brian W. Aldiss
        #  821 Thomas M. Disch
        #   36 R. A. Lafferty
        #  501 Avram Davidson
        #  101 Cordwainer Smith
        ###############################################################
        ae_list = [69, 54, 25, 30, 3, 37, 22, 11, 42, 820, 14, 136, 176, 23, 302, 131, 821, 36, 501, 101]
        author_list = author_list + ae_list

        ###############################################################
        # Top 20 Highest Ranked Authors and Editors from the 1970s
        # (Not appearing earlier)
        ###############################################################
        #   59 John Varley
        #  401 George R. R. Martin
        #  243 Terry Carr
        #   57 James Tiptree, Jr.
        #  140 Michael Moorcock
        #   75 Michael Bishop
        #  171 Gene Wolfe
        # 1112 Charles N. Brown
        #   27 Joe Haldeman
        #   66 Kate Wilhelm
        #  423 Vonda N. McIntyre
        #   15 Orson Scott Card
        #  290 Charles L. Grant
        #   70 Stephen King
        # 25555 Dena Brown
        #  222 Joanna Russ
        #  109 Gregory Benford
        #   60 Joan D. Vinge
        #  633 Damon Knight
        #  481 Richard Cowper
        ###############################################################
        ae_list = [59, 401, 243, 57, 140, 75, 171, 1112, 27, 66, 423, 15, 290, 70, 25555, 222, 109, 60, 633, 481]
        author_list = author_list + ae_list

        ###############################################################
        # Top 20 Highest Ranked Authors and Editors from the 1980s
        # (Not appearing earlier)
        ###############################################################
        #  252 Lucius Shepard
        #  491 Kim Stanley Robinson
        #   99 Connie Willis
        #  172 William Gibson
        #    8 David Brin
        #    9 Greg Bear
        #  280 Bruce Sterling
        #  246 Howard Waldrop
        #   16 C. J. Cherryh
        #  179 Michael Swanwick
        # 1111 Andrew Porter
        #  105 Tanith Lee
        #  201 George Alec Effinger
        #  711 John Crowley
        #  170 Dan Simmons
        #   13 Lois McMaster Bujold
        #  175 Tim Powers
        #  186 Octavia E. Butler
        # 1804 Michael Whelan
        #   96 Pat Cadigan
        ###############################################################
        ae_list = [259, 491, 99, 172, 8, 9, 280, 246, 16, 179, 1111, 105, 201, 711, 170, 13, 175, 186, 1804, 96 ]
        author_list = author_list + ae_list

        ###############################################################
        # 20 Authors whose Language is set to a unicode-intensive language.
        ###############################################################
        #  317994 Akkadian
        #  254237 Arabic
        #  208409 Chinese
        #     161 Czech
        #   29665 Finnish
        #     159 French
        #    6773 German
        #  271538 Greek
        #  196574 Hebrew
        #  179004 Icelandic
        #   14571 Japanese
        #  336273 Korean
        #  162115 Norwegian
        #  280275 Old Norse
        #  166136 Polish
        #    1539 Russia
        #   18773 Serbian
        #  120085 Spanish
        #  277614 Swedish
        #  167535 Ukranian
        ###############################################################
        ae_list = [317994, 254237, 208409, 161, 29665, 159, 6773, 271538, 196574, 179004, 14571, 336273, 162115, 280275, 166136, 1539, 18773, 120085, 277614, 167535 ]
        author_list = author_list + ae_list

        return(author_list)

def test_ea():
        target = "ea.cgi"
        author_list = buildAuthorList()

        (totFail, totPass)  = simpleTest(target, author_list)
        return (totFail, totPass)

def test_eaw():
        target = "eaw.cgi"
        author_list = buildAuthorList()

        (totFail, totPass)  = simpleTest(target, author_list)
        return (totFail, totPass)

def test_ae():
        target = "ae.cgi"
        author_list = buildAuthorList()

        (totFail, totPass)  = simpleTest(target, author_list)
        return (totFail, totPass)

def test_ch():
        target = "ch.cgi"
        author_list = buildAuthorList()

        (totFail, totPass)  = simpleTest(target, author_list)
        return (totFail, totPass)

def test_author_history():
        target = "author_history.cgi"
        author_list = [ 29 ]

        # Only moderators can use this, so we test only one author

        (totFail, totPass)  = simpleTest(target, author_list)
        return (totFail, totPass)

def test_authors_by_debut_year():
        target = "authors_by_debut_year.cgi"
        arg_list = [ 1940, 1945, 1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000 ]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_authors_by_debut_year_table():
        target = "authors_by_debut_year_table.cgi"
        arg_list = [ 0 ]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_authortags():
        target = "authortags.cgi"
        arg_list = buildAuthorList()
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_title():
        target = "title.cgi"
        title_list = buildTitleList()

        print("test_title:", title_list)
        (totFail, totPass)  = simpleTest(target, title_list)
        return (totFail, totPass)

def test_pl():
        target = "pl.cgi"
        pub_list = [778515, 108251, 836980, 15117, 193917]

        (totFail, totPass)  = simpleTest(target, pub_list)
        return (totFail, totPass)

def test_calendar_menu():
        target = "calendar_menu.cgi"
        pub_list = [0]

        (totFail, totPass)  = simpleTest(target, pub_list)
        return (totFail, totPass)

def test_calendar_day():
        target = "calendar_day.cgi"
        pub_list = ["2+28"]

        (totFail, totPass)  = simpleTest(target, pub_list)
        return (totFail, totPass)

def test_adv_identifier_search():
        target = "adv_identifier_search.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_adv_notes_search():
        target = "adv_notes_search.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_adv_search_menu():
        target = "adv_search_menu.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_adv_search_results():
        target = "adv_search_results.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_adv_search_selection():
        target = "adv_search_selection.cgi"
        arg_list = [ 'author', 'title', 'series', 'pub', 'publisher', 'pub_series', 'award_type', 'award_cat', 'award']
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_adv_user_search():
        target = "adv_user_search.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_adv_web_page_search():
        target = "adv_web_page_search.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_award_category():
        target = "award_category.cgi"
        arg_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_award_category_history():
        target = "award_category_history.cgi"
        arg_list = [170, 504]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_award_category_year():
        target = "award_category_year.cgi"
        arg_list = ["1+1980", '2+1980', '3+1980', '4+1980']
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_award_details():
        target = "award_details.cgi"
        arg_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_award_directory():
        target = "award_directory.cgi"
        arg_list = [ 0 ]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_award_history():
        target = "award_history.cgi"
        arg_list = [80349, 83866 ]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_awardtype():
        target = "awardtype.cgi"
        arg_list = [23, 31, 40, 44]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_awardtype_history():
        target = "awardtype_history.cgi"
        arg_list = [23, 31, 40, 44]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_ay():
        target = "ay.cgi"
        arg_list = [ "23+2001", "31+2001", "40+2001", "44+2001"]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_cancelsubmission():
        target = "cancelsubmission.cgi"

        print("SKIP. This is a manual test")
        return (0, 0)

def test_changed_verified_pubs():
        target = "changed_verified_pubs.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_diffselect():
        target = "diffselect.cgi"
        arg_list = [6522377]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_directory():
        target = "directory.cgi"
        arg_list = [ "author", "magazine", "publisher" ]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_dologin():
        target = "dologin.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_dologout():
        target = "dologout.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_dumpxml():
        target = "dumpxml.cgi"
        arg_list = [778515]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_external_id_search_results():
        target = "external_id_search_results.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_fc():
        target = "fc.cgi"
        arg_list = [1050]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_google_search_redirect():
        target = "google_search_redirect.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_index():
        target = "index.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_languages():
        target = "languages.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_most_popular():
        target = "most_popular.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_most_popular_table():
        target = "most_popular_table.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_most_reviewed():
        target = "most_reviewed.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_most_reviewed_table():
        target = "most_reviewed_table.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_mylanguages():
        target = "mylanguages.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_mypreferences():
        target = "mypreferences.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_myrecent():
        target = "myrecent.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_my_removed_secondary_verifications():
        target = "my_removed_secondary_verifications.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_my_secondary_verifications():
        target = "my_secondary_verifications.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_my_unstable_ISBN_verifications():
        target = "my_unstable_ISBN_verifications.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_my_unstable_verifications():
        target = "my_unstable_verifications.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_my_verifications_menu():
        target = "my_verifications_menu.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_myvotes():
        target = "myvotes.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_mywebsites():
        target = "mywebsites.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_note():
        target = "note.cgi"
        arg_list = [428890]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_note_search_results():
        target = "note_search_results.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_pe():
        target = "pe.cgi"
        arg_list = [778515]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_popular_authors():
        target = "popular_authors.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_popular_authors_table():
        target = "popular_authors_table.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_pub_history():
        target = "pub_history.cgi"
        arg_list = [778515]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_publisher():
        target = "publisher.cgi"
        arg_list = [53666]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_publisher_authors():
        target = "publisher_authors.cgi"
        arg_list = [53666]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_publisher_history():
        target = "publisher_history.cgi"
        arg_list = [53666]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_publisher_one_author():
        target = "publisher_one_author.cgi"
        arg_list = ["53666+29"]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_publisheryear():
        target = "publisheryear.cgi"
        arg_list = ["53666+1960"]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_pubseries():
        target = "pubseries.cgi"
        arg_list = [1]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_pubseries_history():
        target = "pubseries_history.cgi"
        arg_list = [1]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_pubs_not_in_series():
        target = "pubs_not_in_series.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_recent_activity_menu():
        target = "recent_activity_menu.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_recent():
        target = "recent.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_recent_primary_ver():
        target = "recent_primary_ver.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_recentver():
        target = "recentver.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_removed_secondary_verifications():
        target = "removed_secondary_verifications.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_se():
        target = "se.cgi"
        arg_list = [171]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_seriesgrid():
        target = "seriesgrid.cgi"
        arg_list = [171]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_series_history():
        target = "series_history.cgi"
        arg_list = [171]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_seriestags():
        target = "seriestags.cgi"
        arg_list = [171]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_stats_and_tops():
        target = "stats-and-tops.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_stats():
        target = "stats.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_submitdiff():
        target = "submitdiff.cgi"
        arg_list = [6522377]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_submitlogin():
        target = "submitlogin.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_submitmylanguages():
        target = "submitmylanguages.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_submitmywebsites():
        target = "submitmywebsites.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_submitpreferences():
        target = "submitpreferences.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_tag():
        target = "tag.cgi"
        arg_list = [1]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_tag_author():
        target = "tag_author.cgi"
        arg_list = [1]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_titlecovers():
        target = "titlecovers.cgi"
        title_list = buildTitleList()
        (totFail, totPass)  = simpleTest(target, title_list)
        return (totFail, totPass)

def test_title_history():
        target = "title_history.cgi"
        title_list = buildTitleList()
        (totFail, totPass)  = simpleTest(target, title_list)
        return (totFail, totPass)

def test_topcontrib():
        target = "topcontrib.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_user_search_results():
        target = "user_search_results.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_usertag():
        target = "usertag.cgi"
        arg_list = [1]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_usertitles():
        target = "usertitles.cgi"
        arg_list = [1]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_userver():
        target = "userver.cgi"
        arg_list = [1]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_verification_sources():
        target = "verification_sources.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_view_submission():
        target = "view_submission.cgi"
        arg_list = [6522377]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def test_webpages_search_results():
        target = "webpages_search_results.cgi"
        arg_list = [0]
        (totFail, totPass)  = simpleTest(target, arg_list)
        return (totFail, totPass)

def doAdvancedSearchTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_adv_identifier_search()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_adv_notes_search()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_adv_search_menu()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_adv_search_results()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_adv_search_selection()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_adv_user_search()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_adv_web_page_search()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doAuthorTests():
        tot_fail = 0
        tot_pass = 0
        #(failed, passed) = test_ea()
        #tot_fail += failed
        #tot_pass += passed
        #(failed, passed) = test_eaw()
        #tot_fail += failed
        #tot_pass += passed
        #(failed, passed) = test_ae()
        #tot_fail += failed
        #tot_pass += passed
        #(failed, passed) = test_ch()
        #tot_fail += failed
        #tot_pass += passed
        #(failed, passed) = test_author_history()
        #tot_fail += failed
        #tot_pass += passed
        #(failed, passed) = test_authors_by_debut_year()
        #tot_fail += failed
        #tot_pass += passed
        #(failed, passed) = test_authors_by_debut_year_table()
        #tot_fail += failed
        #tot_pass += passed
        (failed, passed) = test_authortags()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_ay()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doAwardTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_award_category()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_award_category_history()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_award_category_year()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_award_details()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_award_directory()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_award_history()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_awardtype()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_awardtype_history()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doCalendarTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_calendar_menu()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_calendar_day()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doDirectoryTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_directory()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_index()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_languages()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doLoginTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_dologin()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_dologout()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_submitlogin()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doMiscTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_changed_verified_pubs()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_dumpxml()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_external_id_search_results()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_fc()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_google_search_redirect()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_verification_sources()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doMyTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_mylanguages()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_mypreferences()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_myrecent()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_my_removed_secondary_verifications()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_my_secondary_verifications()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_my_unstable_ISBN_verifications()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_my_unstable_verifications()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_my_verifications_menu()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_myvotes()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_mywebsites()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_submitmylanguages()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_submitmywebsites()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_submitpreferences()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doNoteTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_note()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_note_search_results()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doPopularStatsTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_most_popular()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_most_popular_table()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_most_reviewed()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_most_reviewed_table()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_popular_authors()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_popular_authors_table()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_stats_and_tops()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_stats()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_topcontrib()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doPublicationTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_pl()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_pe()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_pub_history()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doPublisherTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_publisher()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_publisher_authors()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_publisher_history()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_publisher_one_author()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_publisheryear()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doPubSeriesTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_pubseries()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_pubseries_history()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_pubs_not_in_series()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doRecentTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_recent_activity_menu()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_recent()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_recent_primary_ver()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_recentver()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_removed_secondary_verifications()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doSearchResultTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_user_search_results()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_webpages_search_results()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doSeriesTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_se()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_seriesgrid()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_series_history()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_seriestags()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doSubmissionTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_cancelsubmission()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_diffselect()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_submitdiff()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_view_submission()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doTagTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_tag()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_tag_author()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_usertag()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doTitleTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_title()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_titlecovers()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_title_history()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doUserTests():
        tot_fail = 0
        tot_pass = 0
        (failed, passed) = test_usertitles()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = test_userver()
        tot_fail += failed
        tot_pass += passed
        return (tot_fail, tot_pass)

def doAllTests():

        tot_fail = 0
        tot_pass = 0

        (failed, passed) = doAdvancedSearchTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doAuthorTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doAwardTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doCalendarTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doDirectoryTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doLoginTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doMiscTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doMyTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doNoteTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doPopularStatsTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doPublicationTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doPublisherTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doPubSeriesTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doRecentTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doSearchResultTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doSeriesTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doSubmissionTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doTagTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doTitleTests()
        tot_fail += failed
        tot_pass += passed
        (failed, passed) = doUserTests()
        tot_fail += failed
        tot_pass += passed

        print("Total PASS:", tot_pass)
        print("Total FAIL:", tot_fail)

###########################################################
#
# doOneTest exists to allow hand running a single tests.
#
# Modify parameters here to run a single test for debug.
# target = target script
# arg    = arguments to the script
#
# This will leave two files in the directory: GOLDEN and TARGET
# GOLDEN is isfdb.org
# TARGET is system under test
#
# Start your effors with: diff GOLDEN TARGET
#
###########################################################

def doOneTest():
        testSection = 3

        if testSection == 1:
	        # Single test, small number of args
                target = "ea.cgi"
                arg_list = [317994, 254237, 208409, 161, 29665, 159, 6773, 271538, 196574, 179004, 14571, 336273, 162115, 280275, 166136, 1539, 18773, 120085, 277614, 167535 ]
                (totFail, totPass)  = simpleTest(target, arg_list)

        elif testSection == 2:
	        # Single test, normal args
                #test_ea()
                test_title()

        elif testSection == 3:
	        # Group tests
	        doTitleTests()

if __name__ == '__main__':

        doSingleTest = 1

        if doSingleTest:
                doOneTest()
        else:
                doAllTests()
