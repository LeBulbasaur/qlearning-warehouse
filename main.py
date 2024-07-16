from tkinter import Tk, Canvas, Button
import numpy as np

gamma = 0.75
alpha = 0.9

choose_start = False
choose_end = False

location_to_state = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    'I': 8,
    'J': 9,
    'K': 10,
    'L': 11,
}

marked_locations = {
    'A': 0,
    'B': 0,
    'C': 0,
    'D': 0,
    'E': 0,
    'F': 0,
    'G': 0,
    'H': 0,
    'I': 0,
    'J': 0,
    'K': 0,
    'L': 0,
}

def get_location(index):
    return list(location_to_state.keys())[list(location_to_state.values())[index]]

# def toggle_choosing_start():
    # choose_end = False
    # if choose_start == False:
    #     choose_start = True
    # else:
    #     choose_start = False

# def toggle_choosing_end():
    # choose_start = False
    # if choose_end == False:
    #     choose_end = True
    # else:
    #     choose_end = False

root = Tk()
root.geometry('420x400')
c = Canvas(root, width=400, height=300)
root.configure(bg='#2E3440')
c.configure(bg='#2E3440')
# btn_start = Button(root, text='Start', width=8,
#              height=1, bd='5', command=toggle_choosing_start)
# btn_end = Button(root, text='End', width=8,
#              height=1, bd='5', command=toggle_choosing_end)
 
# btn_start.place(x=0, y=315)
# btn_end.place(x=0, y=345)

def clicked(event):
    if choose_start == False and choose_end == False:
        return
    clicked_item = get_location(int(int((event.widget.find_closest(event.x, event.y)[0])-1)/2))
    if marked_locations[clicked_item] == 0:
        marked_locations[clicked_item] = 1
        c.itemconfig(event.widget.find_closest(event.x, event.y), fill="#B48EAD")
    else:
        marked_locations[clicked_item] = 0
        c.itemconfig(event.widget.find_closest(event.x, event.y), fill="#4C566A")
    print(clicked_item)

actions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

R = np.array([
    [0,1,0,0,0,0,0,0,0,0,0,0],
    [1,0,1,0,0,1,0,0,0,0,0,0],
    [0,1,0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0,0,0],
    [0,1,0,0,0,0,0,0,0,1,0,0],
    [0,0,1,0,0,0,1000,1,0,0,0,0],
    [0,0,0,1,0,0,1,0,0,0,0,1],
    [0,0,0,0,1,0,0,0,0,1,0,0],
    [0,0,0,0,0,1,0,0,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,1,0,1],
    [0,0,0,0,0,0,0,1,0,0,1,0]
])

Q = np.array(np.zeros([12,12]))

for i in range(1000):
    current_state = np.random.randint(0,12)
    playable_actions = []
    for j in range(12):
        if R[current_state, j] > 0:
            playable_actions.append(j)
    next_state = np.random.choice(playable_actions)
    TD = R[current_state, next_state] + gamma*Q[next_state, np.argmax(Q[next_state,:])] - Q[current_state, next_state]
    Q[current_state, next_state] = Q[current_state, next_state] + alpha*TD

warehouse_map = np.zeros([3,4])

for a in range(12):
    y, x = divmod(a, 4)
    max_Q_value = np.max(Q[a, :])
    if max_Q_value > warehouse_map[y, x]:
        warehouse_map[y, x] = max_Q_value
    print(x,y)
    text = get_location(a)
    playbutton = c.create_rectangle(100*x, 100*y, 100*x+100, 100*y+100, fill="#4C566A",tags="playbutton")
    playtext = c.create_text(100*x+50, 100*y+50, text=text, font=("Comic Sans MS", 18), fill="#ECEFF4",tags="playbutton-text")
    c.tag_bind("playbutton","<Button-1>",clicked)

c.pack()

print(warehouse_map.astype(int))
# print(Q.astype(int))

def route(start, end):
    path = np.array([start])
    start_state = location_to_state[start]
    end_state = location_to_state[end]
    next_state = start_state
    while next_state != end_state:
        next_state = np.argmax(Q[start_state])
        location = get_location(next_state)
        start_state=next_state
        path = np.append(path, location)
    print(path)

route("J", "G")

root.mainloop()

