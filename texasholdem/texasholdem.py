# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "Result"
score = 0
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.card_list = []

    def __str__(self):
        # return a string representation of a hand
        ans = " "
        for i in range(len(self.card_list)):
            ans += (str(self.card_list[i]) + " ")
        return "Hand contains" + ans

    def add_card(self, card):
        # add a card object to a hand
        return self.card_list.append(card)
                
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hd_val = 0
        ace = False
        for i in self.card_list:
            j = Card.get_rank(i)            
            hd_val += VALUES[j]
            if Card.get_rank(i) == 'A':
                ace = True
        if ace and (hd_val + 10) <= 21:
            return (hd_val + 10)           
        else:
            return hd_val
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards                            
        y = 1
        for x in self.card_list:            
            i = Card.get_suit(x)
            j = Card.get_rank(x)            
            card = Card(i, j)            
            if y < (len(self.card_list) + 1):      
                card.draw(canvas, [pos[0] * 0.3 * y + 150, pos[1]])
            y += 1
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck_list = []
        for suits in SUITS:
            for ranks in RANKS:
                self.deck_list.append(Card(suits, ranks))            
        
    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()        
        random.shuffle(self.deck_list)        
        
    def deal_card(self):
        # deal a card object from the deck        
        return self.deck_list.pop()
        
    def __str__(self):
        # return a string representing the deck
        bns = " "
        for i in range(len(self.deck_list)):
            bns += (str(self.deck_list[i]) + " ")
        return "Deck contains" + bns

    
    
#define cards set
def rearrange(card_set):
    temp1 = list(card_set)
    temp_card = []
    for i in range(0,len((card_set))):
        for j in range(i,len((card_set))):
            if VALUES[temp1[i].get_rank()] < VALUES[temp1[j].get_rank()]:                
                temp_card = temp1[j]
                temp1[j] = temp1[i]
                temp1[i] = temp_card            
    return temp1 

def straight(card_set):
    value = 0
    i, j = 0, 0
    if len(card_set) < 5:
        return False, value 
    for y in range(len(card_set) - 1):  
        if VALUES[card_set[y].get_rank()] == 2:
            pass
    for x in range(len(card_set) - 1):                    
        if VALUES[card_set[x].get_rank()] - VALUES[card_set[x+1].get_rank()] == 1:
            i += 1		
        else: 
            i = 0
        if i == 4:
            value = VALUES[card_set[x].get_rank()] + 3
            print i, x
            return True, value        
    return False 	


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hd, dealer_hd, flop_hd
    deck = Deck()    
    deck.shuffle()             
    player_hd, dealer_hd, flop_hd = Hand(), Hand(), Hand()
    player_hd.add_card(deck.deal_card())    
    dealer_hd.add_card(deck.deal_card())       
    player_hd.add_card(deck.deal_card())    
    dealer_hd.add_card(deck.deal_card())
    in_play = True
    
    
    
    
def flop():
    global in_play, flop_hd
    if in_play and len(flop_hd.card_list) == 0:        
        flop_hd.add_card(deck.deal_card())   
        flop_hd.add_card(deck.deal_card())   
        flop_hd.add_card(deck.deal_card())   
    
       
def turn():
    global in_play, flop_hd
    if in_play and len(flop_hd.card_list) == 3 :        
        flop_hd.add_card(deck.deal_card())   
       
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score

def river():
    global in_play, flop_hd
    if in_play and len(flop_hd.card_list) == 4:        
        flop_hd.add_card(deck.deal_card())        
        player_cardset = (player_hd.card_list[0], player_hd.card_list[1], flop_hd.card_list[0], flop_hd.card_list[1], flop_hd.card_list[2], flop_hd.card_list[3], flop_hd.card_list[4])
        dealer_cardset = (dealer_hd.card_list[0], dealer_hd.card_list[1], flop_hd.card_list[0], flop_hd.card_list[1], flop_hd.card_list[2], flop_hd.card_list[3], flop_hd.card_list[4])
        print 'dealer card'
        for i in dealer_cardset:
            print i
        print 'player card'
        for i in player_cardset:
            print i        
        temp1 = rearrange(dealer_cardset) 
        print 'dealer card order'
        for i in temp1:
            print i
        temp2 = rearrange(player_cardset) 
        print 'player card order'
        for i in temp2:
            print i
        print 'dealer straight', straight(temp1)
        print 'player straight', straight(temp2)

    
# draw handler    
def draw(canvas):    
    # test to make sure that card.draw works, replace with your code below    
    global score, outcome, flop_hd    
    if not in_play:
        dealer_hd.draw(canvas, [300, 100])
        player_hd.draw(canvas, [300, 250])        
    else:
        dealer_hd.draw(canvas, [300, 100])
        player_hd.draw(canvas, [300, 250])
        flop_hd.draw(canvas, [300, 400])
        #canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_SIZE[0] / 2, 200 + CARD_SIZE[1] / 2], CARD_BACK_SIZE)
        
    canvas.draw_text("Texas Hold'em", [30, 50], 40, "White")   
    canvas.draw_text('Dealer', [100, 150], 25, "Black")   
    canvas.draw_text('Player', [100, 300], 25, "Black")  
    canvas.draw_text('Flop', [100, 450], 25, "Black")  
    #canvas.draw_text('Score:'+str(score), [400, 50], 30, "Black")
    #canvas.draw_text(outcome, [250, 150], 25, "Black")
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 1200, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Flop",  flop, 200)
frame.add_button("Turn", turn, 200)
frame.add_button("River", river, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric
