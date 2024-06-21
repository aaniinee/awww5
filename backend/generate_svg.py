import random

def generate_tags():
    return sorted(random.sample(['tag1', 'tag2', 'tag3', 'tag4', 'tag5'], k=random.randint(1, 3)))

def generate_svg():
    rectangles = []
    swidth = random.randint(300, 800)
    sheight = random.randint(300, 800)

    n = random.randint(1, 5)
    for i in range(n):
        x = random.randint(0, swidth)
        y = random.randint(0, sheight)
        width = random.randint(0, swidth-x)
        height = random.randint(0, sheight-y)

        rect = {
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'color': f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})'
        }
        rectangles.append(rect)

    svg = {
        'width': swidth,
        'height': sheight,
        'rectangles': rectangles
    }

    return svg

