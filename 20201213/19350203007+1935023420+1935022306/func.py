def distance2p(start, end):
    x = end['x'] - start['x']
    y = end['y'] - start['y']
    # print((x**2 + y**2) ** 0.5)
    return (x**2 + y**2) ** 0.5


def move_to(graphic, offset_value):
    graphic.pan_start_point = {
        'x': graphic.start_point['x'] + offset_value['dx'],
        'y': graphic.start_point['y'] + offset_value['dy'],
    }
    graphic.pan_end_point = {
        'x': graphic.end_point['x'] + offset_value['dx'],
        'y': graphic.end_point['y'] + offset_value['dy'],
    }
