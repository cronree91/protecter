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

groups = {}


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

def NOTIFIED_INVITE_INTO_GROUP(op):
    print("[GROUP:"+op.param1+"][NAME:"+client.getGroup(op.param1).name+"] "+"[UID:"+op.param2+"]"+"[NAME:"+client.getContact(op.param2).displayName+"] に招待されました。")
    admins,black,bots = readtexts()
    if op.param3 == MySelf.mid:
        if op.param2 in admins:
            print("[GROUP:"+op.param1+"][NAME:"+client.getGroup(op.param1).name+"] "+"[UID:"+op.param2+"]"+"[NAME:"+client.getContact(op.param2).displayName+"]から招待されたグループに入りました")
            client.acceptGroupInvitation(op.param1)
            group = client.getGroup(op.param1)
            groups[op.param1] = client.reissueGroupTicket(op.param1)
            group.preventedJoinByTicket = True
            client.updateGroup(group)
     #        client.sendMessage(op.param1,"@kicker")
        elif op.param2 in bots:
            client.acceptGroupInvitation(op.param1)
        else:
            print("[GROUP:"+op.param1+"][NAME:"+client.getGroup(op.param1).name+"][UID:"+op.param2+"]"+"[NAME:"+client.getContact(op.param2).displayName+"] DONT HAVE TICKET.")
            client.acceptGroupInvitation(op.param1)
            client.sendMessage(op.param1,"権限がありません。")
            client.sendMessage(op.param1,op.param2)
            client.leaveGroup(op.param1)


def RECEIVE_MESSAGE(op):
    admins,black,bots = readtexts()
    msg = op.message
    text = msg.text.lower()
    msg_id = msg.id
    receiver = msg.to
    sender = msg._from
    print(msg.toType)
    print("[GID:"+receiver+"][NAME:"+client.getGroup(receiver).name+"][UID:"+sender+"]"+"[NAME:"+client.getContact(sender).displayName+"] MESSAGE `"+text+"':MID "+msg_id)
    if msg.toType == 2:
        client.sendChatChecked(receiver,msg_id)
        if msg.contentType == 0:
            if sender in admins:
                if text.lower() == "/gid":
                    print("[GID:"+receiver+"][NAME:"+client.getGroup(receiver).name+"] RECEIVE `"+receiver+"'")
                    client.sendMessage(receiver,receiver)
                elif text.lower() == "/mid":
                    print("[GID:"+receiver+"][NAME:"+client.getGroup(receiver).name+"] RECEIVE `"+sender+"'")
                    client.sendMessage(receiver,sender)
                elif text.lower() == "/speed":
                    time0 = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
                    str1 = str(time0)
                    print("[GID:"+receiver+"][NAME:"+client.getGroup(receiver).name+"] RECEIVE `"+str1+"'")
                    client.sendMessage(receiver, str1)
                elif text.lower() == "/hey":
                    client.sendMessage(receiver, "Hi, Here is admin bot")
                elif text.lower() == "/help":
                    print("[GID:"+receiver+"][NAME:"+client.getGroup(receiver).name+"] RECEIVE ")
                    client.sendMessage(receiver, "Help   全てのコマンドはAdminのみ使用可能です\n\n/gid  GroupのIDを表示します\n/mid    このコマンドを送信した人のIDを表示します\n/speed   反応速度を検証します\n/help   ヘルプを表示します\n/kick [ID]  キックしたい人のIDを指定することで、キックできます\n/list   グループに参加している人の名前とIDの一覧を表示します\n/bye   グループから退会します\n/url on    グループへの招待リンクを生成します\n/info   グループの情報を表示します")
                elif text.lower().startswith("/kick "):
                    try:
                        print("[GID:"+receiver+"][NAME:"+client.getGroup(receiver).name+"] [UID:"+text.lower()[6:]+"]"+"[NAME:"+client.getContact(text.lower()[6:]).displayName+"]をキックします")
                        client.kickoutFromGroup(receiver,[text.lower()[6:]])
                        client.sendMessage(receiver, "KICKED")
                    except:
                        print("[GID:"+receiver+"][NAME:"+client.getGroup(receiver).name+"] [UID:"+sender+"]"+"[NAME:"+client.getContact(sender).displayName+"]をキックする過程で、エラーが発生")
                        client.sendMessage(receiver,"Error!")
                elif text.lower() == "/list":
                    lists = []
                    group = client.getGroup(receiver)
                    for g in group.members:
                        lists.append(g.displayName+" :")
                        lists.append("   "+str(g.mid))
                    client.sendMessage(receiver,"\n".join(lists))
                elif text.lower() == "/bye":
                    client.leaveGroup(msg.to)
                elif text.lower() == "/url on":
                    client.sendMessage(receiver, "http://line.me/R/ti/g/" + groups[receiver])
                elif text.lower() == "/info":
                    group = client.getGroup(receiver)
                    client.sendMessage(receiver,"[group name] " + group.name + "\n[group id] " + group.id + "\n人数" + str(len(group.members)))


def NOTIFIED_KICKOUT_FROM_GROUP(op):
    admins,black,bots = readtexts()
    print("[group:"+op.param1+"][NAME:"+client.getGroup(op.param1).name+"] KICOUT [UID:"+op.param3+"]"+"[NAME:"+client.getContact(op.param3).displayName+"] BY [UID:"+op.param2+"][NAME:"+client.getContact(op.param2).displayName+"]")
    if op.param3 == MySelf.mid:
        with open('black.txt','a') as f:
            print(op.param2,file=f)
        client.acceptGroupInvitationByTicket(op.param1, groups[op.param1])
        group = client.getGroup(op.param1)
        client.reissueGroupTicket(op.param1)
        group.preventedJoinByTicket = True
        client.updateGroup(group)
    elif op.param2 in admins:
        client.sendMessage(op.parma1,"@admin, TO KICK USE /kick [mid]")
    elif op.param3 in bots:
        print("BOT KICKED")
    elif op.param2 not in bots:
        client.kickoutFromGroup(op.param1,[op.param2])
        with open('black.txt','a') as f:
            print(op.param2,file=f)
        client.sendMessage(op.param3,"あなたは、グループ［"+client.getGroup(op.param1).name+"］からキックされました。再参加するには、下のURLを利用してください。\n")
        client.sendMessage(op.param3,"http://line.me/R/ti/g/"+groups[op.param1])

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    admins,black,bots = readtexts()
    try:
        if op.param2 in black:
            try:
                client.kickoutFromGroup(op.param1, [op.param2])
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        print ("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return

oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
    OpType.NOTIFIED_KICKOUT_FROM_GROUP: NOTIFIED_KICKOUT_FROM_GROUP,
    OpType.NOTIFIED_ACCEPT_GROUP_INVITATION: NOTIFIED_ACCEPT_GROUP_INVITATION,
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
    })

while True:
    oepoll.trace()
