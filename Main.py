import pygame
import Utils
import random
from AI import AI
from tile import Tile

class Application:

    def __init__(self, human_played = True):
        self.AI = AI()
        self.human_played = human_played
        self.display_width = Utils.display_width
        self.display_height = Utils.display_height
        self.tile_gap = Utils.tile_gap
        self.tiles_per_row = Utils.tiles_per_row
        self.tiles_per_col = Utils.tiles_per_col
        self.tile_list = []
        self.score = 0
        self.positions_taken = set()
        self.human_played = human_played


    def setup_game(self):
        pygame.init()
        self.game_display = pygame.display.set_mode((self.display_width + self.tile_gap * (self.tiles_per_row - 1), self.display_height + self.tile_gap * (self.tiles_per_col - 1)))
        pygame.display.set_caption("2048")
        self.clock = pygame.time.Clock()

        #Add three tiles initially
        for i in range(3):
            random_position = random.sample((set(range(1, Utils.total_tiles + 1)) - self.positions_taken), 1)[0]
            self.tile_list.append(Tile(2, random_position))
            self.positions_taken.add(random_position)

    # Display all the tiles from tile_list on the game display
    def add_tiles_on_board(self):
        self.game_display.fill(Utils.white)
        for tile in self.tile_list:
            self.game_display.blit(pygame.image.load(tile.tile_image), tile.get_coordinates())

    # Sort tiles in accordance with the direction the move is made
    # Tiles nearer the end of the direction should be considered first
    def sort_tile_list(self, tile_list, action_type):
        if action_type == "LEFT":
            tile_list.sort(key=lambda x: x.get_current_col())
        elif action_type == "RIGHT":
            tile_list.sort(key=lambda x: x.get_current_col(), reverse=True)
        elif action_type == "UP":
            tile_list.sort(key=lambda x: x.get_current_row())
        elif action_type == "DOWN":
            tile_list.sort(key=lambda x: x.get_current_row(), reverse=True)

    def start_game(self):
        self.setup_game()
        end_game = False

        action_taken = False

        self.game_display.fill(Utils.white)
        self.add_tiles_on_board()

        action_type = ""
        prev_action = set()
        while not end_game:

            if self.human_played:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end_game = True

                    # If Human, action_type determined by key input
                    if event.type == pygame.KEYDOWN:
                        if not action_taken:
                            print(event.key)
                            if event.key == pygame.K_LEFT:
                                action_type = "LEFT"
                            elif event.key == pygame.K_RIGHT:
                                action_type = "RIGHT"
                            elif event.key == pygame.K_UP:
                                action_type = "UP"
                            elif event.key == pygame.K_DOWN:
                                action_type = "DOWN"
                            action_taken = True
            else:
                pygame.time.delay(50)
                action_type = self.AI.get_action(prev_action)
                action_taken = True
                #Start of a new turn
            if action_taken:
                self.sort_tile_list(self.tile_list, action_type)
                #print(action_type)
                action_taken = False

                for tile in self.tile_list:
                     tile.has_merged = False

                # List of tiles we would need to perform the action on
                # Once action has been performed on tile, it would be removed from the list
                remaining_tiles = self.tile_list.copy()
                # Set of positions currently occupied by the tiles on the board
                self.positions_taken = set()
                # Keeps track of whether performing action caused any of the tiles to move or not
                position_changed = False

                for tile in remaining_tiles:
                    self.tile_list, remaining_tiles, self.score, changed = tile.update_position(action_type,
                                                                                                        self.tile_list,
                                                                                                        remaining_tiles,
                                                                                                        self.score)
                    if changed:
                        position_changed = True

                for tile in self.tile_list:
                    self.positions_taken.add(tile.position)

                # Randomly add new tile only when a tile position has been updated
                if position_changed:
                    # FOR AI: Keep track of all previous actions that have not resulted in any change in position
                    # So as to not repeat them again
                    prev_action = set()

                    possible_locations = set(range(1, Utils.total_tiles + 1)) - self.positions_taken
                    if len(possible_locations) == 0:
                        print("No more moves possible")
                        end_game = True
                        break
                    random_position = random.sample(possible_locations, 1)[0]
                    self.tile_list.append(Tile(2, random_position))
                    self.positions_taken.add(random_position)
                    self.add_tiles_on_board()
                else:
                    if not self.human_played:
                        #Return anything but the last action_type
                         prev_action.add(action_type)
                         continue

            pygame.display.update()
            self.clock.tick(30)

            if end_game:
                print(self.score)
                pygame.quit()
                quit()

random.seed(1024)
app = Application()
app.start_game()