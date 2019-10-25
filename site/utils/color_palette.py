import colorsys

def generate_color_palette(N=5):
    HSV_tuples = [(x * 1.0 / N, 1, 1) for x in range(N)]
    rgb_out = []
    for rgb in HSV_tuples:
        rgb = map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*rgb))
        rgb_out.append(", ".join(map(str,tuple(rgb))))
    return rgb_out

generate_color_palette(10)