from appscript import app
import time

# allFolders = app(u'Microsoft Entourage').folders[u'Saved Email'].folders.get()
# allFolders only recurses to messages located 2 levels in from 'Saved Email'
# allFolders = app(u'Microsoft Entourage').folders[u'Saved Email'].folders[u'SYRACUSE'].folders.get()
# allFolders = app(u'Microsoft Entourage').folders[u'Saved Email'].folders[u'WEB'].folders.get()
# allFolders = app(u'Microsoft Entourage').folders[u'Saved Email'].folders[u'WORK'].folders.get()
allFolders = app(u'Microsoft Entourage').folders[u'Saved Email'].folders[u'WORK'].folders[u'CREDENTIALS'].folders.get()
# print allFolders," and length ",len(allFolders)
for i in range(0, len(allFolders)):
    msgId = []
    msgId_header = []
    msgId_received = []
    deleteMsgId = []
    
    msgs = allFolders[i].messages.get()
    for j in range(0, len(msgs)):
        received = msgs[j].time_received.get()
        if str(received) == "1904-01-01 00:00:00":
            # print msgs[j].subject.get()  # these are sent messages
            pass
        else:
            header = msgs[j].headers.get()
            s = header.find("Message-Id: <") + 13
            if s <= 12:
                s = header.find("Message-ID:  <") + 14
            if s <= 12:
                s = header.find("Message-ID: <") + 13
            if s <= 12:
                print header
                print msgs[j].ID_.get()
                break
            e = header.find(">", s)
            msgs[j].ID_.get()
            msgId_header.append(header[s:e])
            struct_time = time.strptime(str(received), "%Y-%m-%d %H:%M:%S")
            epochT = time.mktime(struct_time)
            msgId_received.append(epochT)
            msgId.append(msgs[j].ID_.get())
    if len(msgId) != len(msgId_header):
        print "MISTAKE!! in ID vs. header ID"
        break
    
    for k in range(0, len(msgId)):
        try:
            temp = msgId_header[k]
        except IndexError:
            break
        count = msgId_header.count(temp)
        if count > 1:
            copyList = [], [], []
            while count != 0:
                indexNum = msgId_header.index(temp)
                copyList[0].append(msgId.pop(indexNum))
                copyList[1].append(msgId_header.pop(indexNum))
                copyList[2].append(msgId_received.pop(indexNum))
                count = msgId_header.count(temp)
            newest = 0
            for i in range(0, len(copyList[0])):
                received = copyList[2][i]
                if received > newest:
                    newest = received
            newestIndex = copyList[2].index(newest)
            for j in range(0, len(copyList[0])):
                if j == newestIndex:
                    pass
                else:
                    deleteMsgId.append(copyList[0][j])
    # print deleteMsgId
    for l in range(0, len(deleteMsgId)):
        app(u'Microsoft Entourage').messages.ID(deleteMsgId[l]).delete()
        # print app(u'Microsoft Entourage').folders.ID(110).messages.ID(deleteMsgId[l]).subject.get()
        # print app(u'Microsoft Entourage').folders.ID(110).messages.ID(deleteMsgId[l]).time_received.get()

