from __future__ import annotations

import pygame
from dataclasses import dataclass, field
from enum import Enum
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")


class Color(Enum):
    """Cyberpunk-inspired color palette."""
    BACKGROUND = (10, 10, 20)      # Dark navy
    GRID = (30, 40, 60)            # Deep blue
    OPEN = (0, 255, 200)           # Cyan
    CLOSED = (255, 0, 150)         # Hot pink
    BARRIER = (20, 20, 40)         # Nearly black
    START = (200, 0, 255)          # Bright purple
    END = (255, 140, 0)            # Bright orange
    PATH = (255, 200, 0)           # Neon yellow
    WHITE = (255, 255, 255)

    def __iter__(self):
        return iter(self.value)


@dataclass(unsafe_hash=True)
class Node:
    """Represents a grid node in the pathfinding algorithm."""
    row: int
    col: int
    width: int
    total_rows: int
    color: tuple[int, int, int] = field(default=None, hash=False, repr=False)
    neighbors: list[Node] = field(default=None, hash=False, repr=False)

    def __post_init__(self):
        if self.color is None:
            self.color = Color.WHITE.value
        if self.neighbors is None:
            self.neighbors = []
        self.x = self.row * self.width
        self.y = self.col * self.width

    def get_pos(self) -> tuple[int, int]:
        return self.row, self.col

    def is_closed(self) -> bool:
        return self.color == Color.CLOSED.value

    def is_open(self) -> bool:
        return self.color == Color.OPEN.value

    def is_barrier(self) -> bool:
        return self.color == Color.BARRIER.value

    def is_start(self) -> bool:
        return self.color == Color.START.value

    def is_end(self) -> bool:
        return self.color == Color.END.value

    def reset(self) -> None:
        self.color = Color.WHITE.value

    def make_closed(self) -> None:
        self.color = Color.CLOSED.value

    def make_open(self) -> None:
        self.color = Color.OPEN.value

    def make_barrier(self) -> None:
        self.color = Color.BARRIER.value

    def make_start(self) -> None:
        self.color = Color.START.value

    def make_end(self) -> None:
        self.color = Color.END.value

    def make_path(self) -> None:
        self.color = Color.PATH.value

    def draw(self, win: pygame.Surface) -> None:
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid: list[list[Node]]) -> None:
        """Update the list of valid neighboring nodes."""
        self.neighbors.clear()
        # Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other: Node) -> bool:
        return False


def heuristic(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """Manhattan distance heuristic."""
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from: dict[Node, Node], current: Node, draw: callable) -> int:
    """Reconstruct and draw the shortest path. Returns path length."""
    path_length = 1  # Count the end node
    while current in came_from:
        current = came_from[current]
        current.make_path()
        path_length += 1
        draw()
    return path_length


def algorithm(draw: callable, grid: list[list[Node]], start: Node, end: Node) -> tuple[bool, int]:
    """A* pathfinding algorithm implementation. Returns (found_path, path_length)."""
    path_length = 0
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from: dict[Node, Node] = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path_length = reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True, path_length

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()

    return False, path_length


def make_grid(rows: int, width: int) -> list[list[Node]]:
    """Create a grid of nodes."""
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win: pygame.Surface, rows: int, width: int) -> None:
    """Draw grid lines."""
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, Color.GRID.value, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, Color.GRID.value, (j * gap, 0), (j * gap, width))


def draw(win: pygame.Surface, grid: list[list[Node]], rows: int, width: int, font: pygame.font.Font = None, stats: str = "") -> None:
    """Render the grid and all nodes."""
    win.fill(Color.BACKGROUND.value)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos: tuple[int, int], rows: int, width: int) -> tuple[int, int]:
    """Convert mouse position to grid coordinates."""
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def main(win: pygame.Surface, width: int) -> None:
    """Main game loop."""
    pygame.init()
    font = pygame.font.Font(None, 36)  # Font for displaying stats
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    path_length = 0

    run = True

    while run:
        draw(win, grid, ROWS, width, font)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    found, path_length = algorithm(lambda: draw(win, grid, ROWS, width, font), grid, start, end)
                    if found:
                        pygame.display.set_caption(f"A* Path Finding Algorithm - Shortest path: {path_length} blocks")
                        draw(win, grid, ROWS, width, font)
                        pygame.time.wait(2000)  # Display result for 2 seconds
                    else:
                        pygame.display.set_caption(f"A* Path Finding Algorithm - No path found")

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    path_length = 0
                    pygame.display.set_caption("A* Path Finding Algorithm")


if __name__ == "__main__":
    pygame.init()
    main(WIN, WIDTH)
    pygame.quit()

    pygame.quit()


main(WIN, WIDTH)