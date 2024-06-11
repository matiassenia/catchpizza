from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font
from PIL import Image, ImageTk 


canvas_width = 800
canvas_height = 400

root = Tk()
root.title("Pizza Catcher")
c = Canvas(root, width=canvas_width, height=canvas_height)
c.pack()

# Cargar la imagen de fondo
bg_image = Image.open("img/bg-pizzeria.jpeg")
bg_image = bg_image.resize((canvas_width, canvas_height))
bg_photo = ImageTk.PhotoImage(bg_image)
c.create_image(0, 0, image=bg_photo, anchor='nw')

#Tamaño de las pizzas
pizza_width = 85
pizza_height = 65

#cargar imagen de las pizzas
pizza_image = Image.open("img/pizza-img.png")
pizza_image = pizza_image.resize((pizza_width, pizza_height))
pizza_photo = ImageTk.PhotoImage(pizza_image)


#Tamaño de la cesta
catcher_width = 100
catcher_height= 100

#Cargar imagen de la cesta
catcher_image = Image.open("img/me-img.png")
catcher_image = catcher_image.resize((catcher_width, catcher_height))
catcher_photo = ImageTk.PhotoImage(catcher_image)

#Posición inicial de la cesta
catcher_startx = canvas_width / 2 - catcher_width / 2
catcher_starty = canvas_height - catcher_height -20

# Crear la imagen
catcher = c.create_image(catcher_startx, catcher_starty, image=catcher_photo, anchor='nw')

#Variables del juego
pizza_score = 10
pizza_speed = 500
pizza_interval = 4000
difficulty = 0.95

#Fuente para puntuación y vidas
game_font = ("Helvetica", 25, "bold")
score_color = "Yellow"
lives_color = "yellow"

#Puntuación y vidas
score = 0
score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill=score_color, text="Score: "+ str(score))
lives_remaining = 3
lives_text = c.create_text(canvas_width-10, 10, anchor="ne", font=game_font, fill=score_color, text="Lives: "+ str(lives_remaining))

#Lista para las pizzas
pizzas = []

#Funcion para crear pizzas
def create_pizza():
    if c:     
        x = randrange(10, 740)
        y = 40
        new_pizza = c.create_image(x, y, image=pizza_photo, anchor="nw")
        pizzas.append(new_pizza)
        root.after(pizza_interval, create_pizza)

#Funcion para mover las pizzas
def move_pizzas():
    if c:
        for pizza in pizzas:
            try:
                (pizzax, pizzay) = c.coords(pizza)
            except:
                continue
            c.move(pizza, 0, 10)
            if pizzay > canvas_height:
                pizza_dropped(pizza)
            else:
                try:
                    (catcherx, catchery) = c.coords(catcher)
                    catcherx2 = catcherx + catcher_width
                    catchery2 = catchery + catcher_height    
                    if catcherx < pizzax < catcherx2 and catchery < pizzay < catchery2:
                        pizza_caught(pizza)  
                except:
                    continue
    root.after(pizza_speed, move_pizzas)        
        

#Funcion para manejar pizzas atrapadas
def pizza_caught(pizza):
    if pizza in pizzas:
        pizzas.remove(pizza)
        c.delete(pizza)
        increase_score(pizza_score)

#Funcion para manejar pizzas caídas
def pizza_dropped(pizza):
    if pizza in pizzas:
        pizzas.remove(pizza)
        c.delete(pizza)
        lose_a_life()
        if lives_remaining == 0:
            messagebox.showinfo("Game Over!", "Final Score: "+ str(score))
            root.destroy()

#Funcion para restar una vida
def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text="Lives: " + str(lives_remaining))

#Funcion para verificar si la cesta atrapó una pizza
def check_catch():
    try:
        (catcherx, catchery) = c.coords(catcher)
        catcherx2 = catcherx + catcher_width
        catchery2 = catchery + catcher_height
        for pizza in pizzas:
            try:
                (pizzax, pizzay,) = c.coords(pizza)
                pizzax2 = pizzax + pizza_width
                pizzay2 = pizzay + pizza_height
                if catcherx < pizzax < catcherx2 and catchery < pizzax2 < catchery2:
                    pizzas.remove(pizza)
                    c.delete(pizza)
                    increase_score(pizza_score)
            except:
                continue
    except:
        pass                
    root.after(100, check_catch)

#funcion para aumentar la puntuación
def increase_score(points):
    global score, pizza_speed, pizza_interval
    score += points
    pizza_speed = int(pizza_speed * difficulty)
    pizza_interval = int(pizza_interval * difficulty)
    c.itemconfigure(score_text, text="Score: "+ str(score))

# Funciones para mover la cesta a la izquierda y derecha
def move_left(event):
    if c:
        try:    
            (x1, y1) = c.coords(catcher)
        except:
            return    
        if x1 > 0:
                c.move(catcher, -20, 0)

def move_right(event):
    if c:
        try:
            (x1, y1) = c.coords(catcher)
        except:
            return    
        if x1 + catcher_width < canvas_width:
            c.move(catcher, 20, 0)

# Configuración de eventos y bucles del juego
c.bind("<Left>", move_left)
c.bind("<Right>", move_right)
c.focus_set()
root.after(1000, create_pizza)
root.after(1000, move_pizzas)
root.after(1000, check_catch)
root.mainloop()