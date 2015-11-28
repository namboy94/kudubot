def decide(messageProtocolEntity):

    sentmessage = messageProtocolEntity.getBody()
    sender = messageProtocolEntity.getFrom(False)
    decision = ["",sender,""]

    if "keks" in sentmessage.lower():
        decision[0] = "Ich will auch Kekse!"
    elif "kuchen" in sentmessage.lower():
        decision[0] = "Ich mag Kuchen."
    elif "rsync-backup" == sentmessage and sender == "4917628727937":
        decision[2] = "rsync-backup-local"
    elif "wã¼rfel" in sentmessage.lower() or "wuerfel" in sentmessage.lower():
        decision[0] = "https://play.google.com/store/apps/details?id=com.namibsun.android.dice"
    else:
        print("illegal action " + sentmessage.lower())

    return decision
