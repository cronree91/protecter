# -*- coding: utf-8 -*-
from Linephu.linepy import *
from Linephu.akad.ttypes import *
import timeit
from time import strftime
import time

client = LINE()
client.log("Auth Token : " + str(client.authToken))
MySelf = client.getProfile()
oepoll = OEPoll(client)


def readtexts():
    f = open("admins.txt")
    admins = f.read().rstrip('\n').split('\n')
    f.close
    f = open("black.txt")
    black = f.read().rstrip('\n').split('\n')
    f.close
    f = open("bots.txt")
    bots = f.read().rstrip('\n').split('\n')
    f.close
    bots.remove(MySelf.mid)
    return admins,black,bots

def RECEIVE_MESSAGE(op):
    admins,black,bots = readtexts()
    msg = op.message
    text = msg.text.lower()
    msg_id = msg.id
    receiver = msg.to
    sender = msg._from
    if msg.toType == 2:
        if msg.contentType == 0:
            if text.lower() == "@kicker":
                group = client.getGroup(op.param1)
                group.preventedJoinByTicket = False
                str1 = client.reissueGroupTicket(op.param1)
                client.updateGroup(group)
                client.sendMessage(receiver,"@adbot "+str1)

oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE
    })

while True:
    oepoll.trace()
