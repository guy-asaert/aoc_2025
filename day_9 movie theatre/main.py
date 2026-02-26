import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from dataclasses import dataclass
from itertools import combinations

from utils import read_lines

@dataclass
class RedTile:
    x: int
    y: int

    def __repr__(self):
        return f"({self.x}, {self.y})"

@dataclass
class Edge:
    From: RedTile
    To: RedTile

    def __repr__(self):
        return f"Edge({self.From}, {self.To})"

SAMPLE_INPUT = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


def solve_puzzle_part1():
    # Read the input

    red_tiles = []
    # for line in SAMPLE_INPUT.split('\n'):
    for line in read_lines(__file__):
        red_tiles.append(RedTile(*(int(i) for i in line.split(','))))
    
    largest_area = 0
    for tile1, tile2 in combinations(red_tiles, 2):
        largest_area = max(
            largest_area, 
            (abs(tile1.x - tile2.x) + 1) * (abs(tile1.y - tile2.y) + 1))
        pass
    print(f"The largest area is {largest_area}")
                

def _is_inside_polygon(x, y, vertex_set, v_edges, all_edges):
    """Check if point (x, y) is inside or on the polygon."""
    # Check if point is a vertex
    if (x, y) in vertex_set:
        return True

    # Check if point is on an edge
    for x1, y1, x2, y2 in all_edges:
        if y1 == y2 == y:
            if min(x1, x2) <= x <= max(x1, x2):
                return True
        if x1 == x2 == x:
            if min(y1, y2) <= y <= max(y1, y2):
                return True

    # Ray casting: count vertical edges to the right
    crossings = 0
    for ex, ey_min, ey_max in v_edges:
        if ex > x and ey_min <= y < ey_max:
            crossings += 1

    return crossings % 2 == 1


def solve_puzzle_part2():
    # Read the input
    red_tiles = []
    # for line in SAMPLE_INPUT.split('\n'):
    for line in read_lines(__file__):
        red_tiles.append(RedTile(*(int(i) for i in line.split(','))))

    n = len(red_tiles)
    vertex_set = {(t.x, t.y) for t in red_tiles}

    # Build polygon edges (consecutive vertices, wrapping around)
    h_edges = []  # horizontal: (y, x_min, x_max)
    v_edges = []  # vertical: (x, y_min, y_max)
    all_edges = []  # (x1, y1, x2, y2)
    for i in range(n):
        p1 = red_tiles[i]
        p2 = red_tiles[(i + 1) % n]
        all_edges.append((p1.x, p1.y, p2.x, p2.y))
        if p1.y == p2.y:
            h_edges.append((p1.y, min(p1.x, p2.x), max(p1.x, p2.x)))
        else:
            v_edges.append((p1.x, min(p1.y, p2.y), max(p1.y, p2.y)))

    largest_area = 0
    for tile1, tile2 in combinations(red_tiles, 2):
        if tile1.x == tile2.x or tile1.y == tile2.y:
            continue

        area = (abs(tile1.x - tile2.x) + 1) * (abs(tile1.y - tile2.y) + 1)
        if area <= largest_area:
            continue

        min_x = min(tile1.x, tile2.x)
        max_x = max(tile1.x, tile2.x)
        min_y = min(tile1.y, tile2.y)
        max_y = max(tile1.y, tile2.y)

        # Other two corners must be inside or on the polygon (green/red region)
        if not _is_inside_polygon(tile1.x, tile2.y, vertex_set, v_edges, all_edges) or \
           not _is_inside_polygon(tile2.x, tile1.y, vertex_set, v_edges, all_edges):
            continue

        # Check no polygon edge passes through the strict interior of the rectangle.
        # A vertical edge at x=X splits the rectangle if min_x < X < max_x
        # and its y-range overlaps [min_y, max_y].
        # A horizontal edge at y=Y splits the rectangle if min_y < Y < max_y
        # and its x-range overlaps [min_x, max_x].
        bad = False
        for ex, ey_min, ey_max in v_edges:
            if min_x < ex < max_x and ey_min < max_y and ey_max > min_y:
                bad = True
                break
        if not bad:
            for ey, ex_min, ex_max in h_edges:
                if min_y < ey < max_y and ex_min < max_x and ex_max > min_x:
                    bad = True
                    break
        if bad:
            continue

        largest_area = area

    print(f"The largest area is {largest_area}")
                
    # 4542134898 is too high
    # 3002421895 is wrong but not sure why

if __name__ == "__main__":
    solve_puzzle_part2()
