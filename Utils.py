display_width = 400
display_height = 400
tile_gap = 10
tiles_per_row = 4
tiles_per_col = 4
num_rows = 4
num_cols = 4
total_tiles = tiles_per_row * tiles_per_col

bottom_left_tile_pos = total_tiles - tiles_per_row + 1
bottom_right_tile_pos = tiles_per_row * tiles_per_col
top_left_tile_pos = 1
top_right_tile_pos = tiles_per_row

white = (255, 255, 255)
black = (0, 0, 0)

action_list = ["UP", "DOWN", "LEFT", "RIGHT"]


image_dict = {}
#18 Because highest possible value in the game is 2^17
for i in range(1, 18):
    image_dict[2**i] = "Assets/Tile_" + str(2**i) + ".png"
