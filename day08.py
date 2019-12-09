import aoc
from collections import namedtuple
from typing import List, Tuple
from operator import itemgetter

Size = namedtuple('Size', ['width', 'height'])


def main():
    aoc.header("Space Image Format")
    aoc.run_tests()

    data = aoc.get_input().readline().strip()

    s = Size(width=25, height=6)
    (_, layers) = aoc.output(1, part1, args=[data, s], post=itemgetter(0))
    aoc.output(2, part2, args=[layers, s], post=lambda i: (i, s), output=lambda t: print_image4(t[0], t[1]))


def test():
    assert part1("123451789012", Size(width=3, height=2))[0] == 2
    assert part2(
        decode_to_layers("0222112222120000", Size(2,2)), 
        Size(2,2)
    ) == [0,1,1,0]

def part1(data : str, size : Size) -> Tuple[int, List[List[int]]]:
    layers = decode_to_layers(data, size)
    l = min(layers, key=lambda l: l.count(0))
    return (l.count(1) * l.count(2), layers)

def part2(layers : List[List[int]], size : Size) -> List[int]:
    coords = {
        (x,y) for x in range(size.width) for y in range(size.height)
    }

    image = [None for _ in range(size.width * size.height)]

    for l in layers:
        opaque_coords = set()
        for x,y in coords:
            px = l[x + y * size.width]
            if px < 2:
                image[x + y * size.width] = px
                opaque_coords.add((x,y))
        coords.difference_update(opaque_coords)

    return image

def decode_to_layers(data : str, size : Size) -> List[List[int]]:
    layer_length = size.width * size.height
    return [
        [
            int(data[i*layer_length + j])
            for j in range(layer_length)
        ]
        for i in range(len(data) // layer_length)
    ]
        
def print_image(img : List[int], size : Size):
    for y in range(size.height):
        print()
        for x in range(size.width):
            print("█" if img[x + y*size.width] == 1 else " ", end="")
    print()


blocks4 = {
    (0,0,0,0): " ",
    (0,0,1,1): "▄",
    (1,0,1,0): "▌",
    (0,1,0,1): "▐",
    (1,1,0,0): "▀",
    (0,0,1,0): "▖",
    (0,0,0,1): "▗",
    (1,0,0,0): "▘",
    (1,0,1,1): "▙",
    (1,0,0,1): "▚",
    (1,1,1,0): "▛",
    (1,1,0,1): "▜",
    (0,1,0,0): "▝",
    (0,1,1,0): "▞",
    (0,1,1,1): "▟",
    (1,1,1,1): "█"
}

def print_image4(img : List[int], size : Size):
    if size.height % 2 > 0:
        img.extend([0 * size.width])
        size = Size(size.width, size.height+1)
    if size.width % 2 > 0:
        newimg = []
        lines = [ img[i*size.width : (i+1)*size.width] for i in range(size.height) ]
        for line in lines:
            newimg.extend(line)
            newimg.append(0)
        img = newimg
        size = Size(size.width+1, size.height)

    def px(x : int, y : int):
        return img[x + y * size.width]

    for y in range(0, size.height, 2):
        print("\n   ", end="")
        for x in range(0, size.width, 2):
            code = (
                px(  x,   y),
                px(x+1,   y),
                px(  x, y+1),
                px(x+1, y+1)
            )
            print(blocks4[code], end="")
    print()

if __name__ == "__main__":
    main()
