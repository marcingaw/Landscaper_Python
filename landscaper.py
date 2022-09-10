import terraingen
import turtle

MAP_SIZE_EXP = 9
landscape = terraingen.PrepareLandscape(MAP_SIZE_EXP, 1)
MAP_SIZE = 2 ** MAP_SIZE_EXP

# for r in range(MAP_SIZE + 1):
#     for c in range(MAP_SIZE + 1):
#         print(f'{landscape[r][c]:6.2f}', end = '')
#     print()

def ColorForPixel(p):
    
    if p < 0.1:
        return (0.0, 0.0, 0.5)
    if p < 0.2:
        return (0.3, 0.3, 0.7)
    if p < 0.3:
        return (0.6, 0.6, 0.9)
    if p < 0.4:
        return (0.0, 0.5, 0.0)
    if p < 0.5:
        return (0.0, 0.7, 0.0)
    if p < 0.6:
        return (0.0, 0.9, 0.0)
    if p < 0.7:
        return (0.5, 0.8, 0.0)
    if p < 0.8:
        return (0.7, 0.7, 0.0)
    if p < 0.9:
        return (0.7, 0.3, 0.0)
    
    return (0.5, 0.0, 0.0)

turtle.colormode(1.0)
turtle.speed(0)
turtle.hideturtle()

# Set to 1 to draw the map at the highest resolution. Otherwise it will
# gradually repaint it with higher and higher resolutions, but overall it will
# take much more time.
step = 1  # MAP_SIZE // 16

while step > 0:
    print(f'drawing block size: {step}')
    turtle.penup()
    turtle.backward(MAP_SIZE // 2)
    turtle.left(90)
    turtle.backward(MAP_SIZE // 2)
    turtle.right(90)
    turtle.pendown()
    
    for r in range(0, MAP_SIZE, step):
        
        for c in range(0, MAP_SIZE, step):
            turtle.color(ColorForPixel(landscape[r][c]))
            
            if step == 1:
                turtle.forward(1)
            else:
                turtle.begin_fill()
                turtle.forward(step)
                turtle.left(90)
                turtle.forward(step)
                turtle.left(90)
                turtle.forward(step)
                turtle.left(90)
                turtle.forward(step)
                turtle.left(90)
                turtle.end_fill()
                turtle.forward(step)
                
        turtle.penup()
        turtle.backward(MAP_SIZE)
        turtle.left(90)
        turtle.forward(step)
        turtle.right(90)
        turtle.pendown()
        
    turtle.penup()
    turtle.home()
    turtle.pendown()
    step = step // 2

turtle.done()
