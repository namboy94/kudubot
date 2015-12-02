import os

def publicLs(input):
    splitInput = input[8:]
    if os.path.isdir(splitInput) or os.path.isfile(splitInput):
        command = "ls " + splitInput
    else:
        command = "echo \"Not a valid directory or file\""
    return command