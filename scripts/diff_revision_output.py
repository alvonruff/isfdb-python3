#!_PYTHONLOC
from __future__ import print_function
#
#     (C) COPYRIGHT 2007-2025   Jesse Weinstein, Al von Ruff
#       ALL RIGHTS RESERVED
#
#     The copyright notice above does not evidence any actual or
#     intended publication of such source code.
#
#     Version: $Revision: 15 $
#     Date: $Date: 2017-10-31 16:32:38 -0400 (Tue, 31 Oct 2017) $

#
#     Written in 2010 by Jesse Weinstein <jesse@wefu.org>
#
#
#     To the extent possible under law, Jesse Weinstein has waived
#     all copyright and related or neighboring rights to
#     diff_revison_output.py. This work is published from:
#     United States of America. 
#     See http://creativecommons.org/publicdomain/zero/1.0/
#     for details.

import sys, subprocess, shutil, urllib
import localdefs

#TODO: Improve get_output to handle cookies, complex sequences of actions (maybe
#       using http://twill.idyll.org/ or some such...)

def printhelp():
    print('This program generates the output of a given file as produced')
    print('by a given revision of the code, and the current state of the')
    print(' code, and outputs the comparison between them.')
    print()
    print('The first argument is either -r or -D, and is passed through to CVS.')
    print('As is the second argument, which should be a tag or date, respectively.')
    print('The third argument is the path to the output file to be compared, without a leading slash.')

def die_with_error(e):
    print(e)
    print('-------')
    printhelp()
    sys.exit(1)

def get_output(filename, ext):
    f=urllib.urlopen("http:/%s/%s" % (localdefs.HTFAKE, filename))
    outfilename=escape_filename(filename)+ext
    open('reference_tree/'+outfilename,'w').write(f.read())
    f.close()

def escape_filename(f):
    return f.replace('/','_').replace('?','_').replace('&','_')

def statusmsg(s):
    sys.stderr.write(s+'\n'+('*'*len(s))+'\n')

if __name__=='__main__':
    if len(sys.argv)<4:
        die_with_error('ERROR: Insufficient arguments given!')
    if sys.argv[1] not in ['-r','-D']:
        die_with_error('ERROR: Invalid first argument!')

    statusmsg('Checkout reference version...')

    subprocess.call(("cvs", "checkout", sys.argv[1], sys.argv[2],
                     "-d", "reference_tree", "isfdb2"))
    
    shutil.copy("../INSTALLDIRS", "reference_tree/")
    shutil.copy("../common/localdefs.py", "reference_tree/common/")

    statusmsg('Install reference version...')

    subprocess.call("cd reference_tree && make install; echo 'XXX'", shell=True)
    get_output(sys.argv[3], '.ref')

    statusmsg('Install current version...')
    
    subprocess.call("cd .. && make install", shell=True)
    get_output(sys.argv[3], '.cnt')

    statusmsg('Compare the output...')
    
    basefilename="reference_tree/"+escape_filename(sys.argv[3])
    subprocess.call(("diff", "-u", basefilename+".ref", basefilename+".cnt"))
    
