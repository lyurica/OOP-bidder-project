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
        return "Behavior Based model #" + str(self.bid_num)

    def __str__(self):
        return "Behavior Based model"

    def defensive(self,user_id):
        """Defensive bidding behavior, returns bid amount"""
        return 0

    def aggressive(self,user_id):
        """Aggressive bidding behavior, returns bid amount"""
        return 1


    def moderate(self,user_id):
        """Moderate bidding behavior, returns bid amount"""
        if user_id in self.user_click_history:
            return np.average(self.user_click_history[user_id])
        else:
            return 0.5

    def bid(self, user_id):
        """returns a non-negative amount of money, in dollars rounded to three decimal places to user_id"""
        #magic of decision making happens here
        #current implementation random bids
        self.user_id = user_id

        if self.user_id in self.user_click_history:
            if np.average(self.user_click_history[user_id]) > 0.5:
                bid_amount = self.aggressive(user_id)
            
            elif 0.2 < np.average(self.user_click_history[user_id]) <= 0.5:
                bid_amount = self.moderate(user_id)

            else:
                bid_amount = self.defensive(user_id) 

        else:
            bid_amount = self.aggressive(user_id)
        
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

