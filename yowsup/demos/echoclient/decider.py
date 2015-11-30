def decide(messageProtocolEntity):

    sentmessage = messageProtocolEntity.getBody()
    sender = messageProtocolEntity.getFrom(False)
    sendername = adressbook(sender)
    decision = ["", sender, ""]

    print("recv: " + sendername + ": " + sentmessage.lower())

    # Instant replies
    if "keks" in sentmessage.lower() or "cookie" in sentmessage.lower(): decision[0] = "Ich will auch Kekse!"
    elif "kuchen" in sentmessage.lower(): decision[0] = "Ich mag Kuchen."
    elif "wã¼rfel" in sentmessage.lower() or "wuerfel" in sentmessage.lower(): decision[0] = "https://play.google.com/store/apps/details?id=com.namibsun.android.dice"
    elif "ð" in sentmessage.lower(): decision[0] = "ððð"

    #terminal commands
    elif "term: " in sentmessage.lower() and sendername.split(" ")[0] == "Hermann":
        decision[2] = sentmessage.lower().split("term: ")[1]
    elif sentmessage.lower().startswith("term: "):
        command = sentmessage.lower().split("term: ")[1]
        if command.startswith("ls") \
                or command.startswith("man") \
                or command.startswith("cat"):
            decision[2] = command
        else: decision[0] = "Invalid command"


    if decision[0]: print("sent: " + sendername + ": " + decision[0])
    elif decision[2]: print("cmnd: " + decision[2])

    return decision


def adressbook(adress):
    if adress == "4915779781557-1418747022":    return "Land of the very Brave      "
    elif adress == "4917628727937-1448730289":  return "Bottesting                  "
    elif adress == "4917628727937":             return "Hermann                     "
    else: return adress

def sizeChecker(string):
    if len(string) > 500: return "Message too long to send"
    else: return string