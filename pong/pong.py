# Implementation of classic arcade game Pong
import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400   
HALF_WIDTH = WIDTH / 2
HALF_HEIGHT = HEIGHT / 2
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
paddle1_pos, paddle2_pos = HALF_HEIGHT, HALF_HEIGHT
paddle1_vel, paddle2_vel = 0, 0
# Spawn ball UPwards or DOWNwards
DIR = [1, -1]
BALL_RADIUS = 12
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
resume_vel = ball_vel
con_vel = 3
ball_acc = 1.1
ng_flag = False
score1, score2 = 0, 0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, ng_flag # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    if direction == 'LEFT':  
        ball_vel[0] -= random.randrange(120,240)/60.0
        ball_vel[1] = -random.randrange(60,180)/60.0        
    elif direction == 'RIGHT':
        ball_vel[0] += random.randrange(120,240)/60.0
        ball_vel[1] = -random.randrange(60,180)/60.0
    ng_flag = False
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel  # these are numbers
    global score1, score2  # these are ints
    global ng_flag
    ng_flag = True
    score1, score2 = 0, 0
    paddle1_pos, paddle2_pos = HALF_HEIGHT, HALF_HEIGHT
    paddle1_vel, paddle2_vel = 0, 0
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0]
    spawn_ball(random.choice(['LEFT', 'RIGHT']))

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel, ball_acc
    global BALL_RADIUS 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1] 
    
    # Ball reflection and speed up
    if ball_pos[0] <= BALL_RADIUS:
        if ball_pos[1] >= paddle1_pos-HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos+HALF_PAD_HEIGHT:
            ball_vel = [x*ball_acc for x in ball_vel]
            ball_vel[0] = - (ball_vel[0])
        else:
            score2 += 1
            spawn_ball('RIGHT')
    elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        if ball_pos[1] >= paddle2_pos-HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos+HALF_PAD_HEIGHT:
            ball_vel = [x*ball_acc for x in ball_vel]
            ball_vel[0] = - (ball_vel[0])
            BALL_RADIUS = BALL_RADIUS+3
        else:
            score1 += 1
            spawn_ball('LEFT')        
    elif ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - (ball_vel[1])
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Blue", "White") 
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT    
    elif paddle1_pos < HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle2_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT    
    elif paddle2_pos < HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    else:
        paddle1_pos += paddle1_vel
        paddle2_pos += paddle2_vel
        
    # draw paddles
    canvas.draw_polygon([(0,paddle1_pos-HALF_PAD_HEIGHT),
                        (PAD_WIDTH,paddle1_pos-HALF_PAD_HEIGHT),
                        (PAD_WIDTH,paddle1_pos+HALF_PAD_HEIGHT),
                        (0,paddle1_pos+HALF_PAD_HEIGHT)], 2, 'Red', 'Red')
    canvas.draw_polygon([(WIDTH-PAD_WIDTH,paddle2_pos-HALF_PAD_HEIGHT),
                        (WIDTH,paddle2_pos-HALF_PAD_HEIGHT),
                        (WIDTH,paddle2_pos+HALF_PAD_HEIGHT),
                        (WIDTH-PAD_WIDTH,paddle2_pos+HALF_PAD_HEIGHT)], 2, 'Blue', 'Blue')
    
    # draw scores
    canvas.draw_text('player1', [WIDTH / 4 - 30, 20], 16, "White")
    canvas.draw_text(str(score1), [WIDTH / 4 - 10, 40], 16, "White")
    canvas.draw_text('player2', [3 * WIDTH / 4 - 30, 20], 16, "White")   
    canvas.draw_text(str(score2), [3* WIDTH / 4 - 10, 40], 16, "White")
    if BALL_RADIUS > 200:
        canvas.draw_text('UCCU', [0, HALF_HEIGHT], 180, "Yellow")   
def keydown(key):
    global paddle1_vel, paddle2_vel, paddle1_pos, paddle2_pos, con_vel
    if key == simplegui.KEY_MAP["down"] and paddle2_pos < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_vel = con_vel*2
    elif key == simplegui.KEY_MAP["up"] and paddle2_pos > HALF_PAD_HEIGHT:
        paddle2_vel = -con_vel*2
    elif key == simplegui.KEY_MAP["S"] and paddle1_pos < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_vel = con_vel*2
    elif key == simplegui.KEY_MAP["W"] and paddle1_pos > HALF_PAD_HEIGHT:
        paddle1_vel = -con_vel*2
    elif key == simplegui.KEY_MAP["left"]:
        spawn_ball('LEFT')
    elif key == simplegui.KEY_MAP["right"]:
        spawn_ball('RIGHT')
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel, paddle2_vel = 0, 0            
    
def pause():
    global ball_vel, resume_vel 
    if ng_flag == False:
        if ball_vel != [0, 0]:
            resume_vel = ball_vel
            ball_vel = [0, 0]
            pause_but.set_text('Resume')
        else:
            ball_vel = resume_vel
            pause_but.set_text('Pause')
            
def restart():
    spawn_ball(random.choice(['LEFT', 'RIGHT']))
    
def reset():
    new_game() 
    
def p_speed(text):
    global con_vel
    con_vel = int(text)
    
def b_speed(text):
    global ball_acc
    ball_acc = 0.1*int(text) + 1
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_label('Spawn the ball randomly by press Spawn:')
frame.add_label('Or press <-, -> to direct spawn')
frame.add_button('Spawn', restart, 200)
frame.add_label('Pause/Resume:')
pause_but = frame.add_button('Pause', pause, 200)
frame.add_label('Reset the score:')
frame.add_button('Reset', reset, 200)
frame.add_label('')
frame.add_input('Paddle speed 1-5, default=3', p_speed, 50)
frame.add_label('')
frame.add_input('Ball speed 1-5, default=1', b_speed, 50)

# start frame
new_game()
frame.start()

