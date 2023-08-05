# This prints the Help message


def printHelp():
    raise SystemExit(
        """------Help------
The commands of pdrozd-ssg are
* -h or --help this will display to the user the options they have

* -v or --version this will display to the user the current verison of pdrozd-ssg

* -i or --input this with a combanation of file or directory will output your files as a Static Site
   to use put in the format py ssg.py -i or --input [file.txt] or [directory]

* -c or --config this will specify a config file which contains arguments for SSG to read.
  """
    )
