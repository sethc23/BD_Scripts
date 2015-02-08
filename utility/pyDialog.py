


def askQuestion(question, followup, answerList):
    print ''
    print question
    print ''
    step = raw_input(":")
    if type(answerList[0]) == str:
        while answerList.count(str(step)) == 0:
            print followup
            print ''
            step = raw_input(":")
    elif type(answerList[0]) == list:
        while answerList.count(eval(str(step))) == 0:
            print followup
            print ''
            step = raw_input(":")
    return step

def multiQuestion(question, answerList):
    print ''
    print question
    print ''
    for i in range(1, len(answerList) + 1):
        print str(i) + '.\t' + str(answerList[i - 1]).capitalize()
    step = raw_input(":")
    if type(answerList) == list:
        while range(1, len(answerList) + 1).count(eval(str(step))) == 0:
            print 'What number?'
            print ''
            step = raw_input(":")
    return step
