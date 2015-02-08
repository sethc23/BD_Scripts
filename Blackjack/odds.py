from random import choice as rc
from random import shuffle as sh
from sys import exit,path
import numpy as np
path.append('/Users/admin/SERVER2/BD_Scripts/utility')
from variables import copyList, listFin, listFout, arrayFin, arrayFout


def total(hand):
    # how many aces in the hand
    aces = hand.count(11)
    # to complicate things a little the ace can be 11 or 1
    # this little while loop figures it out for you
    t = sum(hand)
    # you have gone over 21 but there is an ace
    if t > 21 and aces > 0:
        while aces > 0 and t > 21:
            # this will switch the ace from 11 to 1
            t -= 10
            aces -= 1
    return t
def lowest_chance():
    return 1.0e-6 #one billion
    #return 5.706998236263609e-09  # odds of winning powerball

def new_deck(decks):
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    card_deck = []
    for i in range(0, decks):
        for j in range(0, 4):
            card_deck.extend(cards)
            
    sh(card_deck) 
    return card_deck
def get_card_vals(card):
    cards = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    card_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    if type(card) != list:
        return card_vals[cards.index(str(card))]
    else:
        return [card_vals[cards.index(str(card[i]))] for i in range(0, len(card))]
def get_card(card_val, set=False):
    card_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    if set == True: return cards
    if type(card_val) != list:
        return cards[card_vals.index(int(card_val))]
    else:
        return [cards[card_vals.index(int(card_val[i]))] for i in range(0, len(card_val))]

# def all_pair_list():
#     pairs=[[],[]] # CARD VALUE, CARD FACE
#     cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
#     for x in cards:
#         for y in cards:
#             if pairs[1].count([x,y]) == 0 and pairs[1].count([y,x]) == 0:
#                 pairs[1].append([x,y])
#                 pairs[0].append([get_card_vals(y),get_card_vals(y)])
#     return pairs

# def all_value_pair_list():
#     pairs=[] # CARD VALUE
#     card_vals=range(2,12)
#     print card_vals
#     for x in card_vals:
#         for y in card_vals:
#             if pairs.count([x,y]) == 0 and pairs.count([y,x]) == 0:
#                 pairs.append([x,y])
#     return pairs

# def get_ALL_odds(card_deck,hands,faces=True): # based on CARD FACE
#     print len(card_deck)
#     if faces==True:
#         
#         # hands = CARD VALUE, CARD FACE
#         hand_Combo_Odds=[[],[],[]]
#         print len(hands[0]),len(hands[1])
#         temp_deck=copyList(card_deck)
#         temp_hand_odds=get_prob(temp_deck, face=True, start_prob=1, verbose=True) # CARD VALUE - HAND ODDS
#         for it in hands[1]:
#             for card in it:
#                 
#                 
#                 next_hand_odds=get_prob(temp_deck, face=True, start_prob=1, verbose=True) # CARD VALUE - HAND ODDS
# 
#             for card in it:
#                 start_prob=temp_hand_odds[0].index(it[0])
#                 if temp_deck.count(card) == 0: 
#                     total_odds=0
#                     break
#                 else:
#                     odds=float(temp_deck.count(card)) / float(len(temp_deck)) # BASED ON CARD FACE
#                     temp_deck.pop(temp_deck.index(card))
#                     total_odds=total_odds*odds
#             hand_Combo_Odds[0].append(get_card_vals(it))#hands[0][hands[1].index(it)]))
#             hand_Combo_Odds[1].append(total_odds)
#             hand_Combo_Odds[2].append(it)
#         return hand_Combo_Odds
#     if faces == False:
#         # hands = CARD VALUE
#         print len(card_deck)
#         hand_Combo_Odds=[[],[]]
#         for it in hands:
#             temp_deck=[get_card_vals(x) for x in card_deck]
#             total_odds=0
#             for card in it:
#                 if temp_deck.count(card) == 0: 
#                     total_odds=0
#                     break
#                 else:
#                     odds=float(temp_deck.count(card)) / float(len(temp_deck))
#                     temp_deck.pop(temp_deck.index(card))
#                     if total_odds == 0:  total_odds += odds # BASED ON CARD VALUE
#                     else: total_odds=total_odds*odds
#             hand_Combo_Odds[0].append(it)
#             hand_Combo_Odds[1].append(total_odds)
#         return hand_Combo_Odds        
#     # CARD VALUEs - ODDS/PERCENT

def get_prob(card_deck, face=True, start_prob=1, verbose=False):  
    # always returns probability of ALL CARDS in AVAILABLE deck
    if verbose==True: print '\n<---- START get_prob ----'
    if face == False: possible_cards = range(2,12)
    if face == True: possible_cards = get_card("", set=True)
    temp_deck=copyList(card_deck)
    if face == False: 
        if type(temp_deck[0]) == str: temp_deck = [get_card_vals(x) for x in temp_deck]
    temp_deck.sort()
    prob = [[], []]
    check_percent = 0
    for x in possible_cards:  # important to save FACE, otherwise no difference between J and Q
        if prob[0].count(x) == 0:
            prob[0].append(x)
            card_prob = float(temp_deck.count(x)) / float(len(temp_deck))
            prob[1].append(card_prob * start_prob)
            check_percent += float(card_prob) * float(start_prob)
    if verbose==True: print 'start percent == total percent :',start_prob,' == ',check_percent
    if verbose==True: print 'number of hand=',len(prob[0]),'=',prob[0]
    if verbose==True: print '---- get_prob END ---->\n'
    if str(check_percent/start_prob) != str(1.0):
        print check_percent/start_prob
        print check_percent/start_prob
        exit(0)
    return prob

def add_prob(ht, card_prob, set):
    # ht=hand_total
    # set[0] = hand_vals
    # set[1] = hand_probs
    # card_prob[0] = card_vals
    # card_prob[1] = card_probs  
    if type(set[0]) != list:
        temp_set = [set, []]
        for i in range(0, len(set)): temp_set[1].append(0)
        set = temp_set
    for i in range(0, len(card_prob[0])):
        if card_prob[1][i] != 0:
            total = ht + card_prob[0][i]
            if total >= 22:
                setIndex = len(set[0]) - 1
                set[1][setIndex] = float(set[1][setIndex]) + float(card_prob[1][i])
            elif set[0].count(total) != 0:
                setIndex = set[0].index(total)
                set[1][setIndex] = float(set[1][setIndex]) + float(card_prob[1][i])
    return set
 
def update_hand_prob(temp_cards, hand_prob, temp_prob, printout=False): 
    for i in range(0, len(temp_prob[0])):
        if temp_prob[1][i] != 0:
            hand_sum = temp_prob[0][i] + sum(get_card_vals(temp_cards))
            # print 'hand sum=',temp_prob[0][i],hand_sum
            if hand_sum >= 22: handIndex = hand_prob[0].index(22)
            else: handIndex = hand_prob[0].index(hand_sum)
            temp_hand = [x for x in get_card_vals(temp_cards)]
            temp_hand.extend([temp_prob[0][i]])
            # if combination not included, add combo
            if hand_prob[2][handIndex].count(temp_hand) == 0:
                hand_prob[1][handIndex] = hand_prob[1][handIndex] + temp_prob[1][i]
                hand_prob[2][handIndex].append(temp_hand)
    if printout == True:
        print '---hand_prob---'
        print 'HAND', '\t', 'PROBABILITY', '\t', 'CARDS'
        for i in range(0, len(hand_prob[0])):
            if hand_prob[1][i] == 0: print hand_prob[0][i], '\t', hand_prob[1][i], '\t\t', hand_prob[2][i]
            else: print hand_prob[0][i], '\t', hand_prob[1][i], '\t', hand_prob[2][i]
        print '<---hand_prob--->'
    return hand_prob

def update_combos(hand_combos, play_cards, temp_card_prob, face=True, printout=False): 
    if printout == True: print 'len update combo iteration',len(temp_card_prob[0])
    new_hand_combos=[[],[]] # CARDS BY VALUE - HAND ODDS 
    if face == False:
        for i in range(0, len(hand_combos)):
            # PREPARE DECK FOR EVALUATING CURRENT HAND
            temp_deck_vals=copyList(play_cards)
            popList=[]
            for it in hand_combos:
                popList.append(temp_deck_vals.index(it))
            popList.reverse()
            for it in popList: temp_deck_vals.pop(it)
             
            # CONSIDER ALL NEXT CARDS FOR PARTICULAR HAND
            check_percent=0
            temp_odd=temp_card_prob[i]
            for j in range(2,12):
                if temp_deck_vals.count(j) == 0: pass
                else:
                    # REMOVE FROM DECK, ADD CARD TO HAND
                    next_deck_vals=copyList(temp_deck_vals)
                    hand_combos[i].append(next_deck_vals.pop(next_deck_vals.index(j)))
 
                    # CALC. ODD FOR HAND, UPDATE ODDS
                    # CREATE CHECK WHERE SUM OF "j" ITERATION SHOULD EQUAL temp_card_prob[i]
                    odds=temp_card_prob[i]*(float(temp_deck_vals.count(i)) / float(len(temp_deck_vals)))
                    temp_card_prob[i]=odds
                    check_percent+=odds
            print temp_odd,'=?=',check_percent
        return  [hand_combos,temp_card_prob]
    if face == True:
        for i in range(0, len(temp_card_prob[0])):
            if temp_card_prob[1][i] != 0:
                play_cards_val = [get_card_vals(x) for x in play_cards]
                temp_hand = get_card_vals(temp_card_prob[0][i]) + sum(play_cards_val)
                temp_cards=copyList(play_cards)
                temp_cards.extend([temp_card_prob[0][i]])
                hand_combos[0].append(temp_hand)
                hand_combos[1].append(temp_card_prob[1][i])
                hand_combos[2].append(temp_cards)
                # hand_combos = [ value of cards , odds of catching hand , each card in hand ]
    if printout == True:
        print '---Combo_Prob---'
        print 'HAND', '\t', 'PROBABILITY', '\t', 'CARDS'
        for i in range(0, len(hand_combos[0])):
            if hand_combos[1][i] == 0: print hand_combos[0][i], '\t', hand_combos[1][i], '\t\t', hand_combos[2][i]
            else: print hand_combos[0][i], '\t', hand_combos[1][i], '\t', hand_combos[2][i]
        print '<---Combo_Prob--->'
    return hand_combos
     

def create_lower_set(hand_combos, lower_set,face=True,verbose=False):
    if verbose == True: print 'UPDATE LOWER-- before update',len(hand_combos[0]),len(lower_set[0])
    # face=True --> hand_combos = CARD VALUES - ODDS/PERCENT - CARD FACES
    # face=False --> hand_combos = CARD VALUES - ODDS/PERCENT
    all_hands=copyList(hand_combos)
    hands=hand_combos
    popList = []
    if face==False:
        for i in range(0, len(hands[0])):
            if sum(hands[0][i]) < 17:
                popList.append(i)
            elif sum(hands[0][i]) >= 22:
                if hands[0][i].count(11) != 0:
                    hands[0][i][hands[0][i].index(11)] = 1
                    popList.append(i)
        popList.reverse()
        for it in popList:
            # move from hand_combos to lower_set
            lower_set[0].append(hands[0].pop(it))
            lower_set[1].append(hands[1].pop(it))
    if face==True:
        for i in range(0, len(hands[0])):
            if sum(hands[0][i]) < 17:
                popList.append(i)
            elif sum(hands[0][i]) >= 22:
                if hands[0][i].count(11) != 0:
                    hands[0][i][hands[0][i].index(11)] = 1
                    popList.append(i)
        popList.reverse()
        for it in popList:
            # move from hand_combos to lower_set
            lower_set[0].append(hands[0].pop(it))
            lower_set[1].append(hands[1].pop(it))
            lower_set[2].append(hands[2].pop(it)) 
    upper_set=hand_combos
    if verbose == True: print 'UPDATE LOWER-- after update',len(hand_combos[0]),len(lower_set[0])
    return all_hands,upper_set,lower_set
      #should delete

def update_sets(upper_set,new_sets,face=True,verbose=False):
    if verbose == True: print 'UPDATE -- before update',len(upper_set[0])
    new_upper_set, player_upper_set, lower_set=divide_hands(new_sets,face,verbose=False)
    
    for i in range(0,len(new_upper_set)):
        for j in range(0,len(new_upper_set[i])):
            upper_set[i].append(new_upper_set[i][j])

    if verbose == True: print 'UPDATE LOWER-- after update',len(upper_set[0]),'\nremaining lower_set=',len(lower_set[0])
    return upper_set,player_upper_set,lower_set
    # hand_combos = [ value of cards , odds of catching hand , value of each card in hand ]


def handle_aces(hand):
    if sum(hand) >= 22:
        if hand.count(11) != 0:
            hand[hand.index(11)] = 1
            return hand,True
    return hand,False
def supp_all_hands(all_hands,new_hand,new_odds,face=False,verbose=False):                
    try:
        if all_hands[0].count(new_hand) != 0:
            ind=all_hands[0].index(new_hand)
            all_hands[1][ind]=all_hands[1][ind]+new_odds
        elif all_hands[0].count(new_hand) >= 2:
            print new_hand
            print "ERROR"
            exit(0)
        else:
            all_hands[0].append(new_hand)
            all_hands[1].append(new_odds)
            all_hands[2].append("")
        if 16 < sum(new_hand[:len(new_hand)-2]) and new_hand[:len(new_hand)-2].count(1) == 0:# or 16 < sum(new_hand) < 21: 
            all_hands[3].append(1)
        elif 16 < sum(new_hand[:len(new_hand)-2]) and 16 < 10 + sum(new_hand[:len(new_hand)-2]):
            all_hands[3].append(1)
        else:
            all_hands[3].append(0)
    except:
        print 'x'
    return all_hands
def divide_hands(hands,face=True,verbose=False):
    upper_set, player_upper_set, lower_set = [[],[],[]], [[],[],[]], [[],[],[]]
    #if verbose == True: print 'UPDATE LOWER-- before update',len(upper_set[0]),len(lower_set[0])
    # face=True --> hand_combos = CARD VALUES - ODDS/PERCENT - CARD FACES
    # face=False --> hand_combos = CARD VALUES - ODDS/PERCENT
    for i in range(0, len(hands[0])):
        hands[0][i],change=handle_aces(hands[0][i])

        if 16 < sum(hands[0][i]):
            upper_set[0].append(hands[0][i])
            upper_set[1].append(hands[1][i])
            if face==True: upper_set[2].append(hands[2][i])
        if 16 < sum(hands[0][i]) < 21:
            player_upper_set[0].append(hands[0][i])
            player_upper_set[1].append(hands[1][i])
            if face==True: player_upper_set[2].append(hands[2][i])
        if sum(hands[0][i]) <= 16:
            lower_set[0].append(hands[0][i])
            lower_set[1].append(hands[1][i])
            if face==True: lower_set[2].append(hands[2][i])

    if verbose == True: print 'UPDATE LOWER-- after update',len(hands[0]),len(lower_set[0])
    return upper_set, player_upper_set, lower_set

    # hand_combos = [ value of cards , odds of catching hand , value of each card in hand ]    
def iterate_next_hands(card_deck, all_hands, new_set, face=True, verbose=False):
    hands=copyList(new_set)
    #hands=copyList(player_upper_set)
#     for i in range(0,len(lower_set)):
#         for j in range(0,len(lower_set[i])):
#             hands[i].append(lower_set[i][j])
    #difference between new card deck and used card deck? 
    min_odd=lowest_chance()
    new_hands = [[],[],[]]
    # hands =  CARD VALUES - HAND ODDS - CARD FACES
    
    if verbose == True: print '\n<---- START iterate_next_hands'
    if verbose == True: print 'len update combo iteration=',len(hands[0])
    if face == False:
        for i in range(0, len(hands[0])): # CARD VALUES - HAND ODDS - CARD FACES
            # PREPARE DECK FOR EVALUATING CURRENT HAND
            temp_deck=copyList(card_deck)
            temp_deck=[get_card_vals(x) for x in temp_deck]
            temp_deck.sort()
            popList=[]
            for it in hands[0][i]:
                if it == 1:
                    temp_deck.pop(temp_deck.index(11))
                elif temp_deck.count(it) != 0:
                    temp_deck.pop(temp_deck.index(it))
                else:
                    print 'error'
                    print it
                    print temp_deck
                    print hands[0][i]
                    exit(0)
            if verbose == True: print 'hand size=',len(hands[0][i]),'deck len=',len(temp_deck)
            
            # CONSIDER ALL NEXT CARDS FOR PARTICULAR HAND

            temp_odd=hands[1][i]
            next_cards=get_prob(temp_deck, face=face, start_prob=temp_odd, verbose=False) 
            # CARD FACES/VALUES - HAND ODDS
            
            check_percent=0
            for j in range(0,len(next_cards[0])):
                if next_cards[1][j] >= min_odd:

                    # ADD CARD TO HAND, CALC. ODD of getting to card
                    temp_card_vals=copyList(hands[0][i])
                    temp_card_vals.append(next_cards[0][j])
                    new_hand=copyList(temp_card_vals)
                    new_odds=next_cards[1][j]
                    new_hand,change = handle_aces(new_hand)
                    
                    if all_hands != False: all_hands=supp_all_hands(all_hands,new_hand,new_odds,face=face,verbose=False)

                    new_hands[0].append(new_hand)
                    new_hands[1].append(new_odds)
                    if face == True: new_hands[2].append("")#.append(new_faces)
                                       
                check_percent+=next_cards[1][j]
                    
            if str(check_percent/hands[1][i]) != "1.0":
                print check_percent,' = ',hands[1][i]
                print check_percent,' = ',hands[1][i]
                    
            if verbose == True: print sum([x for x in next_cards[1]]),'=?=',temp_odd,'=?=',check_percent
            
    if verbose == True: print 'iterate_next_hands END ---->'
    if all_hands != False: return  all_hands,new_hands
    else: return  new_hands
        
        #return lower set that has all possible next cards with updated odds

def get_initial_odds(card_deck, prob, show_odds=False):
    hand_odds = []
    card_set = range(2, 11)
    
    for k in range(0, len(card_set)):
        play_cards = [eval(str(card_set[k]))]
        temp_hand_odds = []#get_hand_odds(play_cards, prob, show_odds=False)
        temp_card_odd, relative_odds = prob[1][k], []
        check = 0
        for j in range(0, len(temp_hand_odds)):
            relative_odds.append(temp_card_odd * temp_hand_odds[j])
            check += temp_card_odd * temp_hand_odds[j]
        print temp_card_odd, " = ", check
        hand_odds.append(relative_odds)
def np_get_odds(h,card_deck,verbose=False):
    print len(card_deck)
    r,c = h.shape
    total_odds=np.ones((r,))
    hand_totals=h.sum(axis=1)  
    card_deck_copy=copyList(card_deck)
    card_deck_copy_vals=get_card_vals(card_deck_copy)
    for i in range(1,12):
        cardNum=(h==i).sum(axis=1) # number of cards in particular row
        if i==1: i=11  # to search in the deck of cards for aces
        cardNumOdds=np.ones((r,))
        card_odds=1
        for j in range(1,cardNum.max()): #start at 1 b/c don't care about zero
            # focusing on number of a particular card in deck
            # keeping separate issue of total number of cards changing
            #     the "+1-j" business accounts for repetitions in sets of hand
            #        had to use "+1-j" format to sync with "(cardNum==j)" below
            card_odds*=float(card_deck_copy_vals.count(i)-j+1) / float(len(card_deck_copy_vals))
            temp=(cardNum==j)*card_odds
            add_temp=(temp==0)
            cardNumOdds*=(temp+add_temp)
        total_odds*=cardNumOdds
    #print 'before total card factor',total_odds[1,]
    
    # red_factor adjusts odds based on shrinking deck size
    red_fact,numer=1,1
    zeroCardNum=(h==0.).sum(axis=1)
    zeroNumFactor=np.ones((r,))
    playerOnly=np.zeros((r,))
    for i in range(2,c+1): # iteration based on how many cards are in a hand
        handCountNum=(zeroCardNum==(c-i))
        numer*=len(card_deck_copy_vals)
        denom=np.prod(np.arange(len(card_deck_copy_vals)-1,len(card_deck_copy_vals)-i,-1))
        red_fact = float(numer)/float(denom)#float(len(card_deck_copy_vals))/float(len(card_deck_copy_vals)-(i-1))
        temp=handCountNum*red_fact
        add_temp=(temp==0)
        zeroNumFactor*=(temp+add_temp)
         
        if i>2:
            evalHandTotals=hand_totals*handCountNum
            lastCardofHands=h[:,[i-1]].flatten()
            lastHandTotal=(evalHandTotals-lastCardofHands)*(evalHandTotals>0)
            playerOnly+=(lastHandTotal>16)
            """
            print 'show that upper_set is being selected properly'
            print evalHandTotals[1,]
            print lastHandTotal[1,]
            print playerOnly[1,]
            print h[1,]
            print evalHandTotals[900,]
            print lastHandTotal[900,]
            print playerOnly[900,]
            print h[900,]
            print evalHandTotals[2150,]
            print lastHandTotal[2150,]
            print playerOnly[2150,]
            print h[2150,]
            """
    # update odds from above factoring of shrinking deck
    #total_odds=total_odds*zeroNumFactor
    total_odds*=zeroNumFactor
    if verbose == True:
        np_check_odds(h,total_odds,card_deck_copy_vals)

    return total_odds,playerOnly
def np_update_odds_by_deck(h,total_odds,newCards,card_deck_vals):
    r,c = h.shape
    X,Y=len(newCards),len(card_deck_vals)
    Z=X+Y  # old deck size
    red_fact,numer=1,1
    zeroCardNum=(h==0.).sum(axis=1)
    zeroNumFactor=np.ones((r,))
    playerOnly=np.zeros((r,))
    for i in range(2,c+1): # iteration based on how many cards are in a hand
        handCountNum=(zeroCardNum==(c-i))
        
        #numer*=len(card_deck_copy_vals)
        #denom=np.prod(np.arange(len(card_deck_copy_vals)-1,len(card_deck_copy_vals)-i,-1))
        n = np.prod(np.arange(Y+X,Z-i,-1))
        d = np.prod(np.arange(Z-i-X+1,Z-X+1,1))
        red_fact = float(n)/float(d)#float(len(card_deck_copy_vals))/float(len(card_deck_copy_vals)-(i-1))
        temp=handCountNum*red_fact
        add_temp=(temp==0)
        zeroNumFactor*=(temp+add_temp)       
    total_odds*=zeroNumFactor
        
    return total_odds
def np_check_odds(h,total_odds,card_deck):
    D=len(card_deck)
    print '\nShow that below are correct with',D,"number of cards"
    print '\n',h[670,] # [ 8.  2.  2.  0.  0.  0.]
    print 'actual:\t',total_odds[670,]
    print 'expect:\t',(float(16)/float(D))*(float(15)/float(D-1))*(float(16)/float(D-2))
    
    print '\n',h[671,] # [ 8.  2.  3.  0.  0.  0.]
    print 'actual:\t',total_odds[671,]
    print 'expect:\t',(float(16)/float(D))*(float(16)/float(D-1))*(float(16)/float(D-2))
    
    print '\n',h[1671,] # [ 4.  4.  9.  3.  0.  0.]
    print 'actual:\t',total_odds[1671,]
    print 'expect:\t',(float(16)/float(D))*(float(15)/float(D-1))*(float(16)/float(D-2))*(float(16)/float(D-3))
    
    print '\n',h[11671,] # [ 6.  6.  5.  1.  3.  0.]
    print 'actual:\t',total_odds[11671,]
    print 'expect:\t',(float(16)/float(D))*(float(15)/float(D-1))*(float(16)/float(D-2))*(float(16)/float(D-3))*(float(16)/float(D-4))
    
    print '\n',h[43671,] # [ 10.   2.   1.   3.   3.   0.]
    print 'actual:\t',total_odds[43671,]
    print 'expect:\t',(float(64)/float(D))*(float(16)/float(D-1))*(float(16)/float(D-2))*(float(16)/float(D-3))*(float(15)/float(D-4))
    
    print '\n',h[45000,] # [  3.  10.   3.   1.   2.  10.]
    print 'actual:\t',total_odds[45000,]
    print 'expect:\t',((float(16)/float(D))*
            (float(64)/float(D-1))*
            (float(15)/float(D-2))*
            (float(16)/float(D-3))*
            (float(16)/float(D-4))*
            (float(63)/float(D-5)))
    print '-------------\n'
def np_get_remaining_hands(h,total_odds,player_dealer):
    temp_odds=total_odds.copy()
    playerHands=h.copy()
    checked=[]
    for it in player_dealer:
        if checked.count(it) == 0:
            checked.append(it)
            cardNum=(playerHands==it).sum(axis=1) # number of "it" cards in particular row
            take_rows = np.nonzero(cardNum == 1)
            playerHands=playerHands[take_rows,:]
            playerHands=np.swapaxes(playerHands,1,0)
            playerHands=np.reshape(playerHands,(-1,6))
            temp_odds=temp_odds[take_rows]
    return playerHands,temp_odds

def np_update_odds_by_hand(card_deck_vals,hands,odds,newCards):
    r,c = hands.shape
    # card changing
    for i in range(1,12):
        NCC=newCards.count(i) # NCC = new card count
        if NCC != 0:
            cardNum=(hands==i).sum(axis=1)
            if i==1: i=11
            cardNumOdds=np.ones((r,))
            nC=card_deck_vals.count(i)
            for j in range(1,cardNum.max()+1):
                n=np.prod(np.arange(nC-1,nC-j-1,-1))
                d=np.prod(np.arange(nC+NCC,nC-j+1,-1))
                temp=(cardNum==j)*(float(n)/float(d))
                add_temp=(temp==0)
                odds*=(temp+add_temp)
    return odds

def np_update_total_odds(h,total_odds,card_deck_vals,newCards,verbose=False):
    r,c = h.shape
    # update based on cards shown
    total_odds=np_update_odds_by_hand(card_deck_vals,h,total_odds,newCards)
    
    # update based on deck size
    total_odds=np_update_odds_by_deck(h,total_odds,newCards,card_deck_vals)

    return total_odds

def np_distr(np_hands,np_odds):
    #print np_hands.shape
    #print np_odds.shape
    hand_totals=np_hands.sum(axis=1)
    np_total_odds=np_odds.sum()
    sixteen=(((hand_totals<17)*np_odds).sum())/np_total_odds
    seventeen=(((hand_totals==17)*np_odds).sum())/np_total_odds
    eighteen=(((hand_totals==18)*np_odds).sum())/np_total_odds
    nineteen=(((hand_totals==19)*np_odds).sum())/np_total_odds
    twenty=(((hand_totals==20)*np_odds).sum())/np_total_odds
    twentyone=(((hand_totals==21)*np_odds).sum())/np_total_odds
    bust=(((hand_totals>21)*np_odds).sum())/np_total_odds
    hand_distr = { '16' : sixteen,
                '17' : seventeen,
                '18' : eighteen,
                '19' : nineteen,
                '20' : twenty,
                '21' : twentyone,
                '22' : bust }
    return hand_distr
def get_odds_pre_deal(card_deck, face=True, verbose=False, show_odds=False): 
#     #gets odds of all possible hands in terms of [17-21,bust] 
#     #USING VALUES (NOT FACES)
#     all_hands = [[],[],[],[]] # CARD VALUES - HAND ODDS - CARD FACES - DEALER HAND = 1
#     # 16 < DEALER HAND < 22 -- but dealer can bust too...
#     #    solution was to tag "player only" as all_hands[3] and 
#     #    to continue playing out/tagging player only hands until they busted
#     temp_deck = copyList(card_deck)
#     if face == False: temp_deck = [get_card_vals(x) for x in temp_deck]
#     temp_deck.sort()
#     first_cards=get_prob(card_deck, face, start_prob=1, verbose=False) # CARD FACES - HAND ODDS
#     for i in range(0,len(first_cards[0])):
#         temp_card=first_cards[0][i]
#         temp_odds=first_cards[1][i]
#         first_temp_deck=copyList(temp_deck)
#         temp_deck.pop(temp_deck.index(temp_card))
#         second_cards=get_prob(first_temp_deck, face, start_prob=temp_odds, verbose=False)
#         for j in range(0,len(second_cards[0])):
#             new_hand_val=[temp_card,second_cards[0][j]]
#             new_temp_odd=second_cards[1][j]
#             all_hands=supp_all_hands(all_hands,new_hand_val,new_temp_odd,face=False,verbose=False)
# 
#     if verbose == True:
#         print '<---- START get_ALL_hand_odds'
#         print len(all_hands[0])
#         over,under=[],[]
#         for i in range(0,len(all_hands[0])):
#             if sum(all_hands[0][i]) > 16: over.append(all_hands[0][i])
#             else: under.append(all_hands[0][i])
#             print all_hands[0][i],all_hands[2][i],all_hands[1][i]
#         print 'number in deck',len(card_deck)
#         print 'number of hands',len(all_hands[0])
#         print 'total percent',sum([x for x in all_hands[1]])
#         print 'over//under = ',len(over),'//',len(under)
#  
# #     for it in all_hands[0]:
# #         if all_hands[0].count(it) > 1:
# #             print 'one'
# #             exit(0)
#     all_hands_copy=copyList(all_hands)
#  
#     # lower_set = those hand_combos with values below 17
#     #all_hands,upper_set,lower_set = update_lower_set(all_hands,upper_set,played_lower_set,face,verbose=False)
#     upper_set, first_player_upper_set, lower_set = divide_hands(all_hands_copy,face,verbose)
#     if verbose == True: print len(all_hands),'combos, high//low -- ',len(upper_set[0]),'//',len(lower_set[0])
#     if verbose == True: print 'before checking lower set, number of cards:', len(card_deck)
#      
#     # get odds of playing all lower_set hands until value greater than 16
#     # lower_set ( < 16 ) = CARD VALUES - HAND ODDS - CARD FACES
#     while len(lower_set[0]) != 0:  
#         temp_deck=copyList(card_deck)
#         temp_deck.sort()
#  
#         # simulate/return sets of hands/odds for continued playing of low hands
#         all_hands,iter_lower_set = iterate_next_hands(temp_deck,all_hands,
#                                                       lower_set,face,verbose=False)
#         # split simulated hands up into different group
#         upper_set,player_upper_set,lower_set = update_sets(upper_set,iter_lower_set,
#                                                            face,verbose=False)
#         # for those hands the dealer would not have played but are not bust, 
#         # keep iterating for the purpose of building complete set of all_hands
#         while len(player_upper_set[0]) != 0:  
#             all_hands,iter_player_set = iterate_next_hands(temp_deck,all_hands,
#                                                        player_upper_set,face,verbose=False)
#             dump,player_upper_set,additional_lower_set = update_sets([[],[],[]],iter_player_set,
#                                                                           face,verbose=False)
#             # add to player_upper_set the new lower_sets from simulating player only hands
#             for i in range(0,2):
#                 for j in range(0,len(additional_lower_set[0])):
#                     player_upper_set[i].append(additional_lower_set[i][j])
#             if first_player_upper_set != False:
#                 for i in range(0,2):
#                     for j in range(0,len(first_player_upper_set[0])):
#                         player_upper_set[i].append(first_player_upper_set[i][j])
#                 first_player_upper_set = False

    #listFout(upper_set,'/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-upper_set.txt')
    #listFout(all_hands,'/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck.txt')
    #print fdsdf
#    calcOdds=[[],[],[],[],[]]
#     for i in range(0,len(all_hands[1])):
#         if len(all_hands[0][i]) == 2:
#             calcOdds[0].append(all_hands[1][i])
#         elif len(all_hands[0][i]) == 3:
#             calcOdds[1].append(all_hands[1][i])
#         elif len(all_hands[0][i]) == 4:
#             calcOdds[2].append(all_hands[1][i])
#         elif len(all_hands[0][i]) == 5:
#             calcOdds[3].append(all_hands[1][i])
#         elif len(all_hands[0][i]) == 6:
#             calcOdds[4].append(all_hands[1][i])
#         elif len(all_hands[0][i]) == 7:
#             calcOdds[5].append(all_hands[1][i])
    #print 'len of all_hands',len(all_hands[0])
    #for i in range(0,len(calcOdds)):
    #    print 'sum of ',i+2,'calcOdds',sum(calcOdds[i])
    #print 'ha'
    #all_hands=listFin('/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck.txt')
    #upper_set=listFin('/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-upper_set.txt')
    #hatrix=listFin('/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck-matrix.txt')
    
#     b=all_hands[0]
#     max_cards=6
#     g=False
#     for i in range(2,max_cards+1):
#         d=np.matrix([x for x in b if len(x)==i],dtype=int)
#         r,c=d.shape
#         e=np.zeros((r,max_cards-i))
#         r=np.column_stack([d,e])
#         if type(g)==bool: g=r
#         else: g=np.vstack([g,r])
#     print g.shape
#     arrayFout(g,'/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck-matrix.txt')
    
    h=arrayFin('/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck-matrix.txt')
    r,c = h.shape
    total_odds=np.ones((r,))
    hand_totals=h.sum(axis=1)
    total_odds,playerOnly=np_get_odds(h,card_deck,verbose=False)

    
    # get all sets of upper hands 
    # [since that all that will be calculated for dealer]
    all_upper=(hand_totals>16)*(playerOnly==0)
    take_rows = np.nonzero(all_upper == 1)
    dealer_set=h[take_rows,:]
    dealer_set=np.swapaxes(dealer_set,1,0)
    dealer_set=np.reshape(dealer_set,(-1,6))
    dealer_set_odds=total_odds[take_rows,:]
    dealer_set_odds=np.swapaxes(dealer_set_odds,1,0).flatten()

    # get all set of hand only played by player
    take_rows = np.nonzero(playerOnly == 1)
    player_set=h[take_rows,:]
    player_set=np.swapaxes(player_set,1,0)
    player_set=np.reshape(player_set,(-1,6))
    player_set_odds=total_odds[take_rows,:]
    player_set_odds=np.swapaxes(player_set_odds,1,0).flatten()
    
    """
    print 'check for all hands, dealer_set, player_set -- w/ odds'
    print h.shape
    print h[1,]
    print total_odds.shape
    print total_odds[1,]
    print dealer_set.shape
    print dealer_set[1,]    
    print dealer_set_odds.shape
    print dealer_set_odds[1,]    
    print player_set.shape
    print player_set[1,]    
    print player_set_odds.shape
    print player_set_odds[1,] 
    print sgfsg
    """


#t_odds=np.dot([odds matrix] , odds) = total odds [ when odds going for each hand going vertical ]

    
#     for i in range(0,len(all_hands[0])):
#         hand=all_hands[0][i]
#         odds=all_hands[1][i]
#         card_deck_copy=copyList(card_deck)
#         hand_prob=1
#         for card in hand:
#             hand_prob*=float(card_deck_copy.count(card)) / float(len(card_deck_copy))
#         all_hands[1][i]=hand_prob
#         if upper_set[0].count(hand): 
#             all_hands[3][i]=1
#             upper_set[1][upper_set[0].index(hand)]=hand_prob
        #else:
        #    if sum(all_hands[0][i]) > 16:
        #        all_hands[3][i]=1
                #print all_hands[0][i]
                #upper_set[0].append(all_hands[0][i])
                #upper_set[1].append(all_hands[1][i])

    #listFout(all_hands,'/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck.txt')
    #listFout(upper_set,'/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-upper_set.txt')

    #arr=np.empty((N,M))
    #for x in range(k):
    #    arr[x]=x*np.ones(M)
    #arr.resize((k,M))
    
    #a=np.asarray(hatrix)
    #b=np.asmatrix(hatrix)
    #print a[0]
    #c=np.where(a==2)
    #d=0

    # i like how below compares dealer hands (17-bust) versus ALL player hands --
    # -- such inclusion contemplates differentiation between
    # -- heavy amount of 10s and [2-5] vs. heavy amount of [6-9]
    # -- more simple method would be calculating dealer bust only
    #d_p_distr = get_odds_distribution(card_deck,all_hands,upper_set,relative=False,verbose=False)
 
    """
    
    Next step is to create distribution based on below.
    
    """
  
    # h, dealer_set, player_set
    # total_odds,dealer_set_odds,player_set_odds

    #print 'a'
    all_hand_distr=np_distr(h,total_odds)
    #print 'b'
    d_hand_distr=np_distr(dealer_set,dealer_set_odds)
    #print 'c'
    p_hand_distr=np_distr(player_set,player_set_odds)
    #d_p_distr=d_hand_distr,p_hand_distr
    d_p_distr=d_hand_distr,all_hand_distr
    #for it in d_hand_distr.keys():
    #    print type(d_hand_distr[it])
    #    print sfd

    #p_d_hand_distr=[]
    #for i in range(0,len(d_hand_odds.keys())):
    #    p_d_hand_distr.append(p_hand_odds[d_hand_odds.keys()[i]]-d_hand_odds[d_hand_odds.keys()[i]])
    difference,above,below=get_win_odds(d_p_distr,hands=False,relative=False,verbose=False)
    play_odds=difference

    all_sets=h,dealer_set,player_set
    all_odds=total_odds,dealer_set_odds,player_set_odds
    all_info=all_sets,all_odds
    
    return play_odds,all_info    
    
    
#     total=seventeen + eighteen + nineteen + twenty + twentyone + bust
#     p_total=p_seventeen + p_eighteen + p_nineteen + p_twenty + p_twentyone + p_bust
#     
#     distribution= (seventeen, eighteen, 
#                    nineteen, twenty, twentyone, bust)
#     total=sum(distribution)
#     p_distribution= (p_seventeen, p_eighteen, 
#                      p_nineteen, p_twenty, p_twentyone, p_bust)
#     p_total=sum(p_distribution)
#     if verbose == True: print 'TOTAL ODDS',total+p_total
#     p_d_distribution= (p_seventeen-seventeen, 
#                         p_eighteen-eighteen, p_nineteen-nineteen, 
#                         p_twenty-twenty, p_twentyone-twentyone,
#                         p_bust-bust)
#     if verbose == True: print 'p-total - total', p_total-total
#     if verbose == True: print '\nget_odds_distribution END ---->\n'
#     return distribution,p_distribution,p_d_distribution
#     
#     
#     if verbose == True:
#         print_distr(distribution,title="Dealer Odds")
#         print_distr(p_distribution,title="Player Odds")
# 
#         difference,above,below=get_win_odds(distribution,relative=False,verbose=False)
#         dealer_odds=difference
#         difference,above,below=get_win_odds(p_distribution,relative=False,verbose=False)
#         player_odds=difference
#         difference,above,below=get_win_odds(combined_distribution,relative=False,verbose=False)
#         combinded_odds=difference
#         difference,above,below=get_win_odds(p_d_distribution,relative=False,verbose=False)
#         p_d_odds=difference
#         print 'dealer odds',dealer_odds
#         print 'player odds',player_odds
#         print 'combined',combined_odds
#         print 'p_d_combined',p_d_odds
#         print 'player - dealer',player_odds-dealer_odds
#         print 'dealer - player',dealer_odds-player_odds
#         print 'dealer + player',dealer_odds+player_odds
#     
       
def make_hatrix(all_hands):
#     ordered=[]
#     for it in all_hands[0]:
#         x=it[:]
#         x.sort()
#         if ordered.count(x) == 0:
#             ordered.append(x)
#     listFout(ordered,'/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck2.txt')
#     hands=listFin('/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck2.txt')
#     print len(all_hands[0]),len(hands)
#     
#     hatrix=[]
#     print len(hatrix),len(hands)
#     for i in range(2,7):
#         popList=[]
#         for j in range(0,len(hands)):
#             if len(hands[j]) == i:
#                 popList.append(j)
#         popList.reverse()
#         for it in popList:
#             x=hands.pop(it)
#             x.sort()
#             hatrix.append(x)
#     
#     listFout(hatrix,'/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck-matrix2.txt')
#     print len(hatrix),len(hands)
#     hands=listFin('/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck-matrix2.txt')
#     hatrix2=[]
#     print len(hands),len(hatrix2)
# 
#     # shortest to longest length, smallest to largest number at each length 
#     for i in range(2,7): # for all lengths
#         popList=[]
#         for j in range(0,len(hands)):
#             if len(hands[j])==i:
#                 for k in range(0,len(hands[j])):
#                     for l in range(1,12):
#                         if hands[j][k]==l:
#                             if popList.count(j) == 0: popList.append(j)
#         popList.reverse()
#         tempList=[]
#         for it in popList:
#             try:
#                 tempList.append(hands.pop(it))
#             except:
#                 pass
#         tempList.reverse()
#         for it in tempList:
#             hatrix2.append(it)
#         tempList=[]
#                     
#     listFout(hatrix2,'/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck-matrix3.txt')
#     print len(hands),len(hatrix2
#     hands=listFin('/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck-matrix3.txt')
#     hatrix=[]
#     for i in range(0,6):
#         hatrix.append([])
#     for it in hands:
#         a=it[:]
#         for i in range(0,6):
#             if i < len(it): hatrix[i].append(a[i])
#             else: hatrix[i].append(0)    
#     listFout(hatrix,'/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck-matrix4.txt')
    pass
    
def hand_sets(all_hands,card_val,hand_ind=0):
    hatrix=listFin('/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck-matrix.txt')
#     for i in range(0,len(hatrix)):
#         print len(hatrix[i])
    # purpose to slice out sections of all_hands instead of re-calculating cards/odds
    return all_hands[hand_ind][all_hands[hand_ind].index(card_val):
                               all_hands[hand_ind].index(card_val)+all_hands[hand_ind].count(card_val)]


# def get_hand_odds(card_deck, play_cards, prob, show_odds=False):
#  
#     hand_combos = [[], [], []]  # HAND - PERCENT - COMBO
#     hand_combos = update_combos(hand_combos, play_cards, prob, True) 
#     print 'card deck=',len(card_deck)
#     print 'play cards=',len(play_cards)
#     print prob
#      
#     print len(hand_combos[0]), hand_combos[0][0]
#     exit(0)
#      
#     lower_set, upper_set = [[], [], []], [[], [], []]  # lower_set = those hand_combos with values below 17
#     hand_combos, lower_set = update_sets(upper_set, hand_combos, face=True, verbose=False)
#      
#     print 'before checking lower set, number of cards:', len(card_deck)
#      
#     while len(lower_set[0]) != 0:  # get odds of playing all lower_set hands until value greater than 16
#         temp_hand = lower_set[0]  # sum of hand
#         temp_prob = lower_set[1]  # percent of getting hand
#         temp_cards = lower_set[2]  # cards in hand as string
#          
#         print temp_hand
#         print temp_prob
#         print temp_prob
#         exit(0)
#          
#         # temp_cards=[get_card_vals(x) for x in temp_cards] # as int
#         # for it in play_cards: x=temp_cards.pop(temp_cards.index(get_card_vals(it)))
#          
#         temp_deck = [ x for x in card_deck ]  # string type
#         for it in temp_cards:
#             if it == 1: it = 11  # deck is calculated at the moment with Aces being eleven. later when hands are moved into lower_set, if hand is bust but has an eleven, the eleven is changed to one and the hand is re-added to lower_set
#             try:
#                 x = temp_deck.pop(temp_deck.index(it))
#             except:
#                 print ''
#                 print 'ERROR:'
#                 print temp_cards
#                 print lower_set
#                 print ''
#                 exit(0)
#  
#         temp_card_prob = get_prob(temp_deck, temp_prob)
#         for it in play_cards: temp_cards.append(it)
#  
#         hand_combos = update_combos(hand_combos, temp_cards, temp_card_prob, False)
#         hand_combos, lower_set = update_sets(upper_set, hand_combos, face=True, verbose=False)
#      
#         temp_hand = lower_set[0].pop(0)
#         temp_prob = lower_set[1].pop(0)
#         temp_cards = lower_set[2].pop(0)
# 
#     
#     odd_distribution=get_odds_distribution(hand_combos,relative=False,verbose=False)
#     [seventeen, eighteen, nineteen, twenty, twentyone, bust]=odd_distribution
# 
#     return odd_distribution, hand_combos

def get_distr(hands,relative=False,verbose=False):
    if relative == False: x=1
    elif relative == True:
        x=sum([y for y in hands[1]])
        y=1
    else: x=relative
    sixteen, seventeen, eighteen, nineteen, twenty, twentyone, bust = [], [], [], [], [], [], []
    parts=sixteen, seventeen, eighteen, nineteen, twenty, twentyone, bust
    for i in range(0,len(parts)):
        for j in range(0,len(hands)):
            parts[i].append([])
    for i in range(0, len(hands[0])):
        if sum(hands[0][i]) < 17:
            for j in range(0,len(hands)):
                if j == 1: sixteen[j].append(hands[j][i]/x)
                else: sixteen[j].append(hands[j][i])
        if sum(hands[0][i]) == 17: 
            for j in range(0,len(hands)):
                if j == 1: seventeen[j].append(hands[j][i]/x)
                else: seventeen[j].append(hands[j][i])
        if sum(hands[0][i]) == 18: 
            for j in range(0,len(hands)):
                if j == 1: eighteen[j].append(hands[j][i]/x)
                else: eighteen[j].append(hands[j][i])
        if sum(hands[0][i]) == 19: 
            for j in range(0,len(hands)):
                if j == 1: nineteen[j].append(hands[j][i]/x)
                else: nineteen[j].append(hands[j][i])
        if sum(hands[0][i]) == 20: 
            for j in range(0,len(hands)):
                if j == 1: twenty[j].append(hands[j][i]/x)
                else: twenty[j].append(hands[j][i])
        if sum(hands[0][i]) == 21: 
            for j in range(0,len(hands)):
                if j == 1: twentyone[j].append(hands[j][i]/x)
                else: twentyone[j].append(hands[j][i])
        if sum(hands[0][i]) > 21:
            for j in range(0,len(hands)):
                if j == 1: bust[j].append(hands[j][i]/x)
                else: bust[j].append(hands[j][i])
    hand_distr = { '16' : sixteen,
                    '17' : seventeen,
                    '18' : eighteen,
                    '19' : nineteen,
                    '20' : twenty,
                    '21' : twentyone,
                    '22' : bust }
    if verbose==True: print_distr(hand_distr)
    return hand_distr
    
def get_dealer_plays(card_deck,all_hands,d_lower):
    print 'first',len(d_lower[0])
    #hatrix=listFin('/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck-matrix.txt')

    lower_set=[]
    lower_set=[lower_set.append([]) for it in d_lower]
    upper_set=[]
    upper_set=[upper_set.append([]) for it in d_lower]
    new_d_hands=copyList(d_lower)
    while len(d_lower[0]) != 0:
        temp_deck=copyList(card_deck)
        temp_deck.sort()
        # simulate/return sets of hands/odds for continued playing of low hands
        new_d_hands,iter_lower_set = iterate_next_hands(temp_deck,new_d_hands,
                                                      d_lower,face=False,verbose=False)
        # split simulated hands up into different group
        upper_set,player_upper_set,d_lower = update_sets(upper_set,iter_lower_set,
                                                           face=False,verbose=False)
        print len(d_lower[0])
    return new_d_hands,upper_set

def get_odds_distribution(card_deck,all_hands,upper_set,relative=False,verbose=False):
    if verbose == True: print '\nget_odds_distribution START ---->'
    if verbose == True: print 'ALL HANDS',len(all_hands[0]),len(all_hands[3])
    p_distr=get_distr(all_hands,relative)
    d_distr=get_distr(upper_set,relative)
    #d_lower=p_distr['16']
    #new_d_hands,upper_set=get_dealer_plays(card_deck,d_lower,d_lower)
    #additional_d_distr=get_distr(upper_set,relative)
    check,odd_check,p_odd_check=0,0,0
    if verbose == True: print 'TOTAL UNIQUE PLAYER HITS',check
    if verbose == True: print 'TOTAL ODDS FOR PLAYER HITS',p_odd_check
    if verbose == True: print 'TOTAL ODDS FOR NON PLAYER HITS',odd_check
    if verbose == True: print 'get_odds_distribution END ---->\n'
    return d_distr,p_distr

def print_distr(distribution,title=""):
    print '\n',title
    distr_keys=[eval(x) for x in distribution.keys()]
    distr_keys.sort()
    ctr=0
    for it in distr_keys:
        print str(it)+'\t'+str(distribution[str(it)])
        ctr+=distribution[str(it)]
    print '\nTOTAL PERCENTAGE='+'\t'+str(ctr)+'\n'


def get_win_odds(odd_distribution, hands=False,relative=False,verbose=False):
    above,below=[],[]
    if hands==False:
        d_odds,p_odds=odd_distribution  
        for it in p_odds.keys():
            if 21 < eval(it): below.append(p_odds[it])
            if 17 <= eval(it) <= 21: above.append(p_odds[it])
        for it in d_odds.keys():
            if 21 < eval(it): above.append(d_odds[it])
            if eval(it) <= 21: above.append(d_odds[it])
            if 17 <= eval(it) <= 21: below.append(d_odds[it])
        #t_above=sum([sum(x) for x in above])
        #t_below=sum([sum(x) for x in below])
        t_above=sum(above)
        t_below=sum(below)
        difference=t_above-t_below
#         seventeen, eighteen, nineteen, twenty, twentyone, bust=odd_distribution
#         
#         total=sum(odd_distribution)
#         seventeen=seventeen/total
#         eighteen=eighteen/total
#         nineteen=nineteen/total
#         twenty=twenty/total
#         twentyone=twentyone/total
#         bust=bust/total
#             
#         A = (p-seventeen + d-seventeen)/2
#         B = p-eighteen - (d-seventeen)
#         C = p-nineteen - (d-seventeen + d-eighteen)
#         D = p-twenty - (d-seventeen + d-eighteen + d-nineteen)
#         E = p-twentyone - (d-seventeen + d-eighteen + d-nineteen + d-twenty)
#         F = d-bust - p-bust
#         difference=(A+B+C+D+E+F)
    else:
        dealer,player=hands
        if type(player[0]) == str:  player=[get_card_vals(x) for x in player]
        if type(dealer[0]) == str:  dealer=[get_card_vals(x) for x in dealer]
        d_odds,p_odds=odd_distribution
        if relative==True:
            total_d_odds=sum([sum(d_odds[it][1]) for it in d_odds.keys()])
            total_p_odds=sum([sum(p_odds[it][1]) for it in p_odds.keys()])
            if total_p_odds == 0: total_p_odds=1
        else: total_d_odds,total_p_odds=1,1
        for it in p_odds.keys():
            if eval(it) > 21: below.append(sum(p_odds[it][1])/total_p_odds)
            if sum(dealer) <= eval(it) <= 21: above.append(sum(p_odds[it][1])/total_p_odds)
        for it in d_odds.keys():
            if eval(it) > 21: above.append(sum(d_odds[it][1])/total_d_odds)
            if eval(it) <= sum(player): above.append(sum(d_odds[it][1])/total_d_odds)
            if sum(player) < eval(it) <= 21: below.append(sum(d_odds[it][1])/total_d_odds)
        t_above=sum(above)
        t_below=sum(below)
        #t_above=sum([sum(x) for x in above])
        #t_below=sum([sum(x) for x in below])
        difference=t_above-t_below
        
    if verbose == True:
        print '\nget_win_odds START ---->'
        print 'ODDS OF WINNING=',difference
        #distribution= total,A,B,C,D,E
        print_distr(d_odds,title="Dealer Odds to Win")
        print_distr(p_odds,title="Player Odds to Win")
        print 'get_win_odds END ---->\n'  
    return difference,t_above,t_below


def np_update_odds_on_deal(card_deck,dealer,player,all_info,face=True,verbose=False):
    [h,dealer_set,player_set],[total_odds,dealer_set_odds,player_set_odds]=all_info
    r,c = h.shape

    dealer_show=copyList(dealer)
    card_deck_copy=copyList(card_deck)
    card_deck_copy.append(dealer_show.pop(1))
    card_deck_copy_vals=get_card_vals(card_deck_copy)
    dealer_show_val=get_card_vals(dealer_show)
    possible_hands,possible_future_hands=[[],[],[],[]],[[],[],[],[]]
    if face == False: player=[get_card_vals(x) for x in player]
    player,change=handle_aces(player)

    newCards=player[:]
    newCards.append(dealer_show_val[0])
    print 'deck size=',len(card_deck_copy_vals)
    print 'new cards=',newCards
    
    if len(newCards) == 3: total_odds=np_update_total_odds(h,total_odds,card_deck_copy_vals,newCards,verbose=True)
    #np_check_odds(h,total_odds,card_deck_copy_vals)
    
    #total_odds=np_update_odds_by_hand(card_deck_copy_vals,newCards,h,total_odds,newCards)

    playerHands,playerOdds=np_get_remaining_hands(h,total_odds,player)
    dealerHands,dealerOdds=np_get_remaining_hands(h,total_odds,dealer_show_val)

    #playerOdds=np_update_odds_by_hand(card_deck_copy_vals,playerHands.copy(),playerOdds.copy(),player)

    print playerHands.shape
    print playerHands[1,]
    print playerOdds.shape
    print playerOdds[1,]

    #dealerOdds=np_update_odds_by_hand(card_deck_copy_vals,dealerHands.copy(),dealerOdds.copy(),dealer_show_val)

    print dealerHands.shape
    print dealerHands[1,]
    print dealerOdds.shape
    print dealerOdds[1,]

    print adsa


    #total_odds,playerOnly=np_get_odds(h,card_deck_copy,verbose=True)
    
    
    print 'CHECK ABOVE -- should be all the same'
    """
    the above verbose
    
    I want to be able to access the odds of all hands at all times.
    I should be able to update odds based on changes in deck size.
    I should separately be able to update odds for each card observed.
    I should further be able to determine odds for each player based on cards in hand.
    
    For some reason after cards get taken from the deck the odds start to change.
    Not sure yet how to limit isolate issue.
    Issue could be updating particular card count.
    Issue could be shrinking deck size.
    
    
    """
    # updating odds for player-hand


#     
#     D=len(card_deck_copy_vals)
#     C=len(newCards)
#     zeroCardNum=(h==0.).sum(axis=1)
#     zeroNumFactor=np.ones((r,))
#     for i in range(2,zeroCardNum.max()+2+1): # iteration based on how many cards are in a hand
#          i=2,3,4,5,6 index vars
#          H=4,3,2,1,0  # number of zeros per hand
#         H=(c-i) 
#         numer=np.prod(np.arange(C+D,C+D-i,-1))
#             208,207;208,207,206 ...
#         denom=np.prod(np.arange(D,D-i,-1))
#             205,204;205,204,203 ...
# 
#         handCountNum=(zeroCardNum==H)
#         len(card_deck_copy_vals)
#         deck_factor = float(numer)/float(denom)
#         temp=handCountNum*deck_factor
#         add_temp=(temp==0)
#         total_odds*=(temp+add_temp)
#     

 
    
    dealerHands=(dealer_set==dealer_show_val).sum(axis=1)
    take_rows = np.nonzero(dealerHands == 1)
    dealerHands=dealer_set[take_rows,:]
    dealerHands=np.swapaxes(dealerHands,1,0)
    dealerHands=np.reshape(dealerHands,(-1,6))
    print dealerHands.shape
    print sdfsdf
    
    # red_factor adjusts odds based on shrinking deck size
    red_fact=1
    zeroCardNum=(h==0.).sum(axis=1)
    zeroNumFactor=np.ones((r,))
    playerOnly=np.zeros((r,))
    # iteration based on how many cards are in a hand
    # iter type necessary to account for "playerOnly" hands
    # was able to combine "playerOnly" iter with "red_fact" iter 
    for i in range(2,c+1): 
        handCountNum=(zeroCardNum==(c-i))
        red_fact *= float(len(card_deck_copy_vals))/float(len(card_deck_copy_vals)-(i-1))
        temp=handCountNum*red_fact
        add_temp=(temp==0)
        zeroNumFactor*=(temp+add_temp)
        
        if i>2:
            evalHandTotals=hand_totals*handCountNum
            lastCardofHands=h[:,[i-1]].flatten()
            lastHandTotal=(evalHandTotals-lastCardofHands)*(evalHandTotals>0)
            playerOnly+=(lastHandTotal>16)      

    
    
    playerOdds,possible_odds=[],[]
    
    update_np_odds
    
    return possible_hands,stay_odds,hit_odds

def update_odds_on_deal(card_deck,dealer,player,all_hands,face=True,verbose=False):
    dealer_show=copyList(dealer)
    card_deck_copy=copyList(card_deck)
    card_deck_copy.append(dealer_show.pop(1))
    dealer_show_val=get_card_vals(dealer_show)[0]
    possible_hands,possible_future_hands=[[],[],[],[]],[[],[],[],[]]
    if face == False: player=[get_card_vals(x) for x in player]
    player,change=handle_aces(player)
    playerOdds,possible_odds=[],[]
    
    # GET ODD OF DEALER GETTING SHOW-CARD, THEN DIVIDE ALL HANDS BY SUCH ODD
    for it in player: card_deck_copy.append(get_card(it))
    for it in dealer_show: card_deck_copy.append(it)
    card_deck_copy_vals=get_card_vals(card_deck_copy)
    new_odds=get_prob(card_deck_copy, face=False, start_prob=1, verbose=False)
    for it in player: card_deck_copy.pop(card_deck_copy.index(get_card(it)))
    for it in dealer_show: card_deck_copy.pop(card_deck_copy.index(it))
    dealer_show_odd=new_odds[1][new_odds[0].index(dealer_show_val)]
    
    #print player
    #hatrix=listFin('/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-deck-matrix.txt')
    upper_set=listFin('/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-upper_set.txt')
    new_upper_set_ind=[upper_set[0].index(x) for x in upper_set[0] if x.count(dealer_show_val)!=0]
    new_upper_set=[[upper_set[0][i] for i in new_upper_set_ind],[upper_set[1][i]/dealer_show_odd for i in new_upper_set_ind]]
    #d_upper=[k[i] for k in [i for i in new_upper_set_ind]]
    
    d_distr=get_distr(new_upper_set,relative=True,verbose=False)
    print 'dealer bust odds',sum(d_distr['22'][1])
    p_distr={str(sum(player)): [player,[float(0)]]} # using zero to limit effect on odds calc.
    odd_distr=d_distr,p_distr

    difference,above,below=get_win_odds(odd_distr,hands=[dealer_show,player],relative=True,verbose=False)
    stay_odds=above
    new_cards=get_prob(card_deck_copy, face, start_prob=1, verbose=False)
    
    for i in range(0,len(new_cards[0])):
        new_hand=player[:]
        new_hand.append(new_cards[0][i])
        new_hand,change=handle_aces(new_hand)
        possible_future_hands[0].append(new_hand)
        possible_future_hands[1].append(new_cards[1][i])
        possible_future_hands[2].append("")
        possible_future_hands[3].append("")

    p_distr=get_distr(possible_future_hands,relative=True,verbose=False)
    odd_distr=d_distr,p_distr
    print 'player bust odds',sum(p_distr['22'][1])
    difference,above,below=get_win_odds(odd_distr,hands=[dealer_show,player],relative=True,verbose=False)
    hit_odds=above/float(2) # taking into account that both dealer and player odds equalled 1
    
#     for i in range(0,len(all_hands[0])):
#         it=all_hands[0][i]
#         ctr=0
#         for card in player:
#             if it[:len(player)].count(card) != 0:
#                 ctr+=1
#         if len(it[:len(player)]) == ctr:
#             possible_hands[0].append(all_hands[0][i])
#             possible_hands[1].append(all_hands[1][i])
#             possible_hands[2].append("")
#             possible_hands[3].append(all_hands[3][i])
#             if len(it) == len(player):
#                 playerOdds.append(all_hands[1][i])
#             else:
#                 possible_odds.append(all_hands[1][i])
#   print '\nnumber of possible hands left=',len(possible_hands[0])

#    for i in range(0,len(possible_hands[0])):
#        print len(possible_hands[0][i]),possible_hands[0][i],possible_hands[1][i]
        #if len(possible_hands[0][i]) == 2:
        #    print len(possible_hands[0][i]),possible_hands[0][i],possible_hands[1][i]
        #break
    #upper_set=listFin('/Users/admin/SERVER2/BD_Scripts/Blackjack/hands/4-upper_set.txt')
    
    #odd_distr=get_odds_distribution(card_deck_copy,possible_hands,upper_set,relative=sum(playerOdds),verbose=False)
    # odd_distr == d_hand_odds,p_hand_odds
    #stay_odds
    #difference,above,below=get_win_odds(odd_distr,hands=[dealer,player],verbose=False)
    
    
#     possible_odds=[]
#     for i in range(0,len(possible_hands[0])):
#         it=possible_hands[0][i]
#         if len(player)+1 <= len(it):
#             possible_future_hands[0].append(possible_hands[0][i])
#             possible_future_hands[1].append(possible_hands[1][i])
#             possible_future_hands[2].append("")
#             possible_future_hands[3].append(possible_hands[3][i])
#             possible_odds.append(possible_hands[1][i])

    #odd_distr=get_odds_distribution(card_deck_copy,possible_future_hands,upper_set,relative=sum(playerOdds),verbose=False)
    #hit_odds
    #difference,above,below=get_win_odds(odd_distr,hands=False,verbose=False)
    #hit_odds=hit_odds

    #print odd_distr
    return possible_hands,stay_odds,hit_odds