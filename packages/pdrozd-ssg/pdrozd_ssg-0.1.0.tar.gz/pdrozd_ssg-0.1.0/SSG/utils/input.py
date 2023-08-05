import json
from os.path import exists
import os
import shutil
import codecs
import markdown


def parseInput(arg, lang="en-CA"):
    global newDir  # Creates a new Directory for the output
    global newlang
    newDir = os.path.join(os.path.abspath(os.getcwd()), "dist")
    newlang = lang if len(lang) != 0 else "en-CA"

    if os.path.exists(
        newDir
    ):  # Checks if dist is already a directory if it is it is removed
        shutil.rmtree(newDir)
    os.mkdir(newDir)

    if os.path.isfile(arg):  # added this incase passed argument is absolute path
        parseFile(arg)
    elif os.path.isdir(arg):  # added this incase passed argument is absolute path
        parseDirectory(arg)
    else:  # If passed argument is not absolute create an absolute path for it
        path = os.path.join(
            os.path.abspath(os.getcwd()), arg
        )  # Creates a path for the file or directory

        if os.path.isfile(path):  # Checks if file or directory
            parseFile(path)
        elif os.path.isdir(path):
            parseDirectory(path)
        else:
            raise SystemExit(
                "Input file or directory dosen't exsit (make sure file extension is included)"
            )
    createIndex()


def readConfigFile(arg=""):
    if len(arg) != 0:
        if exists(arg):
            if os.path.isfile(arg):
                with open(arg) as jsonFile:
                    if jsonFile.readable():
                        jsonMap = json.load(jsonFile)
                        if len(jsonMap) == 0:
                            raise SystemExit(
                                "Config file doesn't contain necessary input and output arguments."
                            )
                        else:
                            input = (
                                jsonMap["input"]
                                if jsonMap.__contains__("input")
                                else ""
                            )
                            # Check if argument "input" is included in the config file
                            lang = (
                                jsonMap["lang"] if jsonMap.__contains__("lang") else ""
                            )
                            # Check if argument "lang" is included in the config file.
                            if len(input) != 0:
                                parseInput(input, lang)
                            else:
                                raise SystemExit(
                                    "Input file is not included in the config file."
                                )

                    else:
                        raise SystemExit(
                            "Can't read file "
                            + arg
                            + " , please make sure you have the read permission to the file."
                        )

            else:
                raise SystemExit(arg + " is a directory, please provide a config file.")

        else:
            raise SystemExit("Can't find a valid config file in " + arg)
    else:
        raise SystemExit(
            "Config file is not provided, please make sure to pass a valid config file."
        )


def parseFile(arg):
    with codecs.open(arg, "r", encoding="utf-8") as file:
        lines = file.read().splitlines()

        try:
            fileName = lines[0]
            fullName = os.path.join(newDir, fileName + ".html")

            header = (
                """<!doctype html>
<html lang="""
                + newlang
                + """>
<head>
<meta charset="utf-8">
<meta name="description" content="P-DR0ZD Static Site Generator """
                + fileName
                + """ Page ">
<meta name="robots" content="noindex, nofollow" />
<title>"""
                + fileName
                + """</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<h1>"""
                + fileName
                + """</h1>
<br>
<br>
<p>
"""
            )
            footer = "</p>\n</body>\n</html>"
            if os.path.splitext(arg)[1] == ".txt":
                with open(fullName, "w", encoding="utf-8") as site:
                    site.write(header)
                    for line in lines[
                        1:
                    ]:  # Loops through the list to fill out the html
                        if line != "":
                            site.write(line)
                        else:
                            site.write("</p>\n<p>")

                    site.write(footer)  # Finishes the document with a body
                    if not site.closed:
                        site.close()
            elif os.path.splitext(arg)[1] == ".md":
                with codecs.open(fullName, "w", encoding="utf-8") as site:
                    site.write(header)
                    # Using The markdown parser requiers the list to be in a string format so i used join
                    site.write(markdown.markdown("\n ".join(lines[1:])))
                    site.write(footer)  # Finishes the document with a body
                    if not site.closed:
                        site.close()
            else:
                print("Unable to Proccses " + arg + " because its not a text file")
            if not file.closed:
                file.close()
        except IndexError:
            print("File: " + arg + " is empty")


def parseDirectory(arg):

    allFiles = os.listdir(arg)  # Grabs everything in the directory into a list

    for (
        file
    ) in (
        allFiles
    ):  # Checks if file is a directory or file if it's a directory call parse directory recursively
        tmp = os.path.join(arg, file)
        if os.path.isfile(tmp):
            parseFile(tmp)
        elif os.path.isdir(tmp):
            parseDirectory(tmp)
        else:
            raise SystemExit(
                "Input file or directory dosen't exsit (make sure file extension is included)"
            )


def createIndex():
    allFiles = os.listdir(newDir)

    if allFiles:
        fullName = os.path.join(newDir, "index.html")

        with codecs.open(fullName, "w", encoding="utf-8") as index:
            index.write(
                """<!doctype html>
<html lang="""
                + newlang
                + """>
<head>
<meta charset="utf-8">
<meta name="description" content="P-DR0ZD Static Site Generator Index Please Select the page you want">
<meta name="robots" content="index, follow" />
<title> Index </title>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<h1> Index </h1>
<br>
<br>
<ol>
"""
            )
            for file in allFiles:  # Loops through the list to fill out the html
                index.write('<li><a href="' + file + '">' + file + "</a></li>\n")
            index.write(
                """</ol>
</body>
</html>"""
            )  # Finishes the document with a body
            if not index.closed:
                index.close()
    else:
        raise SystemExit()
