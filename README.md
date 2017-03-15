# cvsignore2gitignore
Script to transform cvsignore,v RCSFiles to gitignore,v files.
Background: if you convert a cvs repository to git using cvs2git it does not 
transform the .cvsignore-files. You can run this python script on a copy of your
cvs-repository before calling cvs2git to get this job done.
The script replaces all .cvsignore,v files by .gitignor,v files where the entries
are prefixed by a slash. The cvs history information will stay the same.


## syntax
    python3 cvsignore2gitignore.py <PathToCopiedRepository>

You might have to adjust the RCSFile-encoding to "utf-8" within the script (default is "cp1252")
calling the script without params will run the transformation with some test-data
from the zipfile example-cvsignore.zip 

## limitation
* does not transform several ignore entries per line.
* entries with @ char aren't supported.
* This is my first python script, so don't expect any syntactic sugar ;-> 

## requirement
* a copy of the cvs repository directory containing the *,v-RCSFiles.
* python3 3.4 interpreter instaled
  
## used resources

[cvsbook/RCS-Format.html](https://durak.org/sean/pubs/software/cvsbook/RCS-Format.html)


## changehistory
2017-03-13 Thomas Stroeter: first release. Includes eclipse PyDev project.