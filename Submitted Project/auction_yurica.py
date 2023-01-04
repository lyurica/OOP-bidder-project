import copy
import numpy as np

class User:
    """Class to represent a user with a secret probability of clicking on an ad"""
    total_users = 0
    def __init__(self):
        self.__probability = np.random.uniform()
        self.user_id = User.total_users
        User.total_users +=1

    @property
    def get_prob(self):
        """secret probability getter"""
        return self.__probability


    def __repr__(self):
        return "User #" +str(self.user_id)

    def __str__(self):
        return str("class with hidden probability")

    def show_ad(self):
        """Method that models user ad behavior. Returns True to represent 
        user clicking on ad False otherwise."""

        return np.random.choice([True,False], p = [self.__probability, 1-self.__probability])

class Auction:
    """users is expected to contain a list of all User objects. bidders is
     expected to conain a list of all Bidder objects"""
    round = 0
    def __init__(self, users, bidders):
        self.history = []
        self.users = users
        self.bidders = bidders
        self.starting_balances_ls = [0]*len(bidders)
        self.starting_bal = {} 
        for bid, dollars in zip(self.bidders,self.starting_balances_ls):
            self.starting_bal[bid] = dollars
        self.balances = self.starting_bal

    def balance_get(self):
        """returns balances for bidders as a dictionary"""
        return self.balances
    
    def balance_set(self,bidder,money_gained = 0, money_spent = 0):
        """sets balances for bidders in dictionary"""
        self.balances[bidder] += money_gained - money_spent
        
    def __repr__(self):
        return str("Class representing Auction game")

    def __str__(self):
        return self.__repr__()

    def execute_round(self):
        """Should execute all steps within a single round of the game."""
        chosen_user = np.random.choice(self.users)
        submitted_bids = []
        bidder_list = copy.copy(self.bidders)
        
        #check user balances to ensure no one is out
        for identity , money  in self.balances.items():             
            if money < -1000 and identity in bidder_list:
                bidder_list.remove(identity)

        #collect user bids
        for individual in bidder_list:
            submitted_bids.append((individual, individual.bid(chosen_user)))
        submitted_bids = sorted(submitted_bids, key = lambda x: (x[1]))     
        
        #check user bids are not negative
        valid_bids = list(filter(lambda x: (x[1]>=0),submitted_bids))

        #handle ties, equal chance at winning
        max_bid = valid_bids[-1][1]
        winners_list = list(filter(lambda x: x[1] == max_bid,valid_bids))
        
        winner = winners_list[np.random.choice(range(len(winners_list)))][0]
        
        #winner pays second place bid
        if len(valid_bids)>1:
            valid_bids.pop()
        cost_of_ad = valid_bids.pop()[1]

        #check if user clicked ad
        clicked = chosen_user.show_ad()

        #notify all bidders if they won and what winning price was
        #winning bidder told if user clicked
        for bid in self.bidders:
            if bid == winner:
                bid.notify(True,cost_of_ad,clicked)
            else:
                bid.notify(False,cost_of_ad,None)
        
        #increment winning bidder balance by 1 if user clicked.
        # Decrease balance by winning price.
        self.balance_set(winner,clicked,cost_of_ad)
        
        #update history of balances
        round_balances = [self.balances[buyer] for buyer in self.bidders]
        self.history.append(round_balances)

