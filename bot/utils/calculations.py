import math

def binaryToDecimal(binaryString):

    exponent = len(binaryString) - 1
    result = 0

    for char in binaryString:
        if char == "1": result += pow(2, exponent)
        exponent -= 1

    return str(result)

def anyBaseToN(base, input):

    exponent = len(input) - 1
    result = 0

    for char in input:
        value = turnLettersToInt(char)
        result += value * pow(base, exponent)
        exponent -= 1

    return str(result)

def turnLettersToInt(letter):

    try:
        return int(letter)
    except:
        if letter.lower() == "a": return 10
        elif letter.lower() == "b": return 11
        elif letter.lower() == "c": return 12
        elif letter.lower() == "d": return 13
        elif letter.lower() == "e": return 14
        elif letter.lower() == "f": return 15
        elif letter.lower() == "g": return 16
        elif letter.lower() == "h": return 17
        elif letter.lower() == "i": return 18
        elif letter.lower() == "j": return 19
        elif letter.lower() == "k": return 20
        elif letter.lower() == "l": return 21
        elif letter.lower() == "m": return 22
        elif letter.lower() == "n": return 23
        elif letter.lower() == "o": return 24
        elif letter.lower() == "p": return 25
        elif letter.lower() == "q": return 26
        elif letter.lower() == "r": return 27
        elif letter.lower() == "s": return 28
        elif letter.lower() == "t": return 29
        elif letter.lower() == "u": return 30
        elif letter.lower() == "v": return 31
        elif letter.lower() == "w": return 32
        elif letter.lower() == "x": return 33
        elif letter.lower() == "y": return 34
        elif letter.lower() == "z": return 35