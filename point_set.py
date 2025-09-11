import random
from typing import Optional, Tuple, List, Any

import numpy as np

from data import Data
from game import Game
from point_set_verifier import PointSetVerifier


class PointSet(Game):
    def __init__(self):
        super().__init__("PointSet", PointSetVerifier)

    def generate(self, num_of_questions: int = 100, difficulty: Optional[int] = 1):
        if not 1 <= difficulty <= 10:
            raise ValueError('Значение сложности от 1 до 10')

        game_data_list = []

        for i in range(num_of_questions):
            grid = self._generate_point_set(difficulty)

            grid_text = self._grid_to_text(grid)
            point, point_type = self._select_random_point(grid)

            question = f"Classify the given set of points in 3D space:\n\n{grid_text}\n\n"
            question += f"Is the point {point} internal, boundary, or external?"

            game_data = Data(
                question=question,
                answer=point_type,
                difficulty=difficulty,
                metadata={
                    "grid": grid.tolist(),
                    "grid_size": grid.shape[0]
                }
            )

            game_data_list.append(game_data)

        return game_data_list


    def _generate_point_set(self, difficulty: int) -> np.ndarray:
        grid_size = difficulty = 3 + difficulty

        x, y, z = [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)]

        grid = np.array([[['.' for _ in range(grid_size)] for _ in range(grid_size)] for _ in range(grid_size)])
        grid[x][y][z] = 'X'

        growth_iterations = random.randint(3, 5 + difficulty)

        for _ in range(growth_iterations):
            filled_points = np.argwhere(grid == 'X')

            if len(filled_points) == 0:
                continue

            current_point = random.choice(filled_points)
            cx, cy, cz = current_point

            directions = [
                (1, 0, 0), (-1, 0, 0),
                (0, 1, 0), (0, -1, 0),
                (0, 0, 1), (0, 0, -1),

                (1, 1, 0), (1, -1, 0), (-1, 1, 0), (-1, -1, 0),
                (1, 0, 1), (1, 0, -1), (-1, 0, 1), (-1, 0, -1),
                (0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1),

                (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1),
                (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1)
            ]
            random.shuffle(directions)

            for dx, dy, dz in directions:
                nx, ny, nz = cx + dx, cy + dy, cz + dz

                if 0 <= nx < grid_size and 0 <= ny < grid_size and 0 <= nz < grid_size:
                    if random.random() < 0.5:
                        grid[nx][ny][nz] = 'X'
        return grid

    def _grid_to_text(self, grid: np.ndarray) -> str:
        grid_size = grid.shape[0]
        result = []

        for z in range(grid_size):
            result.append(f"Flow z={z}:")
            layer_text = []

            f_X = False
            for y in range(grid_size):
                row = []
                for x in range(grid_size):
                    if grid[x, y, z] == 'X':
                        f_X = True

                    row.append(grid[x, y, z])

                layer_text.append(''.join(row))

            if f_X:
                result.append('\n'.join(layer_text))
            else:
                result.append('Empty')
            result.append('')

        return '\n'.join(result)

    def extract_answer(self, test_solution: str):
        return ''

    def _select_random_point(self, grid: np.ndarray) -> tuple[Any, str] | tuple[list[int], str]:
        grid_size = grid.shape[0]
        filled_points = np.argwhere(grid == 'X')
        empty_points = np.argwhere(grid == '.')

        num = random.random()
        

        if num <= 0.6:
            boundary_points = []
            for x, y, z in filled_points:
                for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if (0 <= nx < grid_size and 0 <= ny < grid_size and 0 <= nz < grid_size and
                            grid[nx, ny, nz] == '.'):
                        boundary_points.append([x, y, z])
                        break

            if boundary_points:
                point = random.choice(boundary_points)
                return point, "boundary"

        if 0.6 < num <= 0.8 and len(filled_points) > 0:
            internal_points = []
            for x, y, z in filled_points:
                is_internal = True
                for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if not (0 <= nx < grid_size and 0 <= ny < grid_size and 0 <= nz < grid_size) or \
                            grid[nx, ny, nz] == '.':
                        is_internal = False
                        break

                if is_internal:
                    internal_points.append([x, y, z])

            if internal_points:
                point = random.choice(internal_points)
                return point, "internal"

        point = random.choice(empty_points)
        return point, "external"

