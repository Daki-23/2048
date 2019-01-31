import Utils

class Tile:
    tile_pos_dict = {}
    def __init__(self, tile_value, position):
        self.tile_value = tile_value
        self.tile_image = Utils.image_dict[tile_value]
        # Positions are 1-indexed
        self.position = position
        self.has_merged = False
        Tile.tile_pos_dict[position] = self
        self.prev_x = 0
        self.prev_y = 0

    # Return the x, y coordinates of the tile
    def get_coordinates(self):
        x = (((self.position - 1) % Utils.tiles_per_row)) * (Utils.display_width)//Utils.tiles_per_row + Utils.tile_gap * (((self.position - 1) % Utils.tiles_per_row))
        y = ((self.position - 1)//Utils.tiles_per_col) * (Utils.display_height)//Utils.tiles_per_col + Utils.tile_gap * ((self.position - 1)//Utils.tiles_per_col)
        return (x, y)

    # Given the position, get the tile object
    def get_tile(self, position):
        return Tile.tile_pos_dict[position]

    # Returns 0-indexed row of current tile
    def get_current_row(self):
        return (self.position - 1) // Utils.tiles_per_row + 1

    # Returns 0-indexed column of current tile
    def get_current_col(self):
        return (self.position - 1) % Utils.tiles_per_row + 1


    # Returns nearest tile in the direction specified
    def get_nearest_tile(self, direction, tile_list):
        end_range = 0
        multiplier = 0
        if direction == "DOWN":
            multiplier = Utils.tiles_per_row
            end_range = Utils.num_rows - self.get_current_row() + 1
        if direction == "UP":
            multiplier = -Utils.tiles_per_row
            end_range = self.get_current_row()
        if direction == "LEFT":
            multiplier = -1
            end_range = self.get_current_col()
        if direction == "RIGHT":
            multiplier = 1
            end_range = Utils.num_cols - self.get_current_col() + 1

        nearest_tile = None
        for i in range(1, end_range):
            nearest_tile_pos = self.position + multiplier*i
            if nearest_tile_pos in Tile.tile_pos_dict:
                nearest_tile = Tile.tile_pos_dict[nearest_tile_pos]
                break
        return nearest_tile

    # Update the tile_pos_dict to reflect the tiles new position
    def change_position(self, new_position):
        Tile.tile_pos_dict.pop(self.position)
        self.position = new_position
        Tile.tile_pos_dict[self.position] = self

    # Moves tile to end in the provided direction and returns the new position
    def get_new_position(self, direction):
        update_val = 0

        if direction == "DOWN":
            update_val = (Utils.num_rows - self.get_current_row())*Utils.tiles_per_row
        elif direction == "UP":
            update_val = - (self.get_current_row() - 1) * Utils.tiles_per_row
        elif direction == "LEFT":
            update_val = - (self.get_current_col() - 1)
        elif direction == "RIGHT":
            update_val = (Utils.num_cols - self.get_current_col())

        return self.position + update_val

    #Determines whether action should be performed on current tile or not
    def is_move_valid(self, direction):
        if direction == "DOWN":
            return self.get_current_row() < Utils.num_rows
        elif direction == "UP":
            return self.get_current_row() > 1
        elif direction == "LEFT":
            return self.get_current_col() > 1
        elif direction == "RIGHT":
            return self.get_current_col() < Utils.num_cols

    # Move current tile adjacent to nearest tile
    # Called if nearest tile has different value than current tile
    # Or if the nearest tile has already been merged this turn
    def move_near_nearest_tile(self, nearest_tile, direction):
        position_changed = False
        if direction == "DOWN":
            if self.position != nearest_tile.position - Utils.tiles_per_row:
                        self.change_position(nearest_tile.position - Utils.tiles_per_row)
                        position_changed = True
        elif direction == "UP":
            if self.position != nearest_tile.position + Utils.tiles_per_row:
                self.change_position(nearest_tile.position + Utils.tiles_per_row)
                position_changed = True
        elif direction == "LEFT":
            if self.position != nearest_tile.position + 1:
                self.change_position(nearest_tile.position + 1)
                position_changed = True
        elif direction == "RIGHT":
            if self.position != nearest_tile.position - 1:
                self.change_position(nearest_tile.position - 1)
                position_changed = True

        return position_changed


    def update_position(self, action_taken, tile_list, remaining_tiles, score):

        position_changed = False
        if action_taken == "" or self.has_merged:
            return tile_list, remaining_tiles, score, position_changed
        if self.is_move_valid(action_taken):
            nearest_tile = self.get_nearest_tile(action_taken, tile_list)

            # If there is no tile in the current tiles way, move it to the end
            if nearest_tile is None:
                new_position = self.get_new_position(action_taken)
                if new_position != self.position:
                    self.change_position(new_position)
                    position_changed = True
            else:
                # If nearest tile has already been merged this turn, don't merge it again
                if not nearest_tile.has_merged:
                    # Merge Tiles only if they have the same value
                    if nearest_tile.tile_value == self.tile_value:

                        tile_list.remove(self)
                        Tile.tile_pos_dict.pop(self.position)
                        tile_list.remove(nearest_tile)
                        new_tile = Tile(self.tile_value*2, nearest_tile.position)
                        new_tile.has_merged = True
                        score += new_tile.tile_value
                        tile_list.append(new_tile)
                        remaining_tiles.append(new_tile)
                        position_changed = True
                    # Move adjacent to nearest tile
                    else:
                        position_changed = self.move_near_nearest_tile(nearest_tile, action_taken)
                else:
                    position_changed = self.move_near_nearest_tile(nearest_tile, action_taken)

        return tile_list, remaining_tiles, score, position_changed

