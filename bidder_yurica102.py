import numpy as np

class Bidder:
    """Class that contains the number of User objects in the game and the total number of rounds to be played"""
    bid_num = 0
    def __init__(self, num_users, num_rounds):
        self.num_users = num_users
        self.num_rounds = num_rounds
        self.current_round = 0
        self.balance = 0
        #dictionary user-> list[winning bid]
        self.price_history = {}
        self.user_click_history = {}
        self.bid_num = Bidder.bid_num
        Bidder.bid_num +=1
        self.prev_bal = 0


        if self.num_users >=4 and self.num_rounds < 3000:
            self.bid_strategy = 2

        else:
            self.bid_strategy = 1




    def __repr__(self):
        return "Yurica Bidder #" + str(self.bid_num)

    def __str__(self):
        return "Yurica Bidder"

    def avg_bid(self,user_id):
        """Uses average user click rate to create bid price, this method is used 
         when the number of users and rounds of the auction are ideal"""
        if self.user_id not in self.user_click_history:
            bid_amount = 1+((self.num_rounds-self.current_round)/self.num_rounds)
        
        elif len(self.user_click_history[self.user_id]) < 10:
            bid_amount = 1*((self.num_rounds-self.current_round)/self.num_rounds)
        
        else:
            bid_amount = np.average(self.user_click_history[self.user_id])

        self.current_round +=1
        
        return round(bid_amount,3)


    def beta_ev_bid(self,user_id):
        """Uses expected value of bayesian posterior distribution of a Bernoulli 
        distribution with a Uniform prior which results in a Beta distribution.
        The expected value for this distribution is the anticipated user click rate
         which is used to create bid price, this method is used 
         when the number of users and rounds of the auction are ideal"""

            
        if self.user_id not in self.user_click_history:
            bid_amount = 1*((self.num_rounds-self.current_round)/self.num_rounds)

        else:
            alpha = 1+np.sum(self.user_click_history[self.user_id])
            beta =  1+len(self.user_click_history[self.user_id]) - np.sum(self.user_click_history[self.user_id])
            bid_amount = alpha/(alpha+beta)
            
        return round(bid_amount,3)


    def beta_dist_bid(self,user_id):
        """Uses bayesian posterior distribution of a Bernoulli 
        distribution with a Uniform prior which results in a Beta distribution.
        bids are randomly drawn from the Beta distribution whose parameters are
        regularly updated as user click information is gained. This method is used 
         when the number of users and rounds of the auction are ideal"""

        if self.user_id not in self.user_click_history:
            bid_amount =1*((self.num_rounds-self.current_round)/self.num_rounds)

        else:
            alpha = 1+np.sum(self.user_click_history[self.user_id])
            beta =  1+len(self.user_click_history[self.user_id]) - np.sum(self.user_click_history[self.user_id])
            bid_amount = np.random.beta(alpha, beta)
            
        return round(bid_amount,3)


    def bid(self, user_id):
        """returns a non-negative amount of money, in dollars rounded to three decimal places to user_id
        evaluates balance at set intervals and changes strategy if little to no growth is occuring. Default 
        is set as user click average unless low rounds or low users and high rounds are specified."""
        #magic of decision making happens here
        #captures current balance, compares past and current balance at checkpoint
        #if balance has not increased, change bidding strategy.
        
        self.user_id = user_id
        self.checkpoint = self.num_rounds//4

        
        if self.current_round % self.checkpoint == 0:
            if self.prev_bal >= self.balance:
                self.bid_strategy = 0
            self.prev_bal = self.balance

        if self.bid_strategy == 0:
            bid_amount = self.avg_bid(user_id)

        elif self.bid_strategy == 1:
            bid_amount = self.beta_dist_bid(user_id)

        else:
            bid_amount = self.beta_ev_bid(user_id)


        return round(bid_amount,3)

    def notify(self, auction_winner, price, clicked):
        """used to send info about what happeend 1 round back
        to the Bidder. auction_winner is a bool to represent
        if the given bidder won the auction. price is the amount of
        the second bid, which the winner pays. If Bidder won the
        auction, clicked will contain a bool to
        represent whether the user clicked on the ad, if the given
        Bidder did not win the auction
        clicked will always contain None."""
        
        #updating user click history and balance
        if auction_winner is True:
            self.balance -= price +clicked
            
            if self.user_id in self.user_click_history:
                self.user_click_history[self.user_id].append(clicked)
            
            else:
                self.user_click_history[self.user_id] = [clicked]

        #updating price history, capping price at 1 
        if self.user_id in self.price_history:
            self.price_history[self.user_id].append(min(price,1))
        
        else:
            self.price_history[self.user_id] = [min(1,price)]

