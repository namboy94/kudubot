def fixBrokenUnicode(brokenEmoji):

    byteEmoji = bytes(brokenEmoji, 'utf-8')
    goodByteEmoji = []
    i = 0

    while i < len(byteEmoji):
        if not byteEmoji[i] == 194:
            if byteEmoji[i] == 195:
                i += 1
                goodByteEmoji.append(byteEmoji[i] + 64)
            else:
                goodByteEmoji.append(byteEmoji[i])
        i += 1

    goodByteEmoji = bytes(goodByteEmoji)
    return goodByteEmoji.decode()



def convertToBrokenUnicode(emojis, amount=1):

    byteEmoji = bytes(emojis, 'utf-8')
    goodByteEmoji = []
    i = 0

    while i < len(byteEmoji):
        if i % (len(byteEmoji) / amount) == 0:
            if(len(goodByteEmoji) > 0): goodByteEmoji.pop()
            goodByteEmoji.append(195)
            goodByteEmoji.append(byteEmoji[i] - 64)
        else:
            goodByteEmoji.append(byteEmoji[i])
        goodByteEmoji.append(194)
        i += 1

    goodByteEmoji.pop()

    goodByteEmoji = bytes(goodByteEmoji)
    return goodByteEmoji.decode()