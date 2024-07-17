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

def toggle_choosing_start():
    global choose_start, choose_end
    choose_end = False
    choose_start = not choose_start
    btn_start.config(state="disabled")
    btn_end.config(state="active")

def toggle_choosing_end():
    global choose_start, choose_end
    choose_start = False
    choose_end = not choose_end
    btn_end.config(state="disabled")
    btn_start.config(state="active")

def clicked(event):
    global choose_start, choose_end
    if choose_start == False and choose_end == False:
        return
    
    clicked_item = get_location(int(int((event.widget.find_closest(event.x, event.y)[0])-1)/2))
    if choose_start:
        for a in range(1,25,2):
            if marked_locations[get_location(int((a-1)/2))] == 1:
                marked_locations[get_location(int((a-1)/2))] = 0
                c.itemconfig(a,fill="#4C566A")
        marked_locations[clicked_item] = 1
        c.itemconfig(event.widget.find_closest(event.x, event.y), fill="#A3BE8C")
        btn_start.config(state="active")
        choose_start = False

    if choose_end:
        for a in range(1,25,2):
            if marked_locations[get_location(int((a-1)/2))] == 2:
                marked_locations[get_location(int((a-1)/2))] = 0
                c.itemconfig(a,fill="#4C566A")
        marked_locations[clicked_item] = 2
        c.itemconfig(event.widget.find_closest(event.x, event.y), fill="#EBCB8B")
        btn_end.config(state="active")
        choose_end = False

root = Tk()
root.geometry('420x450')
c = Canvas(root, width=420, height=350)
root.configure(bg='#2E3440')
c.configure(bg='#2E3440')
btn_start = Button(root, text='Choose Start', width=8,
             height=1, bd='3', command=toggle_choosing_start)
btn_end = Button(root, text='Choose End', width=8,
             height=1, bd='3', command=toggle_choosing_end)

 
btn_start.place(x=150, y=343)
btn_end.place(x=150, y=373)

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
    text = get_location(a)
    playbutton = c.create_rectangle(100*x+10, 100*y+10, 100*x+110, 100*y+110, fill="#4C566A",tags="playbutton")
    playtext = c.create_text(100*x+60, 100*y+55, text=text, font=("Comic Sans MS", 18), fill="#ECEFF4",tags="playbutton-text")
    c.tag_bind("playbutton", "<Button-1>", clicked)

def XD(event):
    print("XD")

for a in range(1,3):
    for b in range(4):
        wallbutton = c.create_rectangle(100*b+10, 100*a, 100*b+110, 100*a+10, fill="green",tags="wallbutton")
        c.tag_bind("wallbutton", "<Button-1>", XD)

for a in range(1,4):
    for b in range(3):
        wallbutton = c.create_rectangle(100*a+5, 100*b+10, 100*a+15, 100*b+110, fill="green",tags="wallbutton")
        c.tag_bind("wallbutton", "<Button-1>", XD)

c.pack()

print(warehouse_map.astype(int))
# print(Q.astype(int))

def route():
    start = list(marked_locations.keys())[list(marked_locations.values()).index(1)]
    end = list(marked_locations.keys())[list(marked_locations.values()).index(2)]
    try:
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
    except:
        print("ERROR")

btn_route = Button(root, text='Draw route', width=8,
             height=1, bd='3', command=route)
btn_route.place(x=150, y=403)

root.mainloop()

