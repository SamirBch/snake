import pygame, pygame_gui
from math import floor
import random
from pygame_gui.elements import UIButton, UITextEntryLine, UILabel, UITextBox, UISelectionList
import sys
import json

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Map :
    def __init__(self, x_screen_size, y_screen_size,bloc_size, screen, color): #attribut de Map
        self.x_screen_size = x_screen_size
        self.y_screen_size = y_screen_size
        self.bloc_size = bloc_size       
        self.color = color
        self.screen = screen
        

    def design_map(self):
        for x in range(0, self.x_screen_size, self.bloc_size): #le 3 c'est le step
            for y in range(0, self.y_screen_size, self.bloc_size):
                pygame.draw.rect(self.screen, self.color,pygame.Rect(x,y, self.bloc_size-1, self.bloc_size-1))
    
    def add_item(self, item_x, item_y, color) :
        item_x,item_y = self.grid_positon(item_x,item_y)
        pygame.draw.rect(self.screen, color ,pygame.Rect(item_x,item_y, self.bloc_size-1, self.bloc_size-1))


    def grid_positon(self,grid_x, grid_y):
        grid_x = floor(grid_x/self.bloc_size) * self.bloc_size 
        grid_y = floor(grid_y/self.bloc_size) * self.bloc_size  
        return grid_x, grid_y

    def same_position_in_grid(self,snake_pos_x, snake_pos_y, food_pos_x, food_pos_y):
        snake_pos_x,snake_pos_y = self.grid_positon(snake_pos_x,snake_pos_y)
        food_pos_x,food_pos_y = self.grid_positon(food_pos_x,food_pos_y)
        return snake_pos_x == food_pos_x and snake_pos_y == food_pos_y    



class Snake :

    def __init__(self,pos_x,pos_y,direction, color, grid_x, grid_y, grid_max_pos_x,grid_max_pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = direction
        self.color = color
        self.grid_x, self.grid_y = grid_x, grid_y
        self.grid_max_pos_x, self.grid_max_pos_y = grid_max_pos_x, grid_max_pos_y
        self.length = 0
        self.body= []
    
    def snake_set_direction(self, direction):
        self.direction = direction
    
    def snake_move(self):
        if self.direction == RIGHT:
            self.pos_x += 1
        elif self.direction == DOWN:
            self.pos_y += 1
        elif self.direction == LEFT:
            self.pos_x -= 1
        elif self.direction == UP:
            self.pos_y -= 1
        self.replace_in_grid()
    
    def get_pos_x(self):
        return self.pos_x
    
    def get_pos_y(self):
        return self.pos_y
    
    def get_color(self):
        return self.color
    
    def replace_in_grid(self):               #les bordures 
        if self.pos_x == self.grid_max_pos_x :
            self.pos_x = 0
        elif self.pos_x < 0:
            self.pos_x = self.grid_max_pos_x - 1
        if self.pos_y == self.grid_max_pos_y :
            self.pos_y = 0
        elif self.pos_y < 0:
            self.pos_y = self.grid_max_pos_y - 1 
    
    def has_change_block(self, posx, posy):     
        if self.grid_x != posx or self.grid_y != posy:
            self.old_grid_x, self.old_grid_y = self.grid_x, self.grid_y
            self.grid_x = posx
            self.grid_y = posy
            return True
        return False
            

    def update_body(self, posx, posy):      #permet au corps de serpent de suivre
        if self.has_change_block(posx, posy) and self.length !=0:
            self.body.append((self.old_grid_x, self.old_grid_y))
            if len(self.body) > self.length:
                self.body = self.body[-self.length:]   

    def get_bigger(self):
        self.length += 1

    def is_snake_alive(self):
        for bloc in self.body:
            if self.grid_x == bloc[0] and self.grid_y == bloc[1]: #grid x = tête  
                return False
        return True    

                            


class Food :
    timer = 1000
    expired_color = (0,0,255)
    fresh_food_color = (0,255,0)
    color = fresh_food_color


    def __init__(self,pos_x,pos_y,) :
        self.pos_x = pos_x
        self.pos_y = pos_y

    def update(self):
        self.timer_update()
        if self.is_food_expired():
            self.food_get_expired()

    def timer_update(self):
        self.timer -= 1      

    def is_food_expired(self):
        return self.timer < 0

    def food_get_expired(self):
        self.color = self.expired_color

    def get_pos_x(self):
        return self.pos_x

    def get_pos_y(self):
        return self.pos_y 

    def get_color(self):
        return self.color


class Game :

    snake_color = (255,0,255)
    map_color = (0,0,0)
    direction = RIGHT
    end_game = False
    score = 0
    foods = []
    number_foods = 5

    def __init__(self,x_screen,y_screen,blocsize,screen):
        self.x_screen = x_screen
        self.y_screen = y_screen
        self.blocsize = blocsize
        self.screen = screen
        self.map = Map(self.x_screen, self.y_screen, self.blocsize, self.screen, self.map_color)
        self.snake = self.__creat_snake()
        self.generate_food() 

    def __creat_snake(self) :
        snake_x = random.randint(0,self.x_screen)     
        snake_y = random.randint(0,self.y_screen)
        grid_snake_x, grid_snake_y = self.map.grid_positon(snake_x,snake_y)
        snake = Snake(snake_x, snake_y, self.direction, self.snake_color, grid_snake_x, grid_snake_y, self.x_screen, self.y_screen)
        return snake

    def generate_food(self):
        for i in range(0,self.number_foods):
            x,y = self.generate_grid_pos()
            self.foods.append(Food(x,y))

    def generate_grid_pos(self):
        x = random.randint(0,self.x_screen)
        y = random.randint(0,self.y_screen)  
        return x,y

    def is_foods_availabe(self):
        return not len(self.foods) == 0   #detecte quand la liste food n'a plus rien
    
    def display_score(self):
        my_font = pygame.font.SysFont(None, 30)
        text_surface = my_font.render("score : " + str(self.get_score()), True, (255, 0, 0))
        self.screen.blit(text_surface, (10, 10))



    def play(self):
        self.clock = pygame.time.Clock()     
        while not pygame.event.peek(pygame.QUIT) and not self.end_game:
            self.clock.tick(500)              #rafraichir boucle car trop rapide

            for food in self.foods:
                food.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.direction = self.get_user_direction(event)  
                    
            self.snake.snake_set_direction(self.direction) 
            self.snake.snake_move()
            self.map.design_map()
            self.map.add_item(self.snake.get_pos_x(),self.snake.get_pos_y(),self.snake.get_color())

            if not self.is_foods_availabe():
                self.generate_food()

            for food in self.foods:
                self.map.add_item(food.get_pos_x(),food.get_pos_y(),food.get_color())
            
            for food in self.foods:
                if self.map.same_position_in_grid(self.snake.get_pos_x(),self.snake.get_pos_y(),food.get_pos_x(),food.get_pos_y()):
                    if not food.is_food_expired():
                        self.score += 1
                    self.foods.remove(food)
                    self.snake.get_bigger()
            
            posx, posy = self.map.grid_positon(self.snake.get_pos_x(), self.snake.get_pos_y())
            self.snake.update_body(posx, posy)

            for blocs in self.snake.body:
                self.map.add_item(blocs[0],blocs[1],self.snake.get_color()) 


            if not self.snake.is_snake_alive():
                self.end_game = True
                self.foods.clear()

            self.display_score()
            pygame.display.flip()


    def get_user_direction(self, event):
        if event.key == pygame.K_LEFT:
            direction = LEFT
        if event.key == pygame.K_UP:
            direction = UP
        if event.key == pygame.K_DOWN:
            direction = DOWN
        if event.key == pygame.K_RIGHT:
            direction = RIGHT
        return direction   

    def get_score(self):
        return  self.score            


class App:
    
    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((800, 600))
        self.__manager = pygame_gui.UIManager((800, 600))
        image = pygame.image.load("image1.png")
        image = pygame.transform.scale(image, (800, 600))
        self.__screen.blit(image, (0, 0))
        


        self.data = self.get_data()


        self.create_play_button()
        self.create_ok_button()
        self.create_input()
        self.create_score_label()
        self.create_records()
        self.create_level_button()
        self.create_choice_grid_size()


        self.records.set_text(self.dict_to_str(self.data))
        
        self.__ok_button.hide()
        self.input.hide()
        self.score_label.hide()
        self.records.hide()
        

    def create_play_button(self):
        self.__play_button = UIButton(
        relative_rect=pygame.Rect(350,400,100,50),
        text='PLAY',
        manager = self.__manager
        )

    def create_ok_button(self):
        self.__ok_button = UIButton(
        relative_rect=pygame.Rect(240,220,50,50),
        text='OK',
        manager = self.__manager,
        )    

    def create_input(self):
        self.input = UITextEntryLine(
	    relative_rect=pygame.Rect(130, 220, 100, 50),
	    manager=self.__manager
        )    


    def create_records(self):
        self.records = UITextBox(
        relative_rect=pygame.Rect(420, 170, 200, 220), 
        manager=self.__manager,
        html_text = ""
        )    

    def create_score_label(self):
        self.score_label = UILabel(
        relative_rect=pygame.Rect(120, 170, 115, 50),
	    text= '',
        manager=self.__manager 
        )      

    def create_level_button(self):
        self.level_button = UISelectionList(
        relative_rect=pygame.Rect(365,200,70,66),
        item_list= ["EASY","MEDIUM","HARD"],
        manager = self.__manager,
        )    

    def create_choice_grid_size(self):
        self.grid_size = UILabel(
	    relative_rect=pygame.Rect(340, 180, 130, 20),
	    text='Choose grid size:',
	    manager=self.__manager,
        )    
     
    def save_results(self):  
        try:
            file = open('data.json', 'w')
            file.write(json.dumps(self.data))
            file.close()
        except FileNotFoundError:
            print('Le fichier est introuvable')
        except IOError:
            print("Erreur d'ouverture")
    
    def get_data(self):
        data = ""
        try:
            file = open('data.json')
            data = file.read()
            data = json.loads(data)
            file.close()
        except FileNotFoundError:
            print('Le fichier est introuvable')
        except IOError:
            print("Erreur d'ouverture")
        finally:
            return data

    def dict_to_str(self,dict):
        i = 0
        data = ""
        for elem in dict["Player_names"]:
            data += elem + " " + str(dict["Scores"][i]) + "\n"
            i+=1
        return data

    def add_results(self,player_name, score):
        self.data["Player_names"].append(player_name)   
        self.data["Scores"].append(score)

    def set_grid_level(self):
        level = self.level_button.get_single_selection()
        if level == 'EASY':
            x_screen,y_screen,bloc_size = 800,600,40
        elif level == 'HARD':
            x_screen,y_screen,bloc_size = 800,600,15
        else :
            x_screen,y_screen,bloc_size = 800,600,30
        return x_screen,y_screen,bloc_size

    def process_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.__play_button:
                x_screen,y_screen,blocsize = self.set_grid_level()
                self.level_button.hide()
                self.grid_size.hide()
                pygame.draw.rect(self.__screen, (0, 0, 0), pygame.Rect(0, 0, 800, 600))
                game = Game(x_screen, y_screen, blocsize, self.__screen)
                game.play()
                self.__ok_button.enable() #désactiver
                self.score = game.get_score()
                
                
                
                pygame.draw.rect(self.__screen, (0, 0, 0), pygame.Rect(0, 0, 800, 600))
                image = pygame.image.load("image2.png")
                image = pygame.transform.scale(image, (800, 600))
                self.__screen.blit(image, (0, 0))

                self.__play_button.set_text('Replay')
                self.__play_button.set_position((90,475))
                self.score_label.set_text("Score : " + str(self.score))
                self.__ok_button.show()
                self.input.show()
                self.score_label.show()
                self.records.show()


            if event.ui_element == self.__ok_button: 
                player_name = self.input.get_text()
                self.add_results(player_name, self.score)
                self.save_results()
                self.records.set_text(self.dict_to_str(self.data))
                self.__ok_button.disable()
    

    def run(self):          
        clock = pygame.time.Clock()
        while True:
            time_delta = clock.tick(60)/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.process_events(event)
                self.__manager.process_events(event)
            self.__manager.update(time_delta)
            self.__manager.draw_ui(self.__screen)
            pygame.display.flip()



if __name__ == '__main__':
    App().run()
    
