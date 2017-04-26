import sys
import json

mode = sys.argv[1]
message = sys.argv[2]
respnse = sys.argv[3]
database = sys.argv[4]

with open(message, 'r') as m:
    msg = json.load(m)

if mode == "handle_message":

    sender = msg["sender"]
    receiver = msg["receiver"]
    msg["receiver"] = sender
    msg["sender"] = receiver

    with open(message, 'w') as m:
        msg = json.dump(msg, m)
    with open(respnse, 'w') as m:
        msg = json.dump({"mode": "reply"}, m)

elif mode == "is_applicable_to":
    with open(respnse, 'w') as m:
        msg = json.dump({"mode": "is_applicable", "applicable": True}, m)
