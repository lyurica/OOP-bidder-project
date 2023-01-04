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
        return "Avg. Bidder #" + str(self.bid_num)

    def __str__(self):
        return "Bidder with avg strategy bidding behavior"

    def bid(self, user_id):
        """returns a non-negative amount of money, in dollars rounded to three decimal places to user_id"""
        #magic of decision making happens here
        #current implementation random bids
        self.user_id = user_id

        if self.user_id not in self.user_click_history:
            bid_amount = 1*((self.num_rounds-self.current_round)/self.num_rounds)
        
        elif len(self.user_click_history[self.user_id]) < 10:
            bid_amount = np.average(self.user_click_history[self.user_id])*0.90
        
        else:
            bid_amount = np.average(self.user_click_history[self.user_id])-.01

        self.current_round +=1
        
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


