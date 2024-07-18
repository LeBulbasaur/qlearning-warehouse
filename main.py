from tkinter import Tk, Canvas, Button, messagebox
import numpy as np

# Parametry algorytmu Q-learning
gamma = 0.75
alpha = 0.9

# Flagi wyboru punktów startu i końca
choose_start = False
choose_end = False

# Mapa lokalizacji na stany
location_to_state = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3,
    'E': 4, 'F': 5, 'G': 6, 'H': 7,
    'I': 8, 'J': 9, 'K': 10, 'L': 11,
}

# Oznaczenie lokalizacji
marked_locations = {key: 0 for key in location_to_state.keys()}

actions = list(range(12))

R = np.array([
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0]
])

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
    if not (choose_start or choose_end):
        return

    clicked_item = get_location((event.widget.find_closest(event.x, event.y)[0] - 1) // 2)

    if choose_start:
        for i in range(1, 25, 2):
            if marked_locations[get_location((i - 1) // 2)] == 1 or marked_locations[get_location((i - 1) // 2)] == 3:
                marked_locations[get_location((i - 1) // 2)] = 0
                c.itemconfig(i, fill="#4C566A")
        marked_locations[clicked_item] = 1
        c.itemconfig(event.widget.find_closest(event.x, event.y), fill="#88C0D0")
        btn_start.config(state="active")
        choose_start = False

    if choose_end:
        for i in range(1, 25, 2):
            if marked_locations[get_location((i - 1) // 2)] == 2:
                R[(i - 1) // 2][(i - 1) // 2] = 0
                marked_locations[get_location((i - 1) // 2)] = 0
                c.itemconfig(i, fill="#4C566A")
            elif marked_locations[get_location((i - 1) // 2)] == 3:
                marked_locations[get_location((i - 1) // 2)] = 0
                c.itemconfig(i, fill="#4C566A")
        marked_locations[clicked_item] = 2
        index = (event.widget.find_closest(event.x, event.y)[0] - 1) // 2
        R[index][index] = 1000
        c.itemconfig(event.widget.find_closest(event.x, event.y), fill="#5E81AC")
        btn_end.config(state="active")
        choose_end = False

root = Tk()
root.geometry('420x450')
root.configure(bg='#2E3440')

c = Canvas(root, width=420, height=350, bg='#2E3440')
c.pack()

btn_start = Button(root, text='Choose Start', width=8, height=1, bd='3', command=toggle_choosing_start)
btn_start.place(x=150, y=343)

btn_end = Button(root, text='Choose End', width=8, height=1, bd='3', command=toggle_choosing_end)
btn_end.place(x=150, y=373)

for a in range(12):
    y, x = divmod(a, 4)
    text = get_location(a)
    c.create_rectangle(100*x+10, 100*y+10, 100*x+110, 100*y+110, fill="#4C566A", tags="playbutton")
    c.create_text(100*x+60, 100*y+55, text=text, font=("Comic Sans MS", 18), fill="#ECEFF4", tags="playbutton-text")
    c.tag_bind("playbutton", "<Button-1>", clicked)

vertical_walls = np.zeros([1,9]).astype(int)[0]
horizontal_walls = np.zeros([1,8]).astype(int)[0]

def placeholder_function_vertical(event):
    val = event.widget.find_closest(event.x, event.y)[0]-32
    if val < 0:
        return

    for i in range(1, 25, 2):
        if marked_locations[get_location((i - 1) // 2)] == 3:
            marked_locations[get_location((i - 1) // 2)] = 0
            c.itemconfig(i, fill="#4C566A")

    if vertical_walls[val-1] == 0:
        vertical_walls[val-1] = 1
        c.itemconfig(event.widget.find_closest(event.x, event.y), fill="#BF616A")
        R[val-1][val] = 0
        R[val][val-1] = 0
    else:
        vertical_walls[val-1] = 0
        R[val-1][val] = 1
        R[val][val-1] = 1
        c.itemconfig(event.widget.find_closest(event.x, event.y), fill="#A3BE8C")

def placeholder_function_horizontal(event):
    val = event.widget.find_closest(event.x, event.y)[0]-24
    if val < 0:
        return
    
    for i in range(1, 25, 2):
        if marked_locations[get_location((i - 1) // 2)] == 3:
            marked_locations[get_location((i - 1) // 2)] = 0
            c.itemconfig(i, fill="#4C566A")

    if horizontal_walls[val-1] == 0:
        horizontal_walls[val-1] = 1
        R[val-1][val+3] = 0
        R[val+3][val-1] = 0
        c.itemconfig(event.widget.find_closest(event.x, event.y), fill="#BF616A")
    else:
        horizontal_walls[val-1] = 0
        R[val-1][val+3] = 0
        R[val+3][val-1] = 0
        c.itemconfig(event.widget.find_closest(event.x, event.y), fill="#A3BE8C")


# Tworzenie ścian
for a in range(1, 3):
    for b in range(4):
        c.create_rectangle(100*b+10, 100*a, 100*b+110, 100*a+10, fill="#A3BE8C", tags="wallbutton_horizontal")
        c.tag_bind("wallbutton_horizontal", "<Button-1>", placeholder_function_horizontal)

for a in range(3):
    for b in range(1, 5):
        if b == 4:
            c.create_rectangle(0, 0, 0, 0, tags="wallbutton_vertical")
        else:
            c.create_rectangle(100*b+5, 100*a+10, 100*b+15, 100*a+110, fill="#A3BE8C", tags="wallbutton_vertical")
            c.tag_bind("wallbutton_vertical", "<Button-1>", placeholder_function_vertical)

# Trening Q-learning
def route():
    Q = np.zeros([12, 12])

    for i in range(1000):
        current_state = np.random.randint(0, 12)
        playable_actions = [j for j in range(12) if R[current_state, j] > 0]
        next_state = np.random.choice(playable_actions)
        TD = R[current_state, next_state] + gamma * np.max(Q[next_state]) - Q[current_state, next_state]
        Q[current_state, next_state] += alpha * TD
    try:
        start = list(marked_locations.keys())[list(marked_locations.values()).index(1)]
        end = list(marked_locations.keys())[list(marked_locations.values()).index(2)]
        path = np.array([start])
        start_state = location_to_state[start]
        end_state = location_to_state[end]
        next_state = start_state
        while next_state != end_state:
            next_state = np.argmax(Q[start_state])
            location = get_location(next_state)
            start_state = next_state
            path = np.append(path, location)
        for location in path:
            if location != start and location != end:
                marked_locations[location] = 3
                c.itemconfig(location_to_state[location]*2+1, fill="#B48EAD")
    except ValueError:
        messagebox.showerror("showerror", "ERROR: Please choose both start and end locations.")

btn_route = Button(root, text='Draw route', width=8, height=1, bd='3', command=route)
btn_route.place(x=150, y=403)

root.mainloop()
