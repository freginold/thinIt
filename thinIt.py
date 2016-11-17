
# thinIt, a JS/CSS minifier written in Python 2.7.12


# ------------ Setup ------------------

import os, sys, re

fileName = ""
jsTextArray = []
jsText = ""
jsMinName = ""
fileType = ""
commentsOpen = False
madeAChange = True
comment = ""
syntax = '> thinIt.py [fileName] ["optionalCommentText"]'
ver = "v0.1.0"
sizeBefore = 0
sizeAfter = 0
percentSmaller = 0
alphanumerics = re.compile('[A-Za-z0-9_\.$]+')

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

def checkForCommentEnd(thisLine):
    global madeAChange, jsTextArray, commentsOpen
    for j in range(0, len(thisLine)):
        # loop through line, if see "*/" anywhere, end of comments
        if thisLine[j:j+2] == "*/":
            madeAChange = True
            commentsOpen = False
            thisLine = thisLine[j+2:]
            break
    if commentsOpen:
        thisLine = ""
    return thisLine

def removeLeadingSpace(thisLine):
    # check for & remove leading space
    global madeAChange
    if thisLine[0:1] == " ":
        madeAChange = True
        return thisLine[1:]
    else:
        return thisLine

def removeTrailingSpace(thisLine):
    # check for & remove trailing space
    global madeAChange
    if thisLine[len(thisLine)-1:len(thisLine)] == " ":
        madeAChange = True
        return thisLine[:(len(thisLine)-1)]
    else:
        return thisLine

def removeLeadingTab(thisLine):
    # check for & remove leading tab
    global madeAChange
    if thisLine[0:1] == chr(9):
        madeAChange = True
        return thisLine[1:]
    else:
        return thisLine

def removeTrailingTab(thisLine):
    # check for & remove trailing tab
    global madeAChange
    if thisLine[len(thisLine)-1:len(thisLine)] == chr(9):
        madeAChange = True
        return thisLine[:(len(thisLine)-1)]
    else:
        return thisLine

def removeIndentedComment(thisLine):
    # check for indented Python comments & remove them
    # this function has to be called after checking for 1st char comment, otherwise those will be skipped
    returnLine = ""
    for j in range(0, len(thisLine)):
        # loop through line, if see "#" after just spaces or tabs, remove the line
        if thisLine[j:j+1] == " " or thisLine[j:j+1] == chr(9):
            # if char is a space or tab, keep checking
            if thisLine[j+1:j+2] == "#":
                # if found a comment
                returnLine = ""
                break
            else:
                continue
        else:
            # if not a space or tab, skip this line
            returnLine = thisLine
            break
    return returnLine

def removeInternalSpaces(thisLine):
    # remove spaces between non-alphanumeric characters; *** for JS, check to be sure not in quotes first
    global madeAChange
    if len(thisLine) < 3:
        return thisLine
    newLine = thisLine[0]
    for j in range(1, len(thisLine)-1):
        # loop through line, remove unnecessary spaces
        if thisLine[j] == " ":
            if (alphanumerics.search(thisLine[j-1])) and (alphanumerics.search(thisLine[j+1])):
                # if characters on both sides of space are alphanumeric, keep the space
                newLine = newLine + thisLine[j]
            else:
                # else, skip the space
                madeAChange = True
                continue
        else:
            newLine = newLine + thisLine[j]
    newLine = newLine + thisLine[len(thisLine)-1]
    return newLine

def removeInternalJSComments(line):
    # remove /* */ comments that may not be at the beginning of the line
    global madeAChange, commentsOpen
    for j in range(0, len(jsTextArray[line]) - 1):
        # loop through line to see if see /*
        if jsTextArray[line][j:j+2] == "/*":
            commentsOpen = True
            madeAChange = True            
            # call checkforcommentend with string from j onward; if it returns empty string (no comment end) delete line from j onward; else concatenate
            # beginning up to j, plus part that was returned
            tempString = checkForCommentEnd(jsTextArray[line])
            if tempString == "":
                # no comment end
                return jsTextArray[line][0:j]
            else:
                # if found comment end
                return jsTextArray[line][0:j] + tempString
    return jsTextArray[line]

def condenseLines(num):
    # for lines that don't end w/ a letter or number, check next non-blank char to be sure not alphanumeric; if not, consolidate the lines
    # for: JS, CSS
    global jsText
    # for making output string, loop through chars & lines after current EOL & make sure that next non-blank char is not alphanumeric
    doneChecking = False
    for j in range(num + 1, len(jsTextArray)-1):
        # loop through rest of the lines until find a non-blank character
        for k in range(0, len(jsTextArray[j])-1):
            if jsTextArray[j][k] == "" or jsTextArray[j][k] == " " or jsTextArray[j][k] == chr(10) or jsTextArray[j][k] == chr(13):
                # if a space or line end
                continue
            elif alphanumerics.search(jsTextArray[j][k]):
                # if it's an alphanumeric character
                jsText = jsText + jsTextArray[num] + " "
                doneChecking = True
                break
            else:
                # if not alphanumeric character
                jsText = jsText + jsTextArray[num]
                doneChecking = True
                break
        if doneChecking:
            break
    if not doneChecking:
        jsText = jsText + jsTextArray[num]

def checkForInternalSingleComment(thisLine):
    # check for single-line comment somewhere in line other than at beginning
    # use fileType to determine if looking for // or #
    # ** if changing to do this in the while function, have to check to be sure not in quotes first **
    for k in range(0, len(thisLine)):
        # loop through line looking for comment start
        if fileType[0:2] == "py":
            if thisLine[k] == "#":
                return True
        if fileType == "js":
            if thisLine[k:k+2] == "//":
                return True
    return False

def loopThrough():
    global commentsOpen, madeAChange, fileType
    while madeAChange:
        madeAChange = False
        commentsOpen = False
        for i in range(0, len(jsTextArray)):
            # loop through the lines in the file
            if jsTextArray[i] == chr(13) or jsTextArray[i] == chr(10) or jsTextArray[i] == "":
                # if an empty line, skip it
                jsTextArray[i] = ""
                continue
            if commentsOpen:
                # if currently in a comment that could be multi-line
                jsTextArray[i] = checkForCommentEnd(jsTextArray[i])
            else:
                # if not currently in a comment, check for beginning of a comment
                if jsTextArray[i][0:2] == "//" and fileType == "js":
                    madeAChange = True
                    jsTextArray[i] = ""
                    continue
                if jsTextArray[i][0:1] == "#" and fileType[0:2] == "py":
                    madeAChange = True
                    jsTextArray[i] = ""
                    continue
                if jsTextArray[i][0:1] == "'" and fileType[0:2] == "vb":
                    madeAChange = True
                    jsTextArray[i] = ""
                    continue
                if jsTextArray[i][0:2] == "/*" and (fileType == "js" or fileType == "css"):
                    madeAChange = True
                    commentsOpen = True
                    jsTextArray[i] = checkForCommentEnd(jsTextArray[i])
                    continue

                jsTextArray[i] = removeTrailingSpace(jsTextArray[i])
                jsTextArray[i] = removeTrailingTab(jsTextArray[i])
                
                # language-specific checks
                if fileType == "js":
                    jsTextArray[i] = removeLeadingSpace(jsTextArray[i])
                    jsTextArray[i] = removeLeadingTab(jsTextArray[i])
                    jsTextArray[i] = removeInternalJSComments(i);
                    #jsTextArray[i] = removeInternalSpaces(jsTextArray[i])
                    # --- check to be sure not in quotes first
                if fileType == "css":
                    jsTextArray[i] = removeLeadingSpace(jsTextArray[i])
                    jsTextArray[i] = removeLeadingTab(jsTextArray[i])
                    jsTextArray[i] = removeInternalJSComments(i);
                    jsTextArray[i] = removeInternalSpaces(jsTextArray[i])
                if fileType[0:2] == "py":
                    jsTextArray[i] = removeIndentedComment(jsTextArray[i])
                if fileType[0:2] == "vb":
                    jsTextArray[i] = removeLeadingSpace(jsTextArray[i])
                    jsTextArray[i] = removeLeadingTab(jsTextArray[i])

def makeOutputString():    
    # copy minified text into string
    # if do away with this function for performance reasons, just write array to file with "\n", " ", or nothing between lines
    global jsText, comment, fileType
    if comment <> "":
        # if a comment will be added
        if fileType == "js":
            comment = "// " + comment
        if fileType[0:2] == "py":
            comment = "#" + comment
        if fileType[0:2] == "vb":
            comment = "'" + comment
        else:
            comment = "/* " + comment + " */"
        jsText = comment + "\n"
    for i in range(0, len(jsTextArray)):
        # put new lines into a string. if ; at end, don't add \n
        if jsTextArray[i] == "":
            continue
        else:
            if (fileType == "js" or fileType == "css"):
                # if a JS/CSS file
                if i < len(jsTextArray)-1:
                    # if not the last line
                    if (alphanumerics.search(jsTextArray[i][len(jsTextArray[i])-1])) and (alphanumerics.search(jsTextArray[i+1][0:1])):
                        # if both are alphanumeric, don't consolidate the lines
                        if checkForInternalSingleComment(jsTextArray[i]):
                            jsText = jsText + jsTextArray[i] + "\n"
                        else:
                            jsText = jsText + jsTextArray[i] + " "
                    else:
                        if alphanumerics.search(jsTextArray[i][len(jsTextArray[i])-1]):
                            # if last char is alphanumeric but 1st char on next line isn't:
                            if checkForInternalSingleComment(jsTextArray[i]):
                                jsText = jsText + jsTextArray[i] + "\n"
                            else:
                                condenseLines(i)
                        else:
                            # if neither are alphanumeric
                            jsText = jsText + jsTextArray[i]
                else:
                    # if the last line
                    jsText = jsText + jsTextArray[len(jsTextArray)-1]
            else:
                # for other file types
                jsText = jsText + jsTextArray[i] + "\n"

def getSizes():
    global sizeBefore, sizeAfter, percentSmaller
    sizeBefore = os.stat(fileName).st_size
    sizeAfter = os.stat(jsMinName).st_size
    percentSmaller = int(100 - ((sizeAfter * 1.00) / sizeBefore * 100))
    sizeBefore = "%s %s" % (sizeBefore, "bytes")
    sizeAfter = "%s %s" % (sizeAfter, "bytes")

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

getSizes()

showResults()
