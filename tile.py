import Utils

class Tile:
    tile_pos_dict = {}
    def __init__(self, tile_value, position):
        self.tile_value = tile_value
        self.tile_image = Utils.image_dict[tile_value]
        self.position = position
        self.has_merged = False
        self.tile_pos_dict[position] = self
        self.prev_x = 0
        self.prev_y = 0

    def get_coordinates(self):
        x = (((self.position - 1) % Utils.tiles_per_row)) * (Utils.display_width)//Utils.tiles_per_row + Utils.tile_gap * (((self.position - 1) % Utils.tiles_per_row))
        y = ((self.position - 1)//Utils.tiles_per_col) * (Utils.display_height)//Utils.tiles_per_col + Utils.tile_gap * ((self.position - 1)//Utils.tiles_per_col)
        return (x, y)

    def get_tile(self, position):
        return self.tile_pos_dict[position]

    def get_current_row(self):
        return (self.position - 1) // Utils.tiles_per_row + 1

    def get_current_col(self):
        return (self.position - 1) % Utils.tiles_per_row + 1

    def get_nearest_tile(self, direction, tile_list):
        if direction == "DOWN":
            #From one row below till the last row
            tile_below = None
            for i in range(1, Utils.num_rows - self.get_current_row() + 1):
                tile_below_pos = self.position + Utils.tiles_per_row*i
                if tile_below_pos in self.tile_pos_dict:
                    tile_below = self.tile_pos_dict[tile_below_pos]
                    break

            return tile_below
        if direction == "UP":
            tile_above = None
            for i in range(1, self.get_current_row()):
                tile_above_pos = self.position - Utils.tiles_per_row*i
                if tile_above_pos in self.tile_pos_dict:
                    tile_above = self.tile_pos_dict[tile_above_pos]
                    break
            return tile_above
        if direction == "LEFT":
            tile_left = None
            for i in range(1, self.get_current_col()):
                tile_left_pos = self.position - i
                if tile_left_pos in self.tile_pos_dict:
                    tile_left = self.tile_pos_dict[tile_left_pos]
                    break
            return tile_left
        if direction == "RIGHT":
            tile_right = None
            for i in range(1, Utils.num_cols - self.get_current_col() + 1):
                tile_right_pos = self.position + i
                if tile_right_pos in self.tile_pos_dict:
                    tile_right = self.tile_pos_dict[tile_right_pos]
                    break
            return tile_right

    def change_position(self, new_position):
        self.tile_pos_dict.pop(self.position)
        self.position = new_position
        self.tile_pos_dict[self.position] = self

    #TODO: Handle collisions, update score
    def update_position(self, action_taken, tile_list, remaining_tiles, score):
        position_changed = False
        if action_taken == "" or self.has_merged:
            return tile_list, remaining_tiles, score, position_changed
        if action_taken == "DOWN":
            if self.get_current_row() < Utils.num_rows:
                tile_below = self.get_nearest_tile(action_taken, tile_list)

                if tile_below is None:
                    new_position = self.position + (Utils.num_rows - self.get_current_row())*Utils.tiles_per_row
                    if new_position != self.position:
                        self.change_position(new_position)
                        position_changed = True
                else:
                    # If the below tile hasn't already been merged this turn
                    if not tile_below.has_merged:
                        if tile_below.tile_value == self.tile_value:

                            tile_list.remove(self)
                            self.tile_pos_dict.pop(self.position)
                            tile_list.remove(tile_below)
                            new_tile = Tile(self.tile_value*2, tile_below.position)
                            new_tile.has_merged = True
                            score += new_tile.tile_value
                            tile_list.append(new_tile)
                            remaining_tiles.append(new_tile)
                            position_changed = True

                        else:
                            if self.position != tile_below.position - Utils.tiles_per_row:
                                self.change_position(tile_below.position - Utils.tiles_per_row)
                                position_changed = True
                    else:
                        if self.position != tile_below.position - Utils.tiles_per_row:
                            self.change_position(tile_below.position - Utils.tiles_per_row)
                            position_changed = True
        if action_taken == "UP":
            if self.get_current_row() > 1:
                tile_above = self.get_nearest_tile(action_taken, tile_list)

                if tile_above is None:
                    new_position = self.position - (self.get_current_row() - 1) * Utils.tiles_per_row
                    if new_position != self.position:
                        self.change_position(new_position)
                        position_changed = True
                else:
                    # If the below tile hasn't already been merged this turn
                    if not tile_above.has_merged or not self.has_merged:
                        if tile_above.tile_value == self.tile_value:

                            tile_list.remove(self)
                            self.tile_pos_dict.pop(self.position)
                            tile_list.remove(tile_above)
                            new_tile = Tile(self.tile_value * 2,
                                            tile_above.position)
                            new_tile.has_merged = True
                            score += new_tile.tile_value
                            tile_list.append(new_tile)
                            remaining_tiles.append(new_tile)
                            position_changed = True

                        else:
                            if self.position != tile_above.position + Utils.tiles_per_row:
                                self.change_position(tile_above.position + Utils.tiles_per_row)
                                position_changed = True
                    else:
                        if self.position != tile_above.position + Utils.tiles_per_row:
                            self.change_position(tile_above.position + Utils.tiles_per_row)
                            position_changed = True

        if action_taken == "LEFT":
            if self.get_current_col() > 1:
                tile_left = self.get_nearest_tile(action_taken, tile_list)

                if tile_left is None:
                    new_position = self.position - (self.get_current_col() - 1)
                    if new_position != self.position:
                        self.change_position(new_position)
                        position_changed = True
                else:
                    # If the below tile hasn't already been merged this turn
                    if not tile_left.has_merged:
                        if tile_left.tile_value == self.tile_value:

                            tile_list.remove(self)
                            self.tile_pos_dict.pop(self.position)
                            tile_list.remove(tile_left)
                            new_tile = Tile(self.tile_value * 2,
                                            tile_left.position)
                            new_tile.has_merged = True
                            score += new_tile.tile_value
                            tile_list.append(new_tile)
                            remaining_tiles.append(new_tile)
                            position_changed = True

                        else:
                            if self.position != tile_left.position + 1:
                                self.change_position(tile_left.position + 1)
                                position_changed = True
                    else:
                        if self.position != tile_left.position + 1:
                            self.change_position(tile_left.position + 1)
                            position_changed = True

        if action_taken == "RIGHT":
            if self.get_current_col() < Utils.num_cols:
                tile_right = self.get_nearest_tile(action_taken, tile_list)

                if tile_right is None:
                    new_position = self.position + (Utils.num_cols - self.get_current_col())
                    if new_position != self.position:
                        self.change_position(new_position)
                        position_changed = True
                else:
                    # If the below tile hasn't already been merged this turn
                    if not tile_right.has_merged:
                        if tile_right.tile_value == self.tile_value:

                            tile_list.remove(self)
                            self.tile_pos_dict.pop(self.position)
                            tile_list.remove(tile_right)
                            new_tile = Tile(self.tile_value * 2,
                                            tile_right.position)
                            new_tile.has_merged = True
                            score += new_tile.tile_value
                            tile_list.append(new_tile)
                            remaining_tiles.append(new_tile)
                            position_changed = True

                        else:
                            if self.position != tile_right.position - 1:
                                self.change_position(tile_right.position - 1)
                                position_changed = True
                    else:
                        if self.position != tile_right.position - 1:
                            self.change_position(tile_right.position - 1)
                            position_changed = True
        return tile_list, remaining_tiles, score, position_changed

