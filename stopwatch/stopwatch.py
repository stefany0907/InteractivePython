# template for "Stopwatch: The Game"
import simplegui
# define global variables
interval = 100
count = 0
success = 0
trial = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D    
def format(t):    
    global A, B, C, D
    D = t % 10
    B = int(((t-D)*0.1)%60)
    A = int(((t-D)*0.1)//60)
    if B < 10:
        return str(A)+":0"+str(B)+"."+str(D)
    else:  
        return str(A)+":"+str(B)+"."+str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():    
    timer.start()

def stop():
    global trial, success, D
    if timer.is_running():
        timer.stop()	
        trial += 1
        if (count % 10) == 0:
            success += 1
    else:
        timer.stop()        
def reset():
    timer.stop()        
    global count, trial, success
    count, trial, success = 0, 0, 0
    
# define event handler for timer with 0.1 sec interval
def tick():
    global count
    count += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(count), [120,120], 60, "White")
    canvas.draw_text(str(success)+"/"+str(trial), [300,40], 40, "Green") 
    
# create frame
frame = simplegui.create_frame("Timer", 400, 200)

# register event handlers
timer = simplegui.create_timer(interval, tick)
frame.set_draw_handler(draw)
frame.add_button("start", start, 100)
frame.add_button("stop", stop, 100)
frame.add_button("reset", reset, 100)
# start frame
frame.start()

# Please remember to review the grading rubric


