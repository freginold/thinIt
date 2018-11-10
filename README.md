# thinIt
thinIt is an extremely basic minifier written in Python.

## Syntax

From the command line, run:

`thinit.py [filename] ["optional comment text"]`

- `filename` -- Name of the file to minify. Include the file path if not in the current directory (with quotes, if there are spaces).
- `"optional comment text"` -- If you want to insert a comment at the beginning of the minified file (to reference the version number, date, etc.) include it here, in quotes.

*Example:*

`thinit.py test.js "Test file v1.0"`

Typing `thinit.py help` will bring up a brief help screen.

## Output

When executed, thinIt will create a minified version of the specified file. The new file will have the same name as the original file, with `.min` inserted before the extension. Minifying `test.js` will result in a new file named `test.min.js`.

On completion, thinIt will display the new file name, the original file size, the new file size, and the percent that the file was compressed.

![screen shot](https://github.com/freginold/thinIt/blob/master/ss_thinIt_v1_0_0.png)

## Supported File Types

thinIt was mainly designed to work with JavaScript (`.js`) and CSS (`.css`) files. It also has rudimentary support for Python (`.py\*`) and VBScript (`.vb\*`) files. For Python it removes blank lines and lines that begin with a comment, and for VBScript it removes blank lines, lines that begin with a comment, and indentations. Support for Python docstring comments will be coming in a future version.

## Requirements

- Python 2.7.x

## Versioning

thinIt is versioned using [Semantic Versioning](http://semver.org/).
