import sys

from utils.help import printHelp
from utils.input import readConfigFile, parseInput
from utils.version import printVersion


# Check if there's a parameter being passed for current option
def checkIfParamExists(i: int):
    return len(sys.argv) > i and not sys.argv[i].startswith("-")


try:
    isShowHelp = False
    isShowVersion = False
    inputConfigFile = ""
    inputPath = ""
    inputLang = ""
    unkownArg = ""
    unprovidedArg = ""
    # Extracts all arguments from Command Line
    i = 0
    for arg in sys.argv:
        i += 1  # Uses an index to trace current item in argv so that we know the index of next item.
        if arg.startswith("-"):
            if arg == "-h" or arg == "--help":
                isShowHelp = True
            elif arg == "-v" or arg == "--version":
                isShowVersion = True
            elif arg == "-c" or arg == "--config":
                if checkIfParamExists(
                    i
                ):  # Checks if current option has a valid parameter.
                    inputConfigFile = sys.argv[i]
                else:
                    unprovidedArg = arg
            elif arg == "-i" or arg == "--input":
                if checkIfParamExists(
                    i
                ):  # Checks if current option has a valid parameter.
                    inputPath = sys.argv[i]
                else:
                    unprovidedArg = arg
            elif arg == "-l" or arg == "--lang":
                if checkIfParamExists(i):
                    inputLang = sys.arv[i]
            else:
                unkownArg = arg
    if len(unprovidedArg):
        raise SystemExit("No parameter is provided for" + unprovidedArg)
    elif len(unkownArg):
        raise SystemExit("No option for " + unkownArg)
    elif isShowHelp:
        printHelp()
    elif isShowVersion:
        printVersion()
    elif len(inputConfigFile):
        readConfigFile(inputConfigFile)
    elif len(inputPath):
        parseInput(inputPath, inputLang)
    else:
        raise SystemExit(
            "No arguments were passed if unsure about which aurgument are avialable use -h or --help"
        )
except SystemExit as err:
    print(err)
except IndexError as indexErr:
    print(indexErr)
