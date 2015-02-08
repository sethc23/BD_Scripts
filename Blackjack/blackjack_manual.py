from random import choice as rc
from random import shuffle as sh

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

def new_deck(cards, decks):
    card_deck = []
    for i in range(0, decks):
        for j in range(0, 4):
            card_deck.extend(cards)
    sh(card_deck) 
    return card_deck

def get_card_vals(card):
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    card_vals = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    return card_vals[cards.index(card)]


print ''
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
card_vals = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
decks = 4
reshuffleAtPercentage = 70
dealerPeak = True
blackjackEarnings = 3.0 / 2.0
AcesSplitOnly = True
playerHands = 1
bankroll = 1000
bankHigh, bankLow = bankroll, bankroll
print 'Decks:', decks
print 'Reshuffle at', reshuffleAtPercentage, '%'
print 'Dealer Peak for Blackjack?', dealerPeak
print 'BlackJack Earnings Ratio:', blackjackEarnings, 'to 1'
print 'One hit on Aces Split?', AcesSplitOnly
print 'Number of player hands:', playerHands
print 'Bankroll:', bankroll

quit = False
cwin = 0  # computer win counter
pwin = 0  # player win counter
card_deck = new_deck(cards, decks)
print ''
while True:
    # reshuffle when deck of cards is low....
    if len(card_deck) <= ((reshuffleAtPercentage / 100.00) * (len(cards) * 4) * decks):
        print 'Shuffling...'
        print ''
        card_deck = new_deck(cards, decks)
    # deal cards to player and dealer, take bets per hand
    player, bet, pbust, dealer = [], [], [], []
    for i in range(0, playerHands):  # each player has at least one hand, 
                                    # each hand has a bet, 
                                    # each hand has 'busted' flag
        bet.append([])
        bet[i] = raw_input("Remaining money = $ %s. Place Bet or Quit (q): " % bankroll)
        if bet[i] == 'q':
            quit = True
            break
        else:
            bet[i] = eval(bet[i])
        pbust.append(False)
        player.append([])
        player[i].append(card_deck.pop(0))
        if len(dealer) < 2:
            dealer.append(card_deck.pop(0))
        if len(dealer) == 1:
            print "Dealer shows %s" % str(dealer[0])
        player[i].append(card_deck.pop(0))
        if len(dealer) < 2:
            dealer.append(card_deck.pop(0))
        
    if quit == True:
        break
    cbust = False  # computer busted flag
    # play player hands
    for hand in player:
        while True:
            hand_index = player.index(hand)
            hand_val = [get_card_vals(x) for x in hand]
            tp = total(hand_val)
            # Option for Dealer to check for Blackjack (sometimes a U.S. rule)
            if dealerPeak == True:
                dealer_card_vals = [get_card_vals(x) for x in dealer]
                tc = total(dealer_card_vals)                
                if tc == 21:
                    hand_val = [get_card_vals(x) for x in hand]
                    tp = total(hand_val)
                    break
            if tp > 21:
                print "->  (h:" + str(hand_index + 1) + ") player %s = %d" % (hand, tp), ' BUST.'
                pbust[hand_index] = True
                break
            elif tp == 21:
                # Option for house paying out better for dealing blackjack to player
                if len(hand) == 2:
                    bet[hand_index] = round(bet[hand_index] * blackjackEarnings, 2)
                    print "->  (h:" + str(hand_index + 1) + ") player %s = %d" % (hand, tp), ' BLACKJACK'
                break
            else:
                print "->  (h:" + str(hand_index + 1) + ") player %s = %d" % (hand, tp)
                if hand[0] == hand[1]:
                    hs = raw_input("? Hit, Split, Stand, or Double (h, spl, s, or d): ").lower()
                elif len(hand) == 2:
                    hs = raw_input("? Hit, Stand, or Double (h, s, or d): ").lower()
                else:
                    hs = raw_input("? Hit or Stand (h or s): ").lower()
                if hs == 'h':
                    hand.append(card_deck.pop(0))
                # Player choice to split hands....
                elif hs == 'spl':
                    if hand[0] == 'A' and hand[1] == 'A':  # Rule that player splitting Aces cannot hit
                        if AcesSplitOnly == True: splitOnce = True
                        else: splitOnce = False
                    else: splitOnce = False
                    temp_card = hand[1]
                    hand[1] = card_deck.pop(0)
                    player.append([temp_card, card_deck.pop(0)])
                    bet.append(bet[hand_index])
                    pbust.append(False)
                    for split_hand in player:
                        hand_index = player.index(split_hand)
                        hand_val = [get_card_vals(x) for x in split_hand]
                        tp = total(hand_val)
                        print "-> (split h:" + str(hand_index + 1) + ") player %s = %d" % (split_hand, tp)
                    if splitOnce == True: break
                # Player choice to hit once and double bet....
                elif hs == 'd':
                    bet[hand_index] += bet[hand_index]
                    hand.append(card_deck.pop(0))
                    hand_val = [get_card_vals(x) for x in hand]
                    tp = total(hand_val)
                    if tp > 21:
                        print "->  (h:" + str(hand_index + 1) + ") player %s = %d" % (hand, tp), ' BUST.'
                        pbust[hand_index] = True
                    else:
                        print "->  (h:" + str(hand_index + 1) + ") player %s = %d" % (hand, tp)
                    break                 
                elif hs == 's':
                    break
                else:
                    break
    while True:
        # loop for the computer's play ...
        # dealer generally stands around 17 or 18
        while True:
            dealer_card_vals = [get_card_vals(x) for x in dealer]
            tc = total(dealer_card_vals)                
            if tc < 17:
                dealer.append(card_deck.pop(0))
            else:
                break
        if tc > 21:
            print "--> dealer %s = %d" % (dealer, tc), ' BUST.'
        else:
            print "--> dealer %s = %d" % (dealer, tc)
        # now figure out who won ...
        for hand in player:
            hand_index = player.index(hand)
            hand_val = [get_card_vals(x) for x in hand]
            tp = total(hand_val)
            if tc > 21:
                cbust = True
                if pbust[hand_index] == False:
                    print "- (h:" + str(hand_index + 1) + ") Win.  +$" + str(bet[hand_index])
                    bankroll += bet[hand_index]
                    pwin += 1
                else: print "---> (h:" + str(hand_index + 1) + ") Push."
            elif tc > tp:
                print "- (h:" + str(hand_index + 1) + ") Lose.  -$" + str(bet[hand_index])
                bankroll -= bet[hand_index]
                cwin += 1
            elif tc == tp:
                print "---> (h:" + str(hand_index + 1) + ") Push."
            elif tp > tc:
                if pbust[hand_index] == False:
                    print "- (h:" + str(hand_index + 1) + ") Win.  +$" + str(bet[hand_index])
                    bankroll += bet[hand_index]
                    pwin += 1
                elif cbust == False:
                    print "- (h:" + str(hand_index + 1) + ") Lose.  -$" + str(bet[hand_index])
                    bankroll -= bet[hand_index]
                    cwin += 1
        if bankroll > bankHigh:
            bankHigh = bankroll
        if bankroll < bankLow:
            bankLow = bankroll
        break
    print '**'
print ''
print ("Wins, player = %d  computer = %d" % (pwin, cwin))
print 'Highest Bankroll:', bankHigh, ' --  Lowest Bankroll:', bankLow
