import random
from ModelDesision import model_decision
import tensorflow as tf
new_model = tf.keras.models.load_model('basic_model_highlow.keras')
def find_total(hand):
    face_cards = ['J', 'Q', 'K']
    aces = 0
    hand_value = 0
    # a card will either be a face card, an ace, or an int
    #for a face card add 10, for an int add the int value, for ace count it
    # and determine its impact on the hand value at the end
    for card in hand:
        if card == 'A':
            aces += 1
        elif card in face_cards:
            hand_value += 10
        else: 
            hand_value += card
    # at this point we can determine the value in the hand with the aces
    if aces == 0:
        return hand_value
    else:
        hand_value += aces
        if hand_value + 10 < 22:
            return (hand_value + 10)
        else:
            return hand_value


def logicalDecision(inital_player_hand_value, player_hand, current_count, dealer_card):
     #Never hit over 17
    if inital_player_hand_value < 16:
        # play a no bust strategy when the count is high meaning many face cards
        if current_count > 3 and find_total(player_hand) > 12:
            return 0
        else:
            if find_total(player_hand) < 14:
                dealer_card_showing = find_total([dealer_card])
                # if dealer is looking at a 4 or a 5 that is there weakest hand so I dont want to hit
                if (dealer_card_showing == 5) and inital_player_hand_value > 13:
                    return 0
                elif find_total(player_hand) == dealer_card_showing + 11:
                    return 0
                elif dealer_card_showing > 6:
                    return 1
                elif find_total(player_hand) < dealer_card_showing + 11:
                    return 1 
                else: 
                    return 0
    else:
        return 0
def dealerLogic(player_hand):
    if find_total(player_hand) < 17:
        return 1
    else:
        return 0
def dealerLogicWithCount(player_hand, current_count):
    if find_total(player_hand) < 11:
        return 1
    elif current_count > 2:
        return 0
    elif find_total(player_hand) < 17:
        return 1
    else:
        return 0
    
def noBust(player_hand):
    if find_total(player_hand) < 12:
        return 1
    else:
        return 0
    
def high_low_count_logic(inital_player_hand_value, player_hand, current_count, dealer_card):
    # If the count is very low the deck is full of smaller cards so be more agressive
    if current_count < -6 and find_total(player_hand) < 18:
        return 1
    else:
        # play a no bust strategy when the count is high meaning many face cards
        if current_count > 3 and find_total(player_hand) > 12:
            return 0
        else:
            if find_total(player_hand) < 14:
                dealer_card_showing = find_total([dealer_card])
                # if dealer is looking at a 4 or a 5 that is there weakest hand so I dont want to hit
                if (dealer_card_showing == 5) and inital_player_hand_value > 12:
                    return 0
                elif find_total(player_hand) == dealer_card_showing + 11:
                    return 0
                elif dealer_card_showing > 6:
                    return 1
                elif find_total(player_hand) < dealer_card_showing + 11:
                    return 1 
                else: 
                    return 0
def randomChoice(inital_player_hand_value, player_hand, current_count, dealer_card):
    choice = random.randint(1,3)
    if choice == 1:
        return high_low_count_logic(inital_player_hand_value, player_hand, current_count, dealer_card)
    elif choice == 2:
        return noBust(player_hand)
    else:
        return dealerLogic(player_hand)

def controller(choice, inital_player_hand_value, player_hand, current_count, dealer_card, num_hits):
    if choice == 'random':
        return randomChoice(inital_player_hand_value, player_hand, current_count, dealer_card)
    elif choice == 'highlow':
        return high_low_count_logic(inital_player_hand_value, player_hand, current_count, dealer_card)
    elif choice == 'nobust':
        return noBust(player_hand)
    elif choice == 'dealer':
        return dealerLogic(player_hand)
    elif choice == 'high':
        return logicalDecision(inital_player_hand_value, player_hand, current_count, dealer_card)
    elif choice == 'model':
        return model_decision(new_model, find_total([dealer_card]), find_total(player_hand), current_count, num_hits)
    else:
        print('not an option try again')