import random
import time


def get_total(hand):   # Returns values in this format- [Hand_value, #Aces, Card 1, Card 2, ...]
    value = 0
    has_ace = 0
    cards = []
    for card in hand:
        if card[0] == "A":
            value += 11
            has_ace += 1
        elif card[0] in ["K", "Q", "J", "T"]:
            value += 10
        else:
            value += int(card[0])
        cards.append(card[0])

    while value > 21:
        if has_ace > 0:
            value -= 10
            has_ace -= 1
        else:
            break

    info = [value, has_ace] + cards
    return info


def print_cards(hand, facedown=0):
    row_1 = ""
    row_2 = ""
    row_3 = ""
    row_4 = ""
    for card in hand:
        if facedown and card == hand[0]:
            row_1 += " ___"
            row_2 += "|██"
            row_3 += "|██"
            row_4 += "|██"
        else:
            row_1 += " __"
            row_2 += "| " + card[0]
            row_3 += "| " + card[2]
            row_4 += "|__"
    row_1 += "_ "
    row_2 += " |"
    row_3 += " |"
    row_4 += "_|"
    print(row_1)
    print(row_2)
    print(row_3)
    print(row_4)
    return


def split_hand(hand):

    global top_card
    hand_1 = hand[0]
    hand_2 = hand[1]
    hand_1.append(shuffled_deck[top_card])
    top_card += 1
    hand_2.append(shuffled_deck[top_card])
    top_card += 1
    hands = [hand_1, hand_2]
    print_cards(hand_2)
    print("Second Hand")
    print_cards(hand_1)
    print("First Hand.\nWe will play this hand first.")

    return hands


def finish_hand(user_cards):  # Loop for User to finish their hand
    global top_card
    global outcome
    can_double = True
    total = 0

    while True:
        accepted = "H h S s"
        message = "What would you like to do? \n[H for Hit, S for stay.]"
        if can_double:
            accepted += " D d"
            message = message[:-2]
            message += ", or D to Double down.]"
            can_double = False

        print(message)
        response = input()

        while response not in accepted:

            print("Please type an accepted answer.")
            response = input()

        if response in "H h":
            user_cards.append(shuffled_deck[top_card])
            top_card += 1
            total = get_total(user_cards)
            print_cards(user_cards)

        elif response in "S s":

            total = get_total(user_cards)
            print("Staying at " + str(total[0]))
            break

        elif response in "D d":

            print("Double Down")
    #   enter double down code here

        print("You are at " + str(total[0]))
        if total[0] > 21:
            outcome = "bust"
            print("You have busted out.")
            break
    return total[0]


def dealer_finish(hand):

    global outcome
    global top_card
    total = get_total(hand)

    while True:

        print_cards(hand)
        print("Dealer has " + str(total[0]))
        time.sleep(1)

        if total[0] < 17:  # Dealer Hits on 16 or lower, stays on 17

            hand.append(shuffled_deck[top_card])
            top_card += 1
            total = get_total(hand)
            print("Dealer hits.")

        elif total[0] > 21:
            print("Dealer Busts. Player wins.")
            outcome = "win"
            break

        elif total[0] >= 17:
            print("Dealer stays at " + str(total[0]) + ".")
            break

    return total[0]


deck = ["2 ♦", "3 ♦", "4 ♦", "5 ♦", "6 ♦", "7 ♦", "8 ♦", "9 ♦", "T ♦", "J ♦", "Q ♦", "K ♦", "A ♦",
        "2 ♥", "3 ♥", "4 ♥", "5 ♥", "6 ♥", "7 ♥", "8 ♥", "9 ♥", "T ♥", "J ♥", "Q ♥", "K ♥", "A ♥",
        "2 ♣", "3 ♣", "4 ♣", "5 ♣", "6 ♣", "7 ♣", "8 ♣", "9 ♣", "T ♣", "J ♣", "Q ♣", "K ♣", "A ♣",
        "2 ♠", "3 ♠", "4 ♠", "5 ♠", "6 ♠", "7 ♠", "8 ♠", "9 ♠", "T ♠", "J ♠", "Q ♠", "K ♠", "A ♠"]


want_to_play = True

print("Let's play blackjack. How many chips would you like? \n[Enter a dollar amount, or press Enter to Leave]")

player_chips = input()
current_player_chips = 0

if player_chips == "":
    want_to_play = False
else:
    current_player_chips = int(player_chips)

shuffled_deck = deck
top_card = 0

while want_to_play:

    if top_card == 0 or top_card >= 39:
        random.shuffle(shuffled_deck)
        top_card = 0
        print("Shuffling...")
        time.sleep(1)

    print("You have " + str(current_player_chips) + " chips. How much would you like to wager?\n[Press enter to quit]")
    bet = input()
    outcome = ""

    if bet == "":
        want_to_play = False
        break
    else:
        bet = int(bet)

    print("Dealing Cards.")

    player_hand = []
    dealer_hand = []

    for i in range(2):
        player_hand.append(shuffled_deck[top_card])
        top_card += 1
        dealer_hand.append(shuffled_deck[top_card])
        top_card += 1

    player_value = get_total(player_hand)
    dealer_value = get_total(dealer_hand)

    # Displaying Cards
    time.sleep(1)
    print_cards(dealer_hand, 1)
    print("Dealer's hand\n\n")
    print_cards(player_hand, 0)
    print("Your hand\n\n")
    time.sleep(1)

    insurance = 0

    if dealer_value[3] == "A":  # Handling for Possible dealer blackjack

        print("Ace showing. Would you like to purchase insurance? You can purchase up to " + str(bet / 2) +
              " [Enter an amount, or press Enter for no]")
        insurance = input()

        if insurance:
            print("Insurance purchased.")
            insurance = -int(insurance)
        else:
            print("No insurance purchased.")
            insurance = 0

        if dealer_value[1] == 21:

            print_cards(dealer_hand, 0)
            print("Dealer has BlackJack.")

            if player_value[1] == 21:
                print("Player also has Blackjack. Hand is a push")
                outcome = "push"

            else:
                print("Player Loses. Better luck next hand!")
                outcome = "lose"

            if insurance < 0:
                print("Insurance pays off 2:1")
                insurance *= -2
        else:
            print("No dealer Blackjack. Play on.")

    while not outcome:

        split = ""

        if player_value[0] == 21:
            print("Player has Blackjack. Payout is 3:2")
            outcome = "win"
            bet *= 1.5
            continue

        print("Dealer has " + dealer_value[3] + " showing.\nPlayer has " + str(player_value[0]) + ".")

        if player_value[2] == player_value[3] or (player_value[0] == 20 and player_value[2] == 0):
            print("Would you like to Split? \n[Press Y to split, or Enter to keep your hand.]")
            split = input()
            if split.upper() == "Y":
                player_hand = split_hand(player_hand)
                split = True
            else:
                split = False

        player_total = finish_hand(player_hand)

        if split:
            finish_hand(player_hand[1])

        dealer_total = dealer_finish(dealer_hand)

        if not outcome:
            if player_total > dealer_total:
                outcome = "win"
            elif player_total < dealer_total:
                outcome = "lose"
            else:
                outcome = "push"

        continue

    if outcome == "win":
        current_player_chips += bet
        current_player_chips += insurance
        print("You win! You won " + str(bet) + " chips.")
    elif outcome == "lose":
        current_player_chips -= bet
        current_player_chips += insurance
        print("You lost " + str(bet) + " chips.")
    elif outcome == "push":
        current_player_chips += insurance
        print("Hand was a push.")
