import numpy as np
import pandas as pd

class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []  # Holds Agent's current cards
        self.players = []  # Holds the current players name
        # Stores the game data as Pandas dataframe
        self.data = pd.DataFrame(columns=['lead', 'winner', 'trick'])
        self.cardsplayed = {}
        
        self.Spades = ["2S","3S","4S","5S","6S","7S","8S","9S","TS","JS","QS","KS","AS"]
        self.Hearts = ["2H","3H","4H","5H","6H","7H","8H","9H","TH","JH","QH","KH","AH"]
        self.Clubs = ["2C","3C","4C","5C","6C","7C","8C","9C","TC","JC","QC","KC","AC"]
        self.Diamonds = ["2D","3D","4D","5D","6D","7D","8D","9D","TD","JD","QD","KD","AD"]
        self.trump_suite = 'S'        
        
    
    def parse_trick(self, trick):
        card_dict = {'A': 13, 'K':12,'Q':11,'J':10 ,'T':9, '9': 8, '8': 7, '7':6,'6':5,'5':4 ,'4':3, '3': 2 , '2':1} # Assigning the face cards with numbers for comparison
        card_num = []
        cards = []
        if len(trick) > 0:
            for i in trick:
                cards.append(i[:-1])
            for i in cards:
                card_num.append(card_dict[i]) 
            return card_num
        else:
            return []

    def analyse_hand(self,hand): # Modification over Nishan's code. 
    # Create the dictionary which calculates the number of cards of each suit
        suit_list = {'C','D','H','S'}
        suit_totals = {}
        for suit in suit_list:
            sum = 0
            for card in hand:
                if card[-1] == suit:
                    sum += 1
                    if sum == 0:
                        continue
                    suit_totals[suit] = sum
        return suit_totals 

    def get_name(self):
        """
        Returns a string of the agent's name
        """
        return str(self.name)

    def get_hand(self):
        """
        Returns a list of two character strings reprsenting cards in the agent's hand
        """
        return self.hand

    def new_hand(self, names):
        """
        Takes a list of names of all agents in the game in clockwise playing order
        and returns nothing. This method is also responsible for clearing any data
        necessary for your agent to start a new round.
        """
        self.players = names  # Setting the names of players to the agent
        self.hand = []  # Resetting the hand of the agent
        # Resetting the dataframe
        self.data = pd.DataFrame(columns=['lead', 'winner', 'trick'])
        self.Spades = ["2S","3S","4S","5S","6S","7S","8S","9S","TS","JS","QS","KS","AS"]
        self.Hearts = ["2H","3H","4H","5H","6H","7H","8H","9H","TH","JH","QH","KH","AH"]
        self.Clubs = ["2C","3C","4C","5C","6C","7C","8C","9C","TC","JC","QC","KC","AC"]
        self.Diamonds = ["2D","3D","4D","5D","6D","7D","8D","9D","TD","JD","QD","KD","AD"]   
        

    def add_cards_to_hand(self, cards):
        """
        Takes a list of two character strings representing cards as an argument
        and returns nothing.
        This list can be any length.
        """
        self.hand = cards
        
    
    def trackingCards(self, trick, suite):
        track_cards = [self.Spades[-1],self.Hearts[-1],self.Diamonds[-1],self.Clubs[-1]]
        
        
        if(suite==None):
            return track_cards
        
        elif len(trick) > 0:
            for card in trick:
                if card[-1] == "C":
                    if len(self.Clubs) > 0:
                        self.Clubs.remove(card)
                        track_cards[3] = self.Clubs[-1]  
                    
                elif card[-1] == "S":
                    if len(self.Spades) > 0:
                        self.Spades.remove(card)
                        track_cards[0] = self.Spades[-1]

                        
                elif card[-1] == "H":
                    if len(self.Hearts) > 0:
                        self.Hearts.remove(card)
                        track_cards[1] = self.Hearts[-1]
                
                elif card[-1] == "D":
                    if len(self.Diamonds) > 0:
                        self.Diamonds.remove(card)
                        track_cards[2] = self.Diamonds[-1]
                        
            return track_cards        
        
        
    def trackOpponent(self, suite = None):
        Spades = ["2S","3S","4S","5S","6S","7S","8S","9S","TS","JS","QS","KS","AS"]
        Hearts = ["2H","3H","4H","5H","6H","7H","8H","9H","TH","JH","QH","KH","AH"]
        Clubs = ["2C","3C","4C","5C","6C","7C","8C","9C","TC","JC","QC","KC","AC"]
        Diamonds = ["2D","3D","4D","5D","6D","7D","8D","9D","TD","JD","QD","KD","AD"]
        opp_cards_dict = {'S':Spades,'H':Hearts,'D':Diamonds,'C':Clubs}
        
        hand = self.get_hand()
        for card in hand:
                if card[-1] == "C":
                    Clubs.remove(card)        #argmax of np can be used
                    
                elif card[-1] == "S":
                    Spades.remove(card)
                    
                elif card[-1] == "H":
                    Hearts.remove(card)
                    
                elif card[-1] == "D":
                    Diamonds.remove(card)
                    
        if suite is not None:
            return opp_cards_dict[suite]
        else:
            return opp_cards_dict 
    
    def select_card(self,trick,available_actions,oponent_hand=None):  
        action_num = self.parse_trick(available_actions) # Converting agent's available actions to numerical values
        game_len = len(trick) # How many hands has been passed in the trick
        if game_len == 2: ## Case 3 Agent is the third player 
            temp_trick = trick # Storing trick in a temporary variable
            evals = []
            for action in available_actions:
                temp_trick.append(action)
                oponent_card = self.select_card(temp_trick,oponent_hand)
                temp_trick.append(oponent_card)
                utility = self.evaluate(temp_trick,2)
                evals.append(utility)
                temp_trick = temp_trick[:-2] # Popping the last two element.
                eval_sum = np.sum(evals)
            if eval_sum == 0:
                indx = np.argmin(action_num)        # returns the minimum value in the axis = 0
                selected_card = available_actions[indx]
            else:
                indx = list(np.flatnonzero(evals)) # Getting the index of non zero elements
                valid_actions = [available_actions[i] for i in indx]
                valid_actions_num = [action_num[i] for i in indx] # Numerical represtation of valid actions
                indx = np.argmin(valid_actions_num)
                selected_card = valid_actions[indx]
            return selected_card

        elif game_len == 3: ## Case 4 Agent is the final player
            temp_trick = trick # Storing trick in a temporary variable
            evals = []
            for action in available_actions:  
                temp_trick.append(action)
                utility = self.evaluate(temp_trick,3)
                evals.append(utility)
                temp_trick.pop(-1) # Popping the last element.
            eval_sum = np.sum(evals)
            if eval_sum == 0:
                indx = np.argmin(action_num)
                selected_card = available_actions[indx]  
            else:
                indx = list(np.flatnonzero(evals)) # Getting the index of non zero elements
                valid_actions = [available_actions[i] for i in indx]
                valid_actions_num = [action_num[i] for i in indx] # Numerical represtation of valid actions
                indx = np.argmin(valid_actions_num)
                selected_card = valid_actions[indx]
            return selected_card
    
    def play_card(self, lead, trick):
        """
        Takes a a string of the name of the player who lead the trick and
        a list of cards in the trick so far as arguments.

        Returns a two character string from the agents hand of the card to be played
        into the trick.
        """
        # Starting a game with 2 of clubs
        game_len=len(trick)
        if game_len == 0:
            available_actions = self.get_hand()
            available_cards = [i for i in available_actions]
            action_num = self.parse_trick(available_cards) # Converting agent's available actions to numerical values
            
            track = self.trackingCards(trick, None)
                
            if '2C' in available_actions:       #Checking inhand if we have 2C
                selected_card = '2C'
            
            #case 2: playing highest 
            elif '2C' not in available_actions:
                highest_lead_card = track
                highest_lead_card_num = self.parse_trick(highest_lead_card)
                if max(action_num) in highest_lead_card_num:
                    selected_card_indx = np.argmax(action_num)
                    selected_card = available_actions[selected_card_indx]
                else:
                    selected_card_indx = np.argmin(action_num)
                    selected_card = available_actions[selected_card_indx]
                                        
        
        elif game_len == 1:     
            available_actions = self.get_hand()
            trick_suite = trick[0][-1]
            available_cards = [i for i in available_actions if i[-1] == trick_suite] # Getiing all cards with the selected suite from agent's hand
            action_num = self.parse_trick(available_cards) # Converting agent's available actions to numerical values
            
            track = self.trackingCards(trick, trick_suite)
            highest_lead_card = track
            highest_lead_card_num = self.parse_trick(highest_lead_card)
            
            if len(available_cards) == 0:
                selected_card = self.burn_card()

            elif len(available_cards) == 1:
                selected_card = available_cards[0]
                
            else:
                if max(action_num) in highest_lead_card_num:
                    selected_card_indx = np.argmax(action_num)
                    selected_card = available_cards[selected_card_indx]
                    
                else:
                    selected_card_indx = np.argmin(action_num)
                    selected_card = available_cards[selected_card_indx]
                
        elif game_len == 2 or game_len == 3:
            available_actions = self.get_hand()
            trick_suite = trick[0][-1]
            available_cards = [i for i in available_actions if i[-1] == trick_suite] # Getiing all cards with the selected suite from agent's hand
            action_num = self.parse_trick(available_cards) # Converting agent's available actions to numerical values
            opponent_cards = self.trackOpponent(trick_suite)
            if len(available_cards) == 0:
                selected_card = self.burn_card()
            
            elif len(available_cards) == 1:
                selected_card = available_cards[0]
            else:
                selected_card = self.select_card(trick, available_cards, opponent_cards)  
                print(selected_card)
        # remove the selected card from the hand and return that card
        self.hand.remove(selected_card)
        #print("Selected Card:",selected_card)
        #print('Av c',available_cards)
        #print("Trick",trick)
        #print("Hand",self.get_hand())
        return selected_card
    
    def evaluate(self,trick,agent_pos):
        card_nums = self.parse_trick(trick)
        for i,card in enumerate(trick):
            if card[-1] == self.trump_suite:
                card_nums[i]+=13
            elif card[-1] != trick[0][-1]:
                card_nums[i]-=13
        max_card_indx = np.argmax(card_nums) # Finding the index of winning card
        if max_card_indx == agent_pos:
            return 1
        else:
            return 0
    
    
    def collect_trick(self, lead, winner, trick):
        """
        Takes three arguements. Lead is the name of the player who led the trick.
        Winner is the name of the player who won the trick. And trick is a four card
        list of the trick that was played. Should return nothing.
        """
        temp_dict = {'lead': lead, 'winner': winner, 'trick': [trick]}  # Passing all data as list, so 'pandas' see this as a single row of data
        temp_df = pd.DataFrame(temp_dict)
        # Appending the new data to Agent's data
        self.data = self.data.append(temp_df, ignore_index=True)

    def score(self):
        """
        Calculates and returns the score for the game being played.
        """
        winners = list(self.data['winner'])  # Getting the list of the trick winners
        player_name = self.get_name()  # Getting the agent's name
        wins = winners.count(player_name)  # Counting the number of wins
        return wins

    
    def burn_card(self):
        hand = self.get_hand() # Getting Agent's current hand
        trumps = [i for i in hand if i[-1] == self.trump_suite]
        if len(trumps) == 0: # We are burning a card if we do not have any trump cards
            suit_total = self.analyse_hand(hand) # Computing how many cards from each suite is present
            suits = [i[0] for i in suit_total if i[-1] != self.trump_suite] # Separating the suites from suit_total dictionary without the trumps
            num_cards = [i for i in suit_total.values()] # Separating the numbers from suit_total dictionary
            # Logic for determining which suite the agent going to burn
            possible_burn = []
            for i,nums in enumerate(num_cards):
                if nums == 1: # If only one card is present for any suite, append that suite
                    possible_burn.append(suits[i])
            sorted_suit_total = sorted(suit_total.items(),key = lambda x:x[1]) # Sorting the suit_total to find the suite with highest number of cards
            high_card_suite = sorted_suit_total[-1][0]
            possible_burn.append(high_card_suite) # Adding the suit with highest number of cards for possible burn
            available_cards = [i for selected_suite in possible_burn for i in hand if i[-1] == selected_suite] # Getiing all cards with the selected suite from agent's hand
            available_cards_num = self.parse_trick(available_cards) # Converting the cards into numerals for comparison
            card_indx = np.argmin(available_cards_num) # Getting the index of the lowest card
            selected_card = available_cards[card_indx] # Getting the lowest card for burn
           
        else:
            trump_nums = self.parse_trick(trumps)
            card_indx = np.argmin(trump_nums) # Getting the index of the lowest card
            selected_card = trumps[card_indx] # Getting the lowest card for trump
           
        return selected_card
    
    
if __name__ == "__main__":
    pass