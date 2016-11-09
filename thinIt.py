
# thinIt, a JS/CSS minifier written in Python 2.7.12


# ------------ Setup ------------------

import os, sys

fileName = ""
jsTextArray = []
jsText = ""
jsMinName = ""
fileType = ""
commentsOpen = False
comment = ""
syntax = '> thinIt.py [fileName] ["optionalCommentText"]'
ver = "v0.1.0"
sizeBefore = ""
sizeAfter = ""


# ------------ Functions ------------------

def getParams():
    # if no file name, display msg
    # get file name, also get optional text
    global fileName, comment
    if len(sys.argv) < 2:
        # no parameters
        print
        print "Please specify a JS or CSS file to minify, in this format:"
        showSyntax()
    if sys.argv[1].lower() == "help" or sys.argv[1] == "?" or sys.argv[1] == "/?":
        print
        print "thinIt is a JavaScript and CSS minifier written in Python 2.7.12."
        print "To use it, please specify a JS or CSS file to minify, in this format:"
        showSyntax()
    fileName = sys.argv[1]
    # check if parameter is a valid file name
    if len(sys.argv) > 2:
        comment = sys.argv[2]

def showSyntax():
    print
    print syntax
    print
    print "  fileName = the JavaScript or CSS file to minify (plus path, if not in the current directory) (in quotes if there are spaces)"
    print "  optionalCommentText = A comment to insert as the first line, i.e. description or version number (optional, in quotes)"
    print
    quit()

def clear():
    # clear screen
    os.system("cls" if os.name == "nt" else "clear")

def getFileType():
    fileExt = jsFile.name.split('.')
    return fileExt[len(fileExt)-1].lower()

def getMinName():
    # get min name - separate name by . then insert ".min" before last one
    newNameArray = jsFile.name.split('.')
    global jsMinName, fileType
    for i in range(0, len(newNameArray)):
        if i < (len(newNameArray)-1):
            jsMinName = jsMinName + newNameArray[i] + "."
        else:
            jsMinName = jsMinName + "min." + fileType

def saveMinFile():
    # create output min file
    outputFile = open(jsMinName, "w")
    outputFile.write(jsText)
    outputFile.close()

def checkForCommentEnd(line):
    global madeAChange, partialLine, jsTextArray, commentsOpen
    for j in range(0, len(jsTextArray[line])):
        # loop through line, if see "*/" anywhere, end of comments
        if jsTextArray[line][j:j+2] == "*/":
            commentsOpen = False
            madeAChange = True
            partialLine = True
            jsTextArray[line] = jsTextArray[line][j+2:]
            break
    if commentsOpen:
        jsTextArray[line] = ""
    
def loopThrough():
    global commentsOpen
    madeAChange = True
    partialLine = False
    while madeAChange:
        madeAChange = False
        for i in range(0, len(jsTextArray)):
            if commentsOpen:
                checkForCommentEnd(i)
            else:
                if jsTextArray[i][0:2] == "//":
                    madeAChange = True
                    jsTextArray[i] = ""
                if jsTextArray[i][0:2] == "/*":
                    madeAChange = True
                    commentsOpen = True
                    checkForCommentEnd(i)
                    continue
                if jsTextArray[i][0:1] == " ":
                    # if first char is space, delete it
                    madeAChange = True
                    partialLine = True
                    jsTextArray[i] = jsTextArray[i][1:]
                if jsTextArray[i][len(jsTextArray[i])-1:len(jsTextArray[i])] == " ":
                    # remove trailing spaces
                    jsTextArray[i] = jsTextArray[i][:(len(jsTextArray[i])-1)]
                    
                # check if partialLine flag is set
                if partialLine:
                    partialLine = False

def makeOutputString():
    # copy minified text into string
    global jsText, comment
    if comment <> "":
        # if a comment will be added
        if fileType == "js":
            comment = "// " + comment
        else:
            comment = "/* " + comment + " */"
        jsText = comment + "\n"
    for i in range(0, len(jsTextArray)):
        # put new lines into a string. if ; at end, don't add \n
        if jsTextArray[i] == "":
            continue
        else:
            if jsTextArray[i][len(jsTextArray[i])-1] == ";":
                jsText = jsText + jsTextArray[i]
            else:
                jsText = jsText + jsTextArray[i] + "\n"

def showResults():
    # show before & after file size, new file name
    print
    print "File minified to: ", jsMinName
    print
    print "File size before minify:   ", sizeBefore
    print "File size after minify:    ", sizeAfter
    print
    print "Compressed", str(percentSmaller) + "%"


# ------------ Start ------------------

clear()
getParams()
jsFile = open(fileName, "r")
jsTextArray = jsFile.read().split('\n')
fileType = getFileType()
getMinName()
jsFile.close()

loopThrough()

makeOutputString()

saveMinFile()

sizeBefore = os.stat(fileName).st_size
sizeAfter = os.stat(jsMinName).st_size
percentSmaller = int(100 - ((sizeAfter * 1.00) / sizeBefore * 100))
sizeBefore = "%s %s" % (sizeBefore, "bytes")
sizeAfter = "%s %s" % (sizeAfter, "bytes")

showResults()
