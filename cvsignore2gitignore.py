#!/usr/bin/env python3
# -*- coding: UTF-8

import os
import re
import traceback
import sys
import shutil
import zipfile

# cvsignore2gitigore
# ------------------
# Use this additional script before you call cvs2git.
# Converts .cvsignore,v RCFiles to .gitignore,v files.
#
# WARNING: this scripts replaces the original .cvsignore-files.
#          Do not apply it to your original CVS repository but to a copy!
#
# HINT:    Adjust the 'rcsEncoding' variable to match your repo encoding.
#
# Thomas Stroeter 2017/03/12
#
# Syntax:
#    cvsignore2gitigore <path to CVS-repository directory>
#
#    exitcode: 0 OK, other value means an error occured

# adjust rcsEncoding (cp1252, utf-8)
rcsEncoding="cp1252"

regmatch_add=re.compile("[@]?a\d+\s+\d+.*")
regmatch_del=re.compile("[@]?d\d+\s+\d+.*")


def convert_all_cvsignore_in_dir(CVSRepoDir):        
    print("* replace .cvsignore,v files in "+CVSRepoDir+" by .gitignore,v files:")
    for root, dirs, files in os.walk(CVSRepoDir):
        for file in files:
            if file==".cvsignore,v":
                gitignore_dest_file=os.path.join(root, ".gitignore,v")
                if not os._exists(gitignore_dest_file):
                    cvsignore_src_file=os.path.join(root, file)
                    convert_cvsignore(cvsignore_src_file, gitignore_dest_file)




def convert_cvsignore(cvsignore_src_file, gitignore_dest_file):
    # 0. read .cvsignore,v RCSFile
    print("  " + cvsignore_src_file)        
    with open(cvsignore_src_file, "r", encoding=rcsEncoding) as cvsignore_in:
        lines=cvsignore_in.readlines()
    # 1. reuse all lines from the RCSFile up to "desc" line unmodidiefied
    i=0
    while i < len(lines) and not lines[i].rstrip()=="desc":
        i=i+1
    # 2. replace text@XYZ@ entries by prefixing a slash (/)
    replaceTextLines(lines, i)
    # 3. write as .gitignore,v / remove cvsignore file
    with open(gitignore_dest_file, "w", encoding=rcsEncoding ) as gitignore_out:
        for line in lines:
            gitignore_out.write(line)
    os.remove(cvsignore_src_file)


# loop over all text@@ bodies
def replaceTextLines(lines, i):
    while (i < len(lines)):
        line=lines[i].rstrip()
        if line=="text":
            i=i+1
            line=lines[i].rstrip()
            if line=="@@":
                i=i+1
            else:
                endsWithAt=False
                if not line[:1]=="@":
                    1/0
                if len(line)>1:
                    startWithAt=True
                    if line.endswith("@"):
                        endsWithAt=True
                else:
                    startWithAt=False
                    i=i+1
                firstIndex=i
                # suche lastIndex
                lastIndex=i
                while (not endsWithAt) and lastIndex< len(lines) and not lines[lastIndex+1].rstrip().endswith("@"):
                    lastIndex=lastIndex+1
                # parse Text-Body-Zeile Start/Ende
                replaceText(lines, firstIndex, lastIndex, startWithAt)
        else:
            i=i+1
            

# replace a text body by prefixing a slash to each line
def replaceText(lines, firstIndex, lastIndex, startWithAt):
    if startWithAt:
        lines[firstIndex]="@" + replaceTextLine(lines[firstIndex][1:])
    else:
        lines[firstIndex]=replaceTextLine(lines[firstIndex])
    i=firstIndex
    while ( i < lastIndex):
        i=i+1
        lines[i]=replaceTextLine(lines[i])


# replace a text line by prefixing a slash
# specialcases to be ignored:
#        d<n> <n> - delete lines
#        a<n> <n> - insert lines
#        empty lines
def replaceTextLine(line):
    if (len(line.strip())==0) or regmatch_add.match(line) or regmatch_del.match(line):
        return line
    if line[:1]=='!':
        return "!/"+line
    else:
        return "/"+line



## MAIN ##
        
try:
    exitCode=11
    # get param: CVSRepoDir 
    if len(sys.argv)==2:
        CVSRepoDir=sys.argv[1]
    else:
        # unzip test_cvsrepo from zip - replace the zipfile for testing
        print("  unzip test-resources...")
        build_dir=os.path.join( os.getcwd(), "build" )
        CVSRepoDir=os.path.join( build_dir, "test_cvsrepo" )
        if os.path.isdir(CVSRepoDir):
            shutil.rmtree(CVSRepoDir)
        os.makedirs(CVSRepoDir)
        zip_file=os.path.join( os.curdir, "resources/example-cvsignore.zip")
        zip_ref = zipfile.ZipFile(zip_file, 'r')
        zip_ref.extractall(CVSRepoDir)
        zip_ref.close()
    convert_all_cvsignore_in_dir( os.path.normpath(CVSRepoDir) )    
    exitCode=0
except Exception:
    traceback.print_exc() 

finally:
    sys.exit(exitCode)