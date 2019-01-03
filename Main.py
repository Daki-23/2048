import pygame
import Utils
import random
import copy
from agent import Agent
from tile import Tile

class Application:

    def __init__(self, human_played = False):
        self.agent = Agent()
        self.human_played = human_played
        self.display_width = Utils.display_width
        self.display_height = Utils.display_height
        self.tile_gap = Utils.tile_gap
        self.tiles_per_row = Utils.tiles_per_row
        self.tiles_per_col = Utils.tiles_per_col
        self.tile_list = []
        self.tile_2_image = pygame.image.load("Assets/Tile_2.png")
        self.tile_4_image = pygame.image.load("Assets/Tile_4.png")
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


    def add_tiles(self):
        for tile in self.tile_list:
            self.game_display.blit(pygame.image.load(tile.tile_image), tile.get_coordinates())

    def sort_tile_list(self, action_type):
        if action_type == "LEFT":
            self.tile_list.sort(key=lambda x: x.get_current_col())
        elif action_type == "RIGHT":
            self.tile_list.sort(key=lambda x: x.get_current_col(), reverse=True)
        elif action_type == "UP":
            self.tile_list.sort(key=lambda x: x.get_current_row())
        elif action_type == "DOWN":
            self.tile_list.sort(key=lambda x: x.get_current_row(), reverse=True)

    #TODO: Fix function. Currently failing because it modifies tile_pos_dict in tile.py
    def is_move_possible(self):
        print("Checking Starts")
        position_changed = False

        for action in Utils.action_list:
            temp_tile_list = copy.deepcopy(self.tile_list)
            for tile in temp_tile_list:
                tile.has_merged = False

            remaining_tiles = temp_tile_list.copy()
            score = 0
            for tile in remaining_tiles:
                temp_tile_list, remaining_tiles, score, changed = tile.update_position(action,
                                                                                            temp_tile_list,
                                                                                            remaining_tiles,
                                                                                            score)
                if changed:
                    print("Checking Ends")
                    return True
        print("Checking Ends\n")
        return position_changed

    def start_game(self):
        self.setup_game()
        end_game = False

        action_taken = False

        self.game_display.fill(Utils.white)
        self.add_tiles()

        action_type = ""
        prev_action = set()
        while not end_game:

            #If move not possible: end

            for event in pygame.event.get():
                pygame.time.delay(50)
                if event.type == pygame.QUIT:
                    end_game = True

                # If Human, action_type determined by key input
                if self.human_played:
                    if event.type == pygame.KEYDOWN:
                        if not action_taken:
                            if event.key == pygame.K_LEFT:
                                action_type = "LEFT"
                            elif event.key == pygame.K_RIGHT:
                                action_type = "RIGHT"
                            elif event.key == pygame.K_UP:
                                action_type = "UP"
                            elif event.key == pygame.K_DOWN:
                                action_type = "DOWN"
                            action_taken = True
                # Else action type determined by agent
                else:
                    action_type = self.agent.get_action(prev_action)
                    action_taken = True
                #Start of a new turn
                if action_taken:
                    self.sort_tile_list(action_type)
                    print(action_type)
                    action_taken = False
                    for tile in self.tile_list:
                        tile.has_merged = False

                    remaining_tiles = self.tile_list.copy()
                    self.positions_taken = set()
                    position_changed = False
                    for tile in remaining_tiles:
                        self.tile_list, remaining_tiles, self.score, changed = tile.update_position(action_type,
                                                                                                        self.tile_list,
                                                                                                        remaining_tiles,
                                                                                                        self.score)
                        self.positions_taken.add(tile.position)
                        if changed:
                            position_changed = True

                    if position_changed:
                        # Randomly add new tile only when a tile position has been updated
                        prev_action = set()
                        random_position = random.sample((set(range(1, Utils.total_tiles + 1)) - self.positions_taken), 1)[0]
                        self.tile_list.append(Tile(2, random_position))
                        self.positions_taken.add(random_position)
                        #TODO: Check here if future moves are possible or not
                        # if not self.is_move_possible():
                        #     print("No more moves possible")
                        #     end_game = True
                        self.game_display.fill(Utils.white)
                        self.add_tiles()
                    else:
                        if not self.human_played:
                            #Return anything but the last action_type
                            prev_action.add(action_type)
                            continue

            pygame.display.update()
            self.clock.tick(60)

            if end_game:
                pygame.quit()
                quit()


app = Application()
app.start_game()