# implementation of card game - Memory
import simplegui
import random

HEIGHT = 100
state = 0
turn = 0
pos1 = 0
pos2 = 0
card_list = list(range(8) + range(8))
card_order = range(16)
exposed = []

# helper function to initialize globals
def new_game():
    global state, exposed, turn
    state = 0 
    turn = 0
    random.shuffle(card_list)
    exposed = [False for x in range(16)]
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, card_list, pos1, pos2, card1, card2, turn
    if state == 0:
        state = 1     
        pos1 = pos[0]//50        
        exposed[pos1] = True
        card1 = card_list[pos1]
    elif state == 1:                        
        if not exposed[pos[0]//50]:
            state = 2
            pos2 = pos[0]//50
            exposed[pos2] = True
            card2 = card_list[pos2]  
            turn += 1                
    else:
        state = 1
        if card1 != card2:
            exposed[pos1], exposed[pos2] = False, False	
        pos1 = pos[0]//50
        exposed[pos[0]//50] = True
        card1 = card_list[pos[0]//50]
                              
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global exposed, card_list
    #anvas.draw_text(str(state) + " card exposed", [30, 62], 24, "White")
    for card in range(16):  
        if exposed[card]:            
            canvas.draw_polygon([(card*50, 0), ((card+1)*50, 0), ((card+1)*50, HEIGHT), (card*50, HEIGHT)], 2, 'brown', 'black')
            canvas.draw_text(str(card_list[card]), [card*50 + 12, 60], 40, "White")
        else:           
            canvas.draw_polygon([(card*50, 0), ((card+1)*50, 0), ((card+1)*50, HEIGHT), (card*50, HEIGHT)], 2, 'brown', 'green')        
    label.set_text("Turn="+str(turn))
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric
