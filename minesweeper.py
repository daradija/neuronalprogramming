import pygame
import random
import sys

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Board dimensions
HEIGHT, WIDTH = 10, 10
NUM_MINES = 20
CELL_SIZE = 40
MARGIN = 5

# Pygame Configuration
pygame.init()
screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
pygame.display.set_caption('Minesweeper')
font = pygame.font.Font(None, 25)

class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.nearby_mines = 0

class Minesweeper:
	def __init__(self, height, width, num_mines):
		self.height = height
		self.width = width
		self.num_mines = num_mines
		self.board = [[Cell() for _ in range(width)] for _ in range(height)]
		self.place_mines()

	def place_mines(self):
		mines_placed = 0
		while mines_placed < self.num_mines:
			row = random.randint(0, self.height - 1)
			col = random.randint(0, self.width - 1)

			cell = self.board[row][col]
			if not cell.is_mine:
				cell.is_mine = True
				mines_placed += 1
				# Update nearby mines count for adjacent cells
				self.update_nearby_mines(row, col)

	def update_nearby_mines(self, row, col):
		# Increment the nearby_mines count for adjacent cells
		for i in range(-1, 2):
			for j in range(-1, 2):
				if (0 <= row + i < self.height) and (0 <= col + j < self.width):
					self.board[row + i][col + j].nearby_mines += 1

	def open_cell(self, row, col):
		cell = self.board[row][col]

		if cell.is_mine:
			print("Boom! You've discovered a mine.")
			return True  # Game ends

		if cell.is_revealed:
			return False  # Cell already revealed

		cell.is_revealed = True

		if cell.nearby_mines == 0:
			# Open adjacent cells recursively
			for i in range(-1, 2):
				for j in range(-1, 2):
					if 0 <= row + i < self.height and 0 <= col + j < self.width:
						# Avoid opening the cell itself again
						if i != 0 or j != 0:
							self.open_cell(row + i, col + j)
		return False

	def draw(self):
			for i in range(self.height):
				for j in range(self.width):
					cell = self.board[i][j]

					# Determine the color of the cell
					cell_color = BLACK if cell.is_revealed else GRAY
					pygame.draw.rect(screen, cell_color, [(MARGIN + CELL_SIZE) * j + MARGIN,
														(MARGIN + CELL_SIZE) * i + MARGIN,
														CELL_SIZE - MARGIN, CELL_SIZE - MARGIN])

					# Draw the number of nearby mines if the cell is revealed
					if cell.is_revealed and not cell.is_mine:
						if cell.nearby_mines > 0:
							text = font.render(str(cell.nearby_mines), True, WHITE)
							screen.blit(text, ((MARGIN + CELL_SIZE) * j + MARGIN + CELL_SIZE // 3,
											(MARGIN + CELL_SIZE) * i + MARGIN + CELL_SIZE // 3))

					# Draw a flag symbol if the cell is flagged
					if cell.is_flagged:
						flag_text = font.render('F', True, RED)
						screen.blit(flag_text, ((MARGIN + CELL_SIZE) * j + MARGIN + CELL_SIZE // 3,
												(MARGIN + CELL_SIZE) * i + MARGIN + CELL_SIZE // 3))

	def toggle_flag(self, row, col):
		cell = self.board[row][col]

		# Only toggle the flag if the cell is not revealed
		if not cell.is_revealed:
			cell.is_flagged = not cell.is_flagged


# Game loop
def game_loop():
	game_over = False
	minesweeper = Minesweeper(HEIGHT, WIDTH, NUM_MINES)
	font = pygame.font.Font(None, 36)

	while not game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = event.pos
				column_clicked = mouse_x // (CELL_SIZE + MARGIN)
				row_clicked = mouse_y // (CELL_SIZE + MARGIN)

				if 0 <= row_clicked < HEIGHT and 0 <= column_clicked < WIDTH:
					if event.button == 1:  # Left click
						game_over = minesweeper.open_cell(row_clicked, column_clicked)
					elif event.button == 3:  # Right click
						minesweeper.toggle_flag(row_clicked, column_clicked)

		screen.fill(BLACK)
		minesweeper.draw()
		pygame.display.flip()

if __name__ == "__main__":
    game_loop()
