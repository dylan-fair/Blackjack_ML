from Eval_Data import fully_evaluate_data, evaluate_win
from BlackJackData import BlackJackData

def explore_options(): 
    choice = input('Choose which algorithm to run: random, highlow, nobust, dealer, and high')
    numSim = int(input('How many sims would you like to run'))
    num_players = int(input('How many players are there?'))
    num_decks = int(input('How many decks are there?'))
    BlackJackData(num_decks, num_players, choice, numSim)
    fully_evaluate_data(num_players, num_decks, choice)

def run_normal():
    choice = input('Choose which algorithm to run: random, highlow, nobust, dealer, and high')
    numSim = int(input('How many sims would you like to run'))
    BlackJackData(choice= choice, simulations=numSim)
    fully_evaluate_data(choice= choice)

def run_quick():
    choice = input('Choose which algorithm to run: random, highlow, nobust, dealer, model, and high')
    numSim = int(input('How many sims would you like to run'))
    BlackJackData(choice= choice, simulations=numSim)

print('How would you like to evanulate the data 1: normal run, 2: quick run, 3: explore options')
x = input()

if x == '1':
    run_normal()
elif x == '2':
    run_quick()
else:
    explore_options()