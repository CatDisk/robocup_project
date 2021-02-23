import pygame

class Field():
    def __init__(self, display):
        self.display = display
        self.width, self.height = self.display.get_size()
        self.sprite_dict = {
            "corner": pygame.image.load(  "./TeamViewer/assets/corner.png"),
            "border": pygame.image.load(  "./TeamViewer/assets/border.png"),
            "center": pygame.image.load(  "./TeamViewer/assets/center.png"),
            "goal_top": pygame.image.load("./TeamViewer/assets/goal_top_border.png"),
            "goal_mid": pygame.image.load("./TeamViewer/assets/goal_mid_border.png"),
            "goal_bot": pygame.image.load("./TeamViewer/assets/goal_bottom_border.png"),
        }
        self.goal_size_tiles = 4 #has to be even, smallest size 2
        self.field_tiles = []
        self.__build_field__()
        self.__add_goals__()

    
    def __build_field__ (self):
        tile = self.sprite_dict["corner"]
        for i in range(0, self.width, 64):
            for j in range(0, self.height, 64):
                angle = 0
                if (i == 0 and j == 0) or (i == 0 and j == (self.height - 64)) or ( j == 0 and i == (self.width - 64)) or (i == (self.width - 64) and j == (self.height - 64)):
                    tile = self.sprite_dict["corner"]
                    if i == 0:
                        if j == 0:
                            angle = 0
                        else:
                            angle = 90
                    else:
                        if j == 0:
                            angle = -90
                        else:
                            angle = 180
                elif (i == 0 and j < (self.height - 64)) or (i < (self.width - 64) and j == 0) or (i == (self.width - 64) and j < (self.height - 64)) or (i < (self.width - 64) and j == (self.height - 64)):
                    tile = self.sprite_dict["border"]
                    if i == 0:
                        angle = 90
                    elif i == (self.width - 64):
                        angle = -90
                    if j == 0:
                        angle = 0
                    elif j == (self.height - 64):
                        angle = 180

                else:
                    tile = self.sprite_dict["center"]

                self.field_tiles.append({
                    "tile": tile,
                    "coord": (i, j),
                    "angle": angle,
                })

    def __add_goals__(self):
        start_index = int(((self.height / 64) / 2) - (self.goal_size_tiles / 2))
        print(type(start_index))
        for n in range(start_index, start_index + self.goal_size_tiles):
            if n == start_index:
                self.field_tiles[n]["tile"] = self.sprite_dict["goal_top"]
                self.field_tiles[n]["angle"] = 0
                self.field_tiles[n + int(((self.width / 64) - 1) * (self.height / 64))]["tile"] = self.sprite_dict["goal_bot"]
                self.field_tiles[n + int(((self.width / 64) - 1) * (self.height / 64))]["angle"] = 180
            elif n == (start_index + self.goal_size_tiles) - 1:
                self.field_tiles[n]["tile"] = self.sprite_dict["goal_bot"]
                self.field_tiles[n]["angle"] = 0
                self.field_tiles[n + int(((self.width / 64) - 1) * (self.height / 64))]["tile"] = self.sprite_dict["goal_top"]
                self.field_tiles[n + int(((self.width / 64) - 1) * (self.height / 64))]["angle"] = 180
            else: 
                self.field_tiles[n]["tile"] = self.sprite_dict["goal_mid"]
                self.field_tiles[n]["angle"] = 0
                self.field_tiles[n + int(((self.width / 64) - 1) * (self.height / 64))]["tile"] = self.sprite_dict["goal_mid"]
                self.field_tiles[n + int(((self.width / 64) - 1) * (self.height / 64))]["angle"] = 180
                
    def update(self):
        for piece in self.field_tiles:
            self.display.blit(pygame.transform.rotate(piece["tile"], piece["angle"]), piece["coord"])