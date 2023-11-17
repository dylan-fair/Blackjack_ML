#blackjack simulator

import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
from DescisionMakers import controller

def BlackJackData(num_decks = 5, players = 4, choice = 'random', simulations = 1500):
    # lists and dicts for our cards their values and thir values for the count
    card_types = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    card_counting_dict = {'A': -1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0, 8: 0, 9: 0, 10: -1, "J": -1, "Q": -1, "K": -1}

    #makes the shoe/ shuffles the deks
    def make_shoe(num_decks, card_types):
        new_shoe = []
        for i in range(num_decks):
            for j in range(4):
                new_shoe.extend(card_types)
        #Shuffle the cards
        random.shuffle(new_shoe)
        return new_shoe

    '''
    This function will return the current card count. using the known cards that have been removed
    and then calculate the count, the strategy for the count
    works as follows, 2-6 are +1 as it is good to remove low cards, 7-9 will be 0 as they dont affect the game
    and 10-A will be -1 as these are the cards we want. After this addition has been done yuou divide by the
    number of decks in play to determine the true count.
    '''
    def calculateCount(cards_delt):
        current_count = 0
        num_cards_taken = 0
        total_decks = num_decks
        for key in cards_delt:
            current_count += card_counting_dict[key] * cards_delt[key]
            num_cards_taken += cards_delt[key]
        num_decks_left = (total_decks - (num_cards_taken // 52))
        return current_count // num_decks_left 

        

    # write the function to get the value in a hand
    # pass a hand in as a list of cards and return the value in the hand
    # count aces as 11 if possible, 1 if not. Face cards have value 10
    # need to count the number of aces and determine those possible values 
    # finalize the result after examining the other cards in the hand
    # TODO: improve this component possible is soft attribute.
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
            
    #next, let's simulate ONE game, once the cards have been dealt...we will use this function to determine the player strategy
    #dealer_hand: 2 cards the dealer has
    #player_hands: the cards that the players have
    #curr_player_results: a list containing the result of each player's hand for this round; if there are three players, it might be [1, -1, 1]
    #dealer_cards: the cards left in the shoe; the shoe with the cards that have been dealt to the players for hitting will have been removed
    #hit_stay: is used to determine if a player hits or stays...you'll probably modify this in your own decision-making process
    #card_count: a dictionary to store the counts of the various card values that have been seen, for future card
    #counting in influencing our decision making and training data
    def play_hand(dealer_hand, player_hands, curr_player_results, dealer_cards, hit_stay, card_count, dealer_bust):
        player_card_count = []
        player_num_hits = []
        
        #first, check if the dealer has blackjack.  that can only happen if the dealer has a total of 21, logically, and 
        #the game will be over before it really gets started...the players cannot hit
        if (len(dealer_hand) == 2) and (find_total(dealer_hand) == 21):
            for player in range(players):
                #update live_action for the players, since they don't have a choice
                live_action.append(0)
                current_count = calculateCount(card_count)
                player_card_count.append(current_count)
                
                #check if any of the players also have blackjack, if so, they tie, and if not, they lose
                if (len(player_hands[player]) == 2) and (find_total(player_hands[player]) == 21):
                    curr_player_results[0, player] = 0
                else:
                    curr_player_results[0, player] = -1    
                player_num_hits.append(0)
        
        #now each player can make their decisions...first, they should check if they have blackjack
        #for this player strategy, the decision to hit or stay is random if the total value is less than 12...
        #so it is somewhat unrelated to the cards they actually have been dealt (and is conservative), and ignores the card 
        #that the dealer has.  We will use this strategy to generate training data for a neural network.  
        #your job will be to improve this strategy, incorporate the dealer's revealed card, train a new neural
        #network based on that simulated data, and then compare the results of your neural network to the baseline
        #model generated from this training data.
        else:
            for player in range(players):
                #the default is that they do not hit
                action = 0
                num_hits = 0
                current_count = calculateCount(card_count)
                player_card_count.append(current_count)
                inital_player_hand_value = find_total(player_hands[player])
                
                #check for blackjack so that the player wins
                if (len(player_hands[player]) == 2) and (find_total(player_hands[player]) == 21):
                    curr_player_results[0, player] = 1
                    player_num_hits.append(num_hits)

                else:
                   # Can input different simualtions into this while loop
                    while controller(choice, inital_player_hand_value, player_hands[player], current_count, dealer_hand[1], num_hits) :
                        #deal a card
                        player_hands[player].append(dealer_cards.pop(0))
                        
                        #update our dictionary to include the new card
                        card_count[player_hands[player][-1]] += 1
                        
                        #note that the player decided to hit
                        action = 1
                        num_hits += 1
                        #get the new value of the current hand regardless of if they bust or are still in the game
                        #we will track the value of the hand during play...it was initially set up in the section below,
                        #and we are just updating it if the player decides to hit, so that it changes
                        live_total.append(find_total(player_hands[player]))                      
                            
                        #if the player goes bust, we need to stop this nonsense and enter the loss...
                        #we will record their hand value outside of the while loop once we know the player is done
                        if find_total(player_hands[player]) > 21:
                            curr_player_results[0, player] = -1
                            break
                    player_num_hits.append(num_hits)
                #update live_action to reflect the player's choice
                live_action.append(action)
                        
        #next, the dealer takes their turn based on the rules
        #first, the dealer will turn over their card, so we can count it and update our dictionary; this is the FIRST card they were dealt
        card_count[dealer_hand[0]] += 1
        
        while find_total(dealer_hand) < 17:
            #the dealer takes a card
            dealer_hand.append(dealer_cards.pop(0))    
            
            #update our dictionary for counting cards
            card_count[dealer_hand[-1]] += 1
        
        
        #this round is now complete, so we can determine the outcome...first, determine if the dealer went bust
        if  find_total(dealer_hand) > 21:
            
            #the dealer went bust, so we can append that to our tracking of when the dealer goes bust
            #we'll have to track the player outcomes differently, because if the dealer goes bust, a player
            #doesn't necessarily win or lose
            dealer_bust.append(1)
            
            #every player that has not busted wins
            for player in range(players):
                if curr_player_results[0, player] != -1:
                    curr_player_results[0, player] = 1
        else:
            #the dealer did not bust
            dealer_bust.append(0)
            
            #check if a player has a higher hand value than the dealer...if so, they win, and if not, they lose
            #ties result in a 0; for our neural network, we may want to lump ties with wins if we want a binary outcome
            for player in range(players):
                if find_total(player_hands[player]) > find_total(dealer_hand):
                    if find_total(player_hands[player]) < 22:
                        curr_player_results[0, player] = 1
                elif find_total(player_hands[player]) == find_total(dealer_hand):
                    curr_player_results[0, player] = 0
                else:
                    curr_player_results[0, player] = -1    
        
        #the hand is now complete, so we can return the results
        #we will return the results for each player
        return curr_player_results, dealer_cards, card_count, dealer_bust, player_card_count, player_num_hits

    #now we can run some simulations

    card_types = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']   

    #let's keep track of each round (dealer and player hands as well as the outcome) to analyze this data
    #there is no need to break this up by simulation, since what we want to analyze are the games, regardless
    #of which simulation it is in...but we will be able to track that information through the sim_number_list
    #if we wanted to analyze our data across simulations.

    #we want the cards that the dealer was dealt throughout the simulaton
    dealer_card_history = []
    dealer_total_history = []

    #we want all of the cards dealt to each player for each of the games in the simulation
    player_card_history = []

    #we want the player's outcome for each of the games in the simulation
    outcome_history = []

    #we want the hand values tracked for each of the games in the simulation
    player_live_total = []

    #we want to know whether the player hit during each of the games in the simulation
    player_live_action = []

    #we want to know if the dealer went bust in each of the games in the simulation
    dealer_bust = []

    #we need to keep track of our card counter throughout the simulation
    card_count_list = []

    # Keep tract of the value of the card count as an int using the card count caluator function and 
    # keep a list of list where [0,1,2,3] was the count for each players hand
    player_card_count = []

    #keep track of the number of hits a player did
    player_number_hits = []
    #we will track characteristics related to the shoe or simulation, as noted above:
    first_game = True
    prev_sim = 0
    sim_number_list = []
    new_sim = []
    games_played_in_sim = []

    num_decks_sim = []
    num_players_sim = []


    #let's run our simulations

    for sim in range(simulations):
        
        #we aren't recording our data by simulation, but we could if we changed our minds
        #dealer_card_history_sim = []
        #player_card_history_sim = []
        #outcome_history_sim = []    
        
        games_played = 0
        
        #create the shoe
        dealer_cards = make_shoe(num_decks, card_types)
        
        #for each simulation, create a dictionary to keep track of the cards in the shoe, initially set to 0 for all cards
        card_count = {'A':0, 2:0, 3:0, 4:0, 5:0, 6:0,7:0, 8:0, 9:0, 10:0, 'J':0, 'Q':0, 'K':0}    
        
        #play until the shoe is almost empty...we can change this to be a function of the number of decks
        #in a shoe, but we won't start a game if there are fewer than 20 cards in a shoe...if we limit
        #the number of players to 4 (plus the dealer), then we'll need at least 10 cards for the game, and
        #we'll have enough cards for everyone to take 2...here's where the card counting could work to
        #a player's advantage
        while len(dealer_cards) > 30:
            #here's how we will manage each game in the simulation:
            
            #keep track of the outcome of the players hand after the game: it will be 1, 0, -1
            curr_player_results = np.zeros((1, players))
            
            #create the lists for the dealer and player hands
            dealer_hand = []
            player_hands = [ [] for player in range(players)]
            live_total = []
            live_action = []
            
            #deal the FIRST card to all players and update our card counting dictionary
            for player, hand in enumerate(player_hands):
                player_hands[player].append(dealer_cards.pop(0))
                card_count[player_hands[player][-1]] += 1
                
            #dealer gets a card, and the card counting dictionary is NOT updated
            dealer_hand.append(dealer_cards.pop(0))
            #card_count[dealer_hand[-1]] += 1
            
            #deal the SECOND card to all players and update our card counting dictionary
            for player, hand in enumerate(player_hands):
                player_hands[player].append(dealer_cards.pop(0))
                card_count[player_hands[player][-1]] += 1
                
            #the dealer gets a card, and our card counter will be updated with the card that is showing
            dealer_hand.append(dealer_cards.pop(0))
            card_count[dealer_hand[-1]] += 1
            
            #record the player's live total after cards are dealt...if a player hits, we will update this information
            live_total.append(find_total(player_hands[player]))
            
            #flip a fair coin to determine if the player hits or stays...we can create a bias if we want to 
            #make this more sophisticated
            hit_stay = 0.5
            
            curr_player_results, dealer_cards, card_count, dealer_bust, card_count_cal, player_num_hits = play_hand(dealer_hand, player_hands, curr_player_results, dealer_cards, hit_stay, card_count, dealer_bust)
            
            #track the outcome of the hand
            #we want to know the dealer's card that is showing and their final total
            dealer_card_history.append(dealer_hand[1])
            dealer_total_history.append(find_total(dealer_hand))
            
            #this is the result of the hand for the players
            player_card_history.append(player_hands)
            
            #we want the outcome of each hand for each player
            outcome_history.append(list(curr_player_results[0]))
            
            #we want the evolution of each player's hand in a game, as well as whether they hit or not (this is 1 if the player ever hit)
            player_live_total.append(live_total)
            player_live_action.append(live_action)

            # We want to keep track of the card count for each player in a list of list like thier hand values
            player_card_count.append(card_count_cal)

            player_number_hits.append(player_num_hits)

            num_decks_sim.append(num_decks)
            num_players_sim.append(players)
            
            if sim != prev_sim:
                new_sim.append(1)
            else:
                new_sim.append(0)
                
            if first_game == True:
                first_game = False
            else:
                games_played += 1
            
            sim_number_list.append(sim)
            games_played_in_sim.append(games_played)
            card_count_list.append(card_count.copy())
            prev_sim = sim


    #create the dataframe for analysis.  My model will have the following features:
    #the dealer's second card is the one that is face up...
    #the player's initial hand value
    #whether the player hit or not
    #whether the dealer went bust or not
    #the dealer's total value

    #the outcome: win or lose

    model_df = pd.DataFrame()

    #write the data to a csv file, in case we want to refer to it later
     # Keeps track of the number of decks
    num_decks_in_sim = []

    #Keeps track of number of players in a sim
    num_players_in_sim = []

    #Keeps track of the intial dealer card
    dealer_card = []

    #Keeps track of the dealer hand value
    dealer_value = []

    #Keeps track of the players initial value
    player_initial_value = []

    #Keeps track if a player hit or not with 1 = hit, 0 = stay
    hit = []

    #Keeps track if the dealer busted or not where 0 = no, 1 = bust
    dealer_busted = []

    #Keeps track of a players result
    results = []

    #Keeps track of a count for a player
    count = []

    #keep track of the number of times the player hit
    num_hits = []

    #num_decks,num_players,dealer_card,dealer_value,player_initial_value,hit,dealer_bust,results,player_counts
    #0,5,4,10,18,"[12, 15, 18, 12]","[1, 0, 0, 1]",0,"[-1.0, -1.0, 0.0, 0.0]","[0, -1, -1, -1]"
    dealt_hand_values = []
    for i in range(len(player_card_history)):
        hand_list = []
        hands = player_card_history[i]
        for j in range(len(hands)):
            hand_list.append(find_total(hands[j][0:2]))
        dealt_hand_values.append(hand_list.copy())

    for j in range(len(num_decks_sim)):
        for i  in range(players):
            num_decks_in_sim.append(num_decks_sim[j])
            num_players_in_sim.append(num_players_sim[j])
            dealer_card.append(dealer_card_history[j])
            dealer_value.append(dealer_total_history[j])
            player_initial_value.append(dealt_hand_values[j][i])
            hit.append(player_live_action[j][i])
            dealer_busted.append(dealer_bust[j])
            results.append(outcome_history[j][i])
            count.append(player_card_count[j][i])
            num_hits.append(player_number_hits[j][i])
    outcome_history = []

    for i in range(len(hit)):
        value = 0
        if  hit[i] == 1:
            if results[i] == -1:
                value = 0
            else:
                value = 1
        else:
            if results[i] == -1:
                value = 1
            else:
                value = 0
        outcome_history.append(value)
            


    model_df = pd.DataFrame()

    model_df['num_decks'] = num_decks_in_sim
    model_df['num_players'] = num_players_in_sim
    model_df['dealer_card'] = dealer_card
    model_df['dealer_value'] = dealer_value
    model_df['player_initial_value'] = player_initial_value
    model_df['hit'] = hit
    model_df['dealer_bust'] = dealer_busted
    model_df['results'] = results
    model_df['count'] = count
    model_df['num_hits'] = num_hits
    model_df['outcome'] = outcome_history
    model_df.to_csv(f'CSVTrainingData/blackjackdata{choice}.csv')
    print(model_df.info())
    print(model_df.describe())
    return model_df


