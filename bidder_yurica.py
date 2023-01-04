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


    def beta_EV_bid(self,user_id):
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
        """returns a non-negative amount of money, in dollars rounded to three decimal places to user_id"""
        #magic of decision making happens here
        
        self.user_id = user_id
        #low users, low rounds 
        #avg. Bidder
        if self.num_users <4 and self.num_rounds < 3000:
            bid_amount = self.avg_bid(user_id)


        #moderate users, low rounds
        #Beta exp. val

        #high users, low rounds
        #beta exp. value

        elif 4<= self.num_users and self.num_rounds < 3000:
            bid_amount = self.beta_EV_bid(user_id)


        #low users, mod rounds
        #b3 and b9 similar, b10 worst
        elif self.num_users<4 and 3000<self.num_rounds<7000:
            bid_amount = self.beta_dist_bid(user_id)

        #mod users, mod rounds
        #avg. Bidder
        
        #high users, mod rounds
        #avg. Bidder

        elif 4<= self.num_users and 3000<=self.num_rounds<5000:
            bid_amount = self.avg_bid(user_id)


        #low users, high rounds
        #beta distribution 
        elif self.num_users<4 and 7000<=self.num_rounds:
            bid_amount = self.beta_dist_bid(user_id)


        #mod users, high rounds
        #avg bidder

        #high users, high rounds
        #avg bidder
        else:
            bid_amount = self.avg_bid(user_id)

        

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
        
        #updating user click history
        if auction_winner is True:
            self.balance -= price +clicked
            
            if self.user_id in self.user_click_history:
                self.user_click_history[self.user_id].append(clicked)
            
            else:
                self.user_click_history[self.user_id] = [clicked]

        #updating price history regardless of winning
        if self.user_id in self.price_history:
            self.price_history[self.user_id].append(min(price,1))
        
        else:
            self.price_history[self.user_id] = [min(1,price)]

