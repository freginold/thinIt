# thinIt
thinIt is a basic JavaScript (.js) / CSS (.css)  minifier written in Python.

## Syntax:

`thinit.py [filename] ["optional comment text"]`

For `filename`, include the path if the file is not in the current directory (with quotes, if there are spaces).  `optional comment text` is used if you want to insert a comment as the first line of the minified file, for example to include the file name, version number, date, brief description, etc.

Typing `thinit.py help` will bring up a brief help screen.

thinIt has rudimentary support for Python (.py\*) and VBScript (.vb\*) files as well.  For Python it removes blank lines and lines that begin with a comment, and for VBScript it removes blank lines, lines that begin with a comment, and indentations.  Support for Python docstring comments will be coming in a future version.

## Requirements:

- Python 2.7.x

##

![screen shot](https://github.com/freginold/thinIt/blob/master/ss_thinIt_v1_0_0.png)

thinIt is versioned using [Semantic Versioning](http://semver.org/).
