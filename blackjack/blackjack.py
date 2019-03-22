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
                card.draw(canvas, [pos[0] * y, pos[1]])
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

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hd, dealer_hd, player_hd2, dealer_hd2, hole, score    
    deck = Deck()    
    deck.shuffle()             
    player_hd, dealer_hd = Hand(), Hand()
    player_hd.add_card(deck.deal_card())    
    x = dealer_hd.add_card(deck.deal_card())
    #i = Card.get_suit(x)    
    #j = Card.get_rank(x)
    #hole = Card(i, j)        
    player_hd.add_card(deck.deal_card())    
    dealer_hd.add_card(deck.deal_card())
    player_hd.get_value()    
    if in_play:
        outcome = 'Fold, you lose:('
        score -= 1
    else:
        in_play = True
        outcome = 'In play'
    
def hit():
    global in_play, hd_val, player_hd, outcome, score
    if in_play:        
        player_hd.add_card(deck.deal_card())
        if player_hd.get_value() > 21:            
            in_play = False
            outcome = 'You went bust and lose:('                    
            score -= 1
    # if the hand is in play, hit the player   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global in_play, hd_val, player_hd, dealer_hd, score, outcome    
    if in_play and player_hd.get_value() <= 21:
        while dealer_hd.get_value() < 17:
            dealer_hd.add_card(deck.deal_card())
        if dealer_hd.get_value() > 21:
            outcome = 'Dealer went bust and you win:)'
            score += 1
        elif dealer_hd.get_value() >= player_hd.get_value():           	
            outcome = 'You lose:('
            score -= 1
        else:
            outcome = 'You win:)'
            score += 1
        in_play = False              
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score

def reset():
    global score
    score = 0
# draw handler    
def draw(canvas):    
    # test to make sure that card.draw works, replace with your code below    
    global score, outcome    
    if not in_play:
        dealer_hd.draw(canvas, [100, 200])
        player_hd.draw(canvas, [100, 400])
        canvas.draw_text('New deal?', [250, 350], 25, "Black")
    else:
        dealer_hd.draw(canvas, [100, 200])
        player_hd.draw(canvas, [100, 400])
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [100 + CARD_SIZE[0] / 2, 200 + CARD_SIZE[1] / 2], CARD_BACK_SIZE)
        canvas.draw_text('Hit or stand?', [250, 350], 25, "Black")

    canvas.draw_text('Blackjack', [30, 50], 40, "White")   
    canvas.draw_text('Dealer', [100, 150], 25, "Black")   
    canvas.draw_text('Player', [100, 350], 25, "Black")   
    canvas.draw_text('Score:'+str(score), [400, 50], 30, "Black")
    canvas.draw_text(outcome, [250, 150], 25, "Black")
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Reset score", reset, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric
