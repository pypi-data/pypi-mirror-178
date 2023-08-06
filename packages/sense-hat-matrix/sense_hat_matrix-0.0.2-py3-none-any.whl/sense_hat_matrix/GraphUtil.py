

def temp_colour(current, min_colour, middle_colour, max_colour):
        colour = min_colour
        if current >= 6:
            colour = max_colour
        elif current >= 2:
            colour = middle_colour
        return colour


def rescale(minimum, maximum, m):
    if m <= minimum:
        return 1
    elif m >= maximum:
        return 8
    else:
        return ((m - minimum) / (maximum - minimum)) * ((8 - 1) + 1) # https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range

