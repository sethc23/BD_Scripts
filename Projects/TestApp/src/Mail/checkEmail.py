def checkCapatcha(unique):
    import libgmail
    # unique="11230"
    unique = str(unique)
    subject = "capatcha"
    subjectLine = subject + unique
    unreadMsg = "<b>" + subjectLine + "</b>"
    ga = libgmail.GmailAccount("moneypress.1@gmail.com", "muchmoney")
    ga.login()
    folder = ga.getMessagesByFolder("inbox")

    for thread in folder:
        # print thread.subject
        if thread.subject == unreadMsg or thread.subject == subjectLine:
            for msg in thread:
                # print msg
                message = ga.getRawMessage(msg.id)
                subjectContents = "Re: " + subjectLine
                s = message.find(subjectLine)
                s2 = message.find("7bit", s) + 4
                e = message.find("<moneypress.1@gmail.com> wrote", s2)
                cutMessage = message[s2:e]
                e = cutMessage.find("On ")
                answer = cutMessage[:e]
                finalAnswer = answer.strip()
    try:
        finalAnswer = finalAnswer
        return finalAnswer
        # print finalAnswer
    except:
        return None
        # print None

