# thinIt
thinIt is a basic JavaScript (.js) / CSS (.css)  minifier written in Python.

## Syntax:

`thinit.py [filename] ["optional comment text"]`

- `filename` -- Name of the file to minify. Include the file path if not in the current directory (with quotes, if there are spaces).
- `"optional comment text"` -- If you want to insert a comment at the beginning of the minified file (to reference the version number, date, etc.) include it here, in quotes.

*Example:*

`thinit.py test.js "Test file v1.0"`

Typing `thinit.py help` will bring up a brief help screen.

thinIt has rudimentary support for Python (.py\*) and VBScript (.vb\*) files as well.  For Python it removes blank lines and lines that begin with a comment, and for VBScript it removes blank lines, lines that begin with a comment, and indentations.  Support for Python docstring comments will be coming in a future version.

## Requirements:

- Python 2.7.x

##

![screen shot](https://github.com/freginold/thinIt/blob/master/ss_thinIt_v1_0_0.png)

thinIt is versioned using [Semantic Versioning](http://semver.org/).
