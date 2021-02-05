import pygame

class Field():
    def __init__(self, display):
        self.display = display
        self.width, self.height = self.display.get_size()
        self.sprite_dict = {
            "corner": pygame.image.load("./assets/corner.png"),
            "border": pygame.image.load("./assets/border.png"),
            "center": pygame.image.load("./assets/center.png")
        }

    def update(self):
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
                
                self.display.blit(pygame.transform.rotate(tile, angle), (i, j))