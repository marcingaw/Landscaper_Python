import random
import turtle

# 'map_size' must be a power of two because in each step of the Diamond Square
# algorithm the step size is divided by 2. The algorithm ends when the step is
# 2 (so in that step the remaining pixels between generated pixels are filled).
# Returns a list of 'map_size+1' lists with 'map_size+1' floats each.
# 'complexity' tells how many starting points should be randomized, 0 means
# corners only, 1 means 9 points, 2 means 25 etc.
def PrepareLandscape(map_size, complexity):

    # Calculate average elevation of corners of a square surrounding the given point
    # for the diamond step.
    def DiamondAvgRnd(lndscp, row, col, size, rnd_div):
        
        if lndscp[row][col] is not None:
            return lndscp[row][col]
        return ((lndscp[row - size][col - size] + lndscp[row - size][col + size] +
                 lndscp[row + size][col - size] + lndscp[row + size][col + size]) / 4.0 +
                (random.random() - 0.5) / rnd_div)

    # Calculate average elevation of corners of a diamond surrounding the given
    # point for the square step - this needs special handling for points along the
    # boundaries of the landscape.
    def SquareAvgRnd(lndscp, row, col, size, rnd_div):
        
        if lndscp[row][col] is not None:
            return lndscp[row][col]

        point_sum = 0.0
        point_cnt = 0.0

        if row >= size:
            point_sum = point_sum + lndscp[row - size][col]
            point_cnt = point_cnt + 1.0

        if row < len(lndscp) - size:
            point_sum = point_sum + lndscp[row + size][col]
            point_cnt = point_cnt + 1.0

        if col >= size:
            point_sum = point_sum + lndscp[row][col - size]
            point_cnt = point_cnt + 1.0

        if col < len(lndscp[row]) - size:
            point_sum = point_sum + lndscp[row][col + size]
            point_cnt = point_cnt + 1.0

        return point_sum / point_cnt + (random.random() - 0.5) / rnd_div

    # This will be initialized to be a 2D array indexed 0...MAP_SIZE.
    landscape = []

    for r in range(map_size + 1):
        landscape.append([])
        
        for c in range(map_size + 1):
            landscape[r].append(None)
            
    # Pick random values in the starting points.
    start_step = MAP_SIZE // (2 ** complexity)

    for r in range(0, map_size + 1, start_step):

        for c in range(0, map_size + 1, start_step):
            landscape[r][c] = random.random()

    min_pixel = landscape[0][0]
    max_pixel = landscape[0][0]

    # Now let's do the Diamond Square trick...
    step_size = map_size
    rnd_div = 2.0
    
    while step_size > 1:
        print(f'current step size: {step_size}')
        half_step = step_size // 2
        # Diamond.
        
        for r in range(0, map_size, step_size):
            
            for c in range(0, map_size, step_size):
                landscape[r + half_step][c + half_step] = DiamondAvgRnd(
                    landscape, r + half_step, c + half_step, half_step, rnd_div)
                min_pixel = min(min_pixel, landscape[r + half_step][c + half_step])
                max_pixel = max(max_pixel, landscape[r + half_step][c + half_step])


        # Square.
        for r in range(0, map_size + 1, step_size):
            
            for c in range(0, map_size + 1, step_size):
                
                if r < map_size:
                    landscape[r + half_step][c] = SquareAvgRnd(
                        landscape, r + half_step, c, half_step, rnd_div)
                    min_pixel = min(min_pixel, landscape[r + half_step][c])
                    max_pixel = max(max_pixel, landscape[r + half_step][c])
                    
                if c < map_size:
                    landscape[r][c + half_step] = SquareAvgRnd(
                        landscape, r, c + half_step, half_step, rnd_div)
                    min_pixel = min(min_pixel, landscape[r][c + half_step])
                    max_pixel = max(max_pixel, landscape[r][c + half_step])

        # Prepare the next step.
        step_size = half_step
        rnd_div = 2.0 * rnd_div

    delta = max_pixel - min_pixel

    if delta == 0.0:  # rather not realistic, unless the map size is 1
        delta = 1.0

    for r in range(map_size + 1):

        for c in range(map_size + 1):
            landscape[r][c] = (landscape[r][c] - min_pixel) / delta

    return landscape

MAP_SIZE = 512
landscape = PrepareLandscape(MAP_SIZE, 1)

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

step = MAP_SIZE // 4

while step > 0:
    print(f'Drawing with {step} block size.')
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
