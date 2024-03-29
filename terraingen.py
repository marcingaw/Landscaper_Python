import random

def PrepareLandscape(map_size_exp, complexity):
    '''Generates a landscape as a square array of floats 0.0...1.0.

    map_size_exp - the landscape will be of the size 2**map_size+1
    complexity - 0, 1 or 2 - there will be, resp., 4, 9 or 25 initial points on the map
    returns a square array representing the terrain, values are floats 0.0...1.0'''

    def DiamondAvgRnd(lndscp, row, col, size, rnd_div):
        '''Calculate average elevation of corners of a square surrounding the
        given point for the diamond step.'''
        
        if lndscp[row][col] is not None:
            return lndscp[row][col]
        
        return ((lndscp[row - size][col - size] + lndscp[row - size][col + size] +
                 lndscp[row + size][col - size] + lndscp[row + size][col + size]) / 4.0 +
                (random.random() - 0.5) / rnd_div)

    def SquareAvgRnd(lndscp, row, col, size, rnd_div):
        '''Calculate average elevation of corners of a diamond surrounding the
        given point for the square step - this needs special handling for points
        along the boundaries of the landscape.'''
        
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

    map_size = 2 ** map_size_exp
    
    # This will be initialized to be a 2D array indexed 0...map_size.
    landscape = []

    for r in range(map_size + 1):
        landscape.append([])
        
        for c in range(map_size + 1):
            landscape[r].append(None)
            
    # Pick random values in the starting points.
    start_step = map_size // (2 ** complexity)

    for r in range(0, map_size + 1, start_step):

        for c in range(0, map_size + 1, start_step):
            landscape[r][c] = random.random()

    min_pixel = landscape[0][0]
    max_pixel = landscape[0][0]

    # Now let's do the Diamond Square trick...
    step_size = map_size
    rnd_div = 2.0
    
    while step_size > 1:
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
