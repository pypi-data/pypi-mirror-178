# pdrozd-ssg

pdrozd-ssg is a static site generator created in python

# Optional features

* Added title parsing

* Added recursive search

* Added automatically generated index file

# Requirements

Python 3

# Commands

The commands of pdrozd-ssg are
* -h or --help this will display to the user the options they have

* -c or --config this will specify a config file which contains arguments for SSG to read.

* -v or --version this will display to the user the current verison of pdrozd-ssg

* -i or --input this with a combanation of .txt or .md file or directory will output your files as a Static Site
  to use put in the format. e.g. <br>
   ```py ssg.py -i or --input [file.txt\text.ms] or [directory\]``` 

* -l or --lang this at the end of the input command will allow the default language of the HTML files to change. e.g.<br>
   ```py ssg.py -i or --input [file.txt\text.md] or [directory\] -l or --lang [language]```

# Config File
Config files should be in legal JSON format with a similar format like
``` 
{
    "input":"./Sherlock-Holmes-Selected-Stories",
    "lang":"fr"
} 
```

 # New features
 * Added JSON config file support 
 * Complete Markdown Support with the Help of [Python-Markdown/markdown](https://github.com/Python-Markdown/markdown)

 # Planned Features
 - [ ] Choosing Output Directory 
 
 - [ ] CSS support
