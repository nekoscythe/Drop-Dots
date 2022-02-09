add_library('minim')
import os
import math
import random

RESOLUTION      = 800
GRAVITY         = 0.1
ELASTICITY      = 0.98                             #1 for perfect elastic collision, between 0 and 1 for inelastic, >1 for extra bounce
BUFFER          = 1                                #since ball might not exactly be equal due to uncertainty in c

BALL_SIZE, DROPPER_SIZE, POINT_SIZE = 10, 10, 10
DROPPER_Y       = 40                               #default dropper y-value

MAX_BALLS       = 200
MAX_VELOCITY    = GRAVITY * math.sqrt(2*(RESOLUTION - DROPPER_Y)/GRAVITY)
NUM_SOUNDFILES  = 12                               #number of soundfiles per sound type
INTERVAL_LIST   = []
STEP            = MAX_VELOCITY / NUM_SOUNDFILES    #step determined to create intervals for sound playback

for n in range(NUM_SOUNDFILES):
    if len(INTERVAL_LIST)==0:
        INTERVAL_LIST.append(0)
    INTERVAL_LIST.append((n+1)*STEP)


path = os.getcwd()

#loading all necessary sounds
player      = Minim(this)


#buttons
play         = player.loadSample(path + "/sounds/buttons/play.mp3", 2048)
exit_button  = player.loadSample(path + "/sounds/buttons/exit.mp3", 2048)
instructions = player.loadSample(path + "/sounds/buttons/instructions.mp3", 2048)
erase        = player.loadSample(path + "/sounds/buttons/erase.mp3", 2048)
clear_button = player.loadSample(path + "/sounds/buttons/clear.mp3", 2048)
click        = player.loadSample(path + "/sounds/buttons/click.mp3", 2048)


#misc
dropper_close = player.loadSample(path + "/sounds/misc/dropper_close.mp3", 2048)
dropper_open  = player.loadSample(path + "/sounds/misc/dropper_open.mp3", 2048)
line_create   = player.loadSample(path + "/sounds/misc/line.mp3", 2048)
point_create  = player.loadSample(path + "/sounds/misc/point.mp3", 2048)
 

#instruments
xylophone  = []
guitar     = []
banjo      = []
percussion = []

for n in range(NUM_SOUNDFILES):
    xylophone.append(player.loadSample(path + "/sounds/instruments/xylophone/xylophone ("+str(n+1)+").mp3", 2048))
    guitar.append(player.loadSample(path + "/sounds/instruments/guitar/guitar ("+str(n+1)+").mp3", 2048))
    banjo.append(player.loadSample(path + "/sounds/instruments/banjo/banjo ("+str(n+1)+").mp3", 2048))
    percussion.append(player.loadSample(path + "/sounds/instruments/percussion/percussion ("+str(n+1)+").mp3", 2048))



class Dropper:
    def __init__(self, x, y, color, sound, state="OFF"):
        self.x      = x 
        self.y      = y 
        self.radius = DROPPER_SIZE
        self.color  = color
        self.state  = state
        self.sound  = sound
        self.moving = 0
    
    def move(self, newX, newY):
        if dist(self.x, self.y, newX, newY) <= self.radius or self.moving ==1:
            self.moving = 1
            self.old_x = self.x
            self.old_y = self.y
            self.x = newX
            self.y = newY
            d_list = [] + game.dropper_list

            del d_list[d_list.index(self)]

            for dropper in d_list:
                if dist(self.x,self.y, dropper.x,dropper.y) <= self.radius + dropper.radius: #to handle collisions with other points
                    dropper.x = dropper.x + (newX-self.old_x) 
                    dropper.y = dropper.y + (newY-self.old_y)

    

    def switch(self):
        if dist(self.x,self.y,mouseX,mouseY) <= self.radius:
            if self.state == 'ON':
                dropper_close.trigger()
                self.state = 'OFF'
            elif self.state =='OFF':
                dropper_open.trigger()
                self.state = 'ON'
            return True 
        else: 
            return False 
    
    def generate_balls(self, game):
        global ball_list
        if len(game.ball_list)<MAX_BALLS:        #limit to number of balls on screen

            game.ball_list.append(Ball(self.x, self.y, self.color, self.sound))

    def display(self):
        pushStyle()
        strokeWeight(4)
        if self.color == 'Red':
            if self.state == 'ON':
                stroke(245,86,86)
                noFill()
            elif self.state == 'OFF':
                noStroke()
                fill(245,86,86)
        if self.color == 'Green':
            if self.state =='ON':
                stroke(102,204,0)
                noFill()
            elif self.state == 'OFF':
                noStroke()
                fill(102,204,0)
        if self.color == 'Blue':
            if self.state == 'ON':
                stroke(102,178,255)
                noFill()
            elif self.state == 'OFF':
                noStroke()
                fill(102,178,255)
        if self.color == 'Yellow':
            if self.state =='ON':
                stroke(255,255,102)
                noFill()
                
            elif self.state =='OFF':
                noStroke()
                fill(255,255,102)

        circle(self.x, self.y, 2*self.radius + 5)
        popStyle()
            



class Ball:
    def __init__(self, x, y, color, sound = []): #set to empty list for menu balls

        self.x = x 
        self.y = y 

        self.radius = BALL_SIZE
        self.vx     = 0
        self.vy     = 0
        self.color  = color
        self.sound  = sound

        self.g      = GRAVITY
        self.collision = 0
    

    def play_sound(self, sound_type = 'regular'):
        if sound_type == 'regular':
            for n in range(NUM_SOUNDFILES+1):
                if n == 0:
                    pass
                else:
                    if INTERVAL_LIST[n-1]**2 < self.vx**2 + self.vy**2 <= INTERVAL_LIST[n]**2:
                        self.sound[n].trigger()
        if sound_type == 'percussion':
            for n in range(NUM_SOUNDFILES+1):
                if n == 0:
                    pass
                else:
                    if INTERVAL_LIST[n-1]**2 < self.vx**2 + self.vy**2 <= INTERVAL_LIST[n]**2:
                        percussion[n-1].trigger()





    def collide_line(self, line):
        global BUFFER

        # in case ball collides with endpoints
        self.collide_point(line.p1)
        self.collide_point(line.p2)


        #collision logic
        self.line_length    = (dist(line.p2.x, line.p2.y, line.p1.x, line.p1.y))

        if self.line_length == 0:
            del game.line_list[game.line_list.index(line)]
            
        else:
            line.dot_product = (((self.x-line.p1.x)*(line.p2.x-line.p1.x)) + ((self.y-line.p1.y)*(line.p2.y-line.p1.y)) ) / self.line_length**2 #calculating ball product
    
            self.closest_x = line.p1.x + (line.dot_product*(line.p2.x-line.p1.x)) #using normal projection to find the closest point on the line
            self.closest_y = line.p1.y + (line.dot_product*(line.p2.y-line.p1.y))
            
            # check if closest point is on the segment
            if dist(self.closest_x, self.closest_y, line.p1.x, line.p1.y) + dist(self.closest_x, self.closest_y, line.p2.x, line.p2.y)>= self.line_length - BUFFER:
                if dist(self.closest_x, self.closest_y, line.p1.x, line.p1.y) + dist(self.closest_x, self.closest_y, line.p2.x, line.p2.y)<= self.line_length + BUFFER:
                    
                    #finding distance using closest point on line
                    self.distance = dist(self.x+self.vx, self.y+self.vy, self.closest_x, self.closest_y) #distance after movement
    
                    try:
    
                        # in case ball intersects line, remove it
                        if self.distance <= 0.2*(self.radius): 
                            del game.ball_list[game.ball_list.index(self)]
                    
                        #if ball slows down and stops on an object, remove it
                        if self.distance <= 0.7*self.radius and self.vx**2 + self.vy**2 <= 0.1: 
                            del game.ball_list[game.ball_list.index(self)]
    
                        #proper collision response
                        elif self.distance <= self.radius and self.vx**2 + self.vy**2 > 0.1:

                            self.play_sound()
    
                            #reverse direction
                            self.vx = -self.vx
                            self.vy = -self.vy
                            self.speed = math.sqrt(self.vx**2 + self.vy**2)
                            self.v_angle = math.atan2(self.vy, self.vx) #angle of velocity
                
                            #angle between centres of ball and point
                            self.incident_angle = math.atan2(self.closest_y - self.y, self.closest_x -self.x)
                            
                            
                            self.r_angle = 2*self.incident_angle - self.v_angle;
                            
                            #setting new velocity
                            self.vx = ELASTICITY * self.speed * math.cos(self.r_angle)  #multiplying by friction constant for inelastic collision
                            self.vy = ELASTICITY * self.speed * math.sin(self.r_angle)
                            
                            self.collision = 1 #if currently colliding, dont check for collision again

    
                        elif self.distance >= self.radius: #reset collision status if ball has finished a collision
                            self.collision = 0
                
                    except ValueError: #incase already deleted 
                        pass
                     
        


    def collide_point(self, point):

        self.distance = dist(self.x, self.y, point.x, point.y)
        self.future_distance = dist(self.x + self.vx,self.y + self.vy, point.x, point.y) #distance after movement
        
        
        try:
            #in case ball intersects object, remove it
            if self.distance <= 0.95*(self.radius + point.radius): 
                del game.ball_list[game.ball_list.index(self)]
                
            #if ball slows down and stops on an object, remove it
            elif self.future_distance <= self.radius + point.radius and self.vx**2 + self.vy**2 <= 0.5:
                del game.ball_list[game.ball_list.index(self)]
                
        
            #proper collision response
            elif self.collision == 0 and self.future_distance <= self.radius + point.radius and self.vx**2 + self.vy**2 > 0.5:
                
                self.play_sound('percussion')
                
                #reverse direction
                self.vx = -self.vx
                self.vy = -self.vy
                self.speed = math.sqrt(self.vx**2 + self.vy**2)
                self.v_angle = math.atan2(self.vy, self.vx) #angle of velocity
    
                #angle between centres of ball and point
                self.incident_angle = math.atan2(point.y - self.y, point.x -self.x)
                
                
                self.r_angle = 2*self.incident_angle - self.v_angle;
                
                #setting new velocity
                self.vx = ELASTICITY * self.speed * math.cos(self.r_angle)  #multiplying by friction constant for inelastic collision
                self.vy = ELASTICITY * self.speed * math.sin(self.r_angle)
                
                self.collision = 1 #if currently colliding, dont check for collision again
                
                
            elif self.collision==1 and self.distance >= self.radius + point.radius: #reset collision status if ball has finished a collision
                self.collision = 0
                
        except ValueError: #incase already deleted, as checks for all points receives index error more than one point are close to it during deletion 
            pass
        
    
    def update(self):  
        for point in game.point_list:
            self.collide_point(point)
                    
        if self.y - self.radius < RESOLUTION and self.x - self.radius < RESOLUTION and self.x +self.radius > 0  : #if ball is on screen
            self.vy = self.vy + self.g #gravity
            self.y = self.y + self.vy
            self.x = self.x + self.vx
    
                
        else:   #if ball exits screen completely, remove instance from main ball list
            try:
                del game.ball_list[game.ball_list.index(self)]

            except ValueError: #ball was already removed
                pass


    def display(self):
        pushStyle()
        # noStroke()
        stroke(0)
        strokeWeight(2)
        
        self.update()
        
            
        if self.color == 'Red':
            fill(245,86,86)
        if self.color == 'Green':
            fill(102,204,0)
        if self.color == 'Blue':
            fill(102,178,255)
        if self.color == 'Yellow':
            fill(255,255,102)
        circle(self.x, self.y, 2*(self.radius),)
        popStyle()
        

       
        
class Point:

    def __init__(self,x,y,point_type = "point", radius = POINT_SIZE):
        self.x = x
        self.y = y
        self.radius = radius
        self.moving = 0
        self.type = point_type
    

    def display(self):
        pushStyle()
        stroke(0,0,0)
        fill(0,0,0)
        circle(self.x, self.y, 2*self.radius)
        popStyle()



    def move(self, newX, newY):
        if dist(self.x, self.y, newX, newY) <= self.radius or self.moving ==1:
            self.moving = 1
            self.old_x = self.x
            self.old_y = self.y
            self.x = newX
            self.y = newY
            if self.type == "point":
                p_list = [] + game.point_list

            else:
                p_list = [] + game.line_point_list

            del p_list[p_list.index(self)]
            for point in p_list:
                if dist(self.x,self.y, point.x,point.y) <= self.radius + point.radius: #to handle collisions with other points
                    point.x = point.x + (newX-self.old_x) 
                    point.y = point.y + (newY-self.old_y) 


            

class Line:


    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
        self.p1.radius, self.p2.radius = 5, 5


    def move(self, newX, newY):
        self.p1.move(newX, newY)
        self.p2.move(newX, newY)
    
    
    def display(self):
        pushStyle()
        strokeWeight(5)
        stroke(0,0,0)
        line(self.p1.x,self.p1.y,self.p2.x,self.p2.y)
        popStyle()




class Button:

    def __init__(self, tool="point", y=30*RESOLUTION/800, x = RESOLUTION*(0.925), w=50*RESOLUTION/800, h=50*RESOLUTION/800): #scale buttons with resolution
        self.tool = tool
        self.img = loadImage(path + "/menu_pics/"+ self.tool + ".png")
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.Clicked = 0


    def switch(self):
        if self.tool == "play" or self.tool == "instructions":
            if self.x - (0.5*self.w) < mouseX < self.x + 0.5*self.w and self.y - 200< mouseY < self.y - 200+ self.h:
                if self.Clicked == 0:
                    self.Clicked = 1
                elif self.Clicked == 1:
                    self.Clicked = 0
                return True
            else:
                return False
        else:        

            if self.x < mouseX < self.x + self.w and self.y < mouseY < self.y + self.h :
                if self.tool == "clear":
                    clear_button.trigger()
                else:
                    click.trigger()
                if self.Clicked == 0:
                    self.Clicked = 1
                elif self.Clicked == 1:
                    self.Clicked = 0
                return True
            else:
                return False

         
    def display(self):
        
        if self.tool == "play" or self.tool == "instructions":
            pushStyle()
            image(self.img, self.x - (0.5*self.w), self.y - 200, self.w, self.h)
            popStyle()

        elif self.tool == "exit":
            pushStyle()
            image(self.img, self.x, self.y, self.w, self.h)
            popStyle()
        else:
            pushStyle()
            stroke(40)
            if self.Clicked == 0:
                strokeWeight(3)
                rect(self.x+7.5, self.y-2.5, self.w-5, self.h-5, 20)
                image(self.img, self.x+5, self.y-5, self.w, self.h)
                
            elif self.Clicked ==1:
                strokeWeight(5)
                rect(self.x+10, self.y, self.w-10, self.h-10, 20)
                image(self.img, self.x+5, self.y-5, self.w, self.h)
            popStyle()




class Game:

    def __init__(self, width, height,state = "main_menu"):
        self.w                = width
        self.h                = height
        self.state            = state
        self.line_counter     = 0

        self.point_list       = []
        self.line_point_list  = []
        self.ball_list        = []
        self.line_list        = []
        self.dropper_list     = []
        self.menu_ball_list   = []

        self.point_select     = Button("point")
        self.line_select      = Button("line"        , 90 * RESOLUTION/800)
        self.eraser_select    = Button("eraser"      , 150 * RESOLUTION/800)
        self.clear_select     = Button("clear"       , 210 * RESOLUTION/800)
        self.exit_button      = Button("exit"        , 20, 20, 40,40 )
        self.play_button      = Button("play"        , RESOLUTION/2        , RESOLUTION/2, 190, 90)
        self.instructions     = Button("instructions", RESOLUTION/2 + 120  , RESOLUTION/2, 464, 90)
        self.instructions_img = loadImage(path + "/menu_pics/game_instructions.png")
        self.names            = loadImage(path + "/menu_pics/names.png")

        self.menu_ball()
        
        

        self.dropper_list.append(Dropper(0.5*(RESOLUTION)/4, DROPPER_Y,'Red'   ,xylophone, "ON"))
        self.dropper_list.append(Dropper(1.5*(RESOLUTION)/4, DROPPER_Y,'Blue'  ,xylophone))
        self.dropper_list.append(Dropper(2.5*(RESOLUTION)/4, DROPPER_Y,'Green' ,guitar))
        self.dropper_list.append(Dropper(3.5*(RESOLUTION)/4, DROPPER_Y,'Yellow',banjo))

    def menu_ball(self): #generate balls for menu screen animation
        
        for n in range(14):
            self.menu_ball_list.append(Ball(random.randint(100,700), random.randint(100,700), random.choice(["Yellow","Red","Blue", "Green"])))
            self.menu_ball_list[n].vx = random.uniform(-2,2)
            self.menu_ball_list[n].vy = random.uniform(-4,4)
            self.menu_ball_list[n].radius = random.randint(40,70)
            self.menu_ball_list[n].g  = 0 
        

    def menu_ball_movement(self): 
        for ball in self.menu_ball_list:
            ball.display()
            if ball.x + ball.radius + ball.vx >= RESOLUTION or ball.x - ball.radius +ball.vx <=0:
                ball.vx = -ball.vx
            if ball.y + ball.radius + ball.vy >= RESOLUTION or ball.y - ball.radius + ball.vy <=0:
                ball.vy = -ball.vy



    def create_point(self):
        point_create.trigger()
        self.point_list.append(Point(mouseX, mouseY))

        

    def create_line(self):
        
        self.line_point_list.append(Point(mouseX,mouseY, "line", 5 ))

        if len(self.line_point_list) % 2 == 0:
            self.line_list.append(Line(self.line_point_list[2*self.line_counter], self.line_point_list[2*self.line_counter + 1]))
            self.line_counter+=1
            line_create.trigger()


    def erase_point(self):
        for point in self.point_list:
            if dist(point.x, point.y, mouseX, mouseY) <= point.radius:
                erase.trigger()
                del self.point_list[self.point_list.index(point)]
                
        for point in self.line_point_list: #remove single line points
            if dist(point.x, point.y, mouseX, mouseY) <= point.radius:
                erase.trigger()
                del self.line_point_list[self.line_point_list.index(point)]
                
    def erase_line(self):
        global  BUFFER
        for line in self.line_list:
            self.line_length = dist(line.p1.x, line.p1.y, line.p2.x, line.p2.y)
            self.dist_p1     = dist(line.p1.x, line.p1.y, mouseX, mouseY)
            self.dist_p2     = dist(line.p2.x, line.p2.y, mouseX, mouseY)
            
            if self.line_length - BUFFER <= self.dist_p1 + self.dist_p2 <= self.line_length + BUFFER: #if clicked on line
                erase.trigger()
                del self.line_point_list[self.line_point_list.index(line.p1)]
                del self.line_point_list[self.line_point_list.index(line.p2)]
                del self.line_list[self.line_list.index(line)]
                self.line_counter-=1
            
            elif self.dist_p1 < line.p1.radius or self.dist_p2< line.p2.radius: #if clicked endpoints
                try:
                    erase.trigger()
                    del self.line_point_list[self.line_point_list.index(line.p1)]
                    del self.line_point_list[self.line_point_list.index(line.p2)]
                    del self.line_list[self.line_list.index(line)]
                    self.line_counter-=1
                except ValueError: #incase erase_point removes line endpoint
                    pass
                
                
    def clear(self):

        del game.dropper_list[:]
        game.dropper_list.append(Dropper(0.5*(RESOLUTION)/4, DROPPER_Y,'Red',xylophone, "ON"))
        game.dropper_list.append(Dropper(1.5*(RESOLUTION)/4, DROPPER_Y,'Blue',xylophone))
        game.dropper_list.append(Dropper(2.5*(RESOLUTION)/4, DROPPER_Y,'Green',guitar))
        game.dropper_list.append(Dropper(3.5*(RESOLUTION)/4, DROPPER_Y,'Yellow',banjo))
        
        del game.point_list[:]
        del game.line_list[:]
        del game.line_point_list[:]
        game.line_counter = 0
        

    def display(self):

        if self.state =="main_menu":

            self.menu_ball_movement()

            self.play_button.display()
            self.instructions.display()

            image(self.names, RESOLUTION - 360, RESOLUTION - 120, 360,98)

        if self.state =="instructions":
            image(self.instructions_img, 80, 30, 0.83*(RESOLUTION-40), RESOLUTION-40)
            self.exit_button.display()

        if self.state =="play":

            for dropper in self.dropper_list:
                dropper.display()
                if frameCount % 60 == 0 and dropper.state == 'ON':
                    dropper.generate_balls(game)

            for line in self.line_list:
                line.display()

            for point in self.point_list:
                point.display()
                
            for point in self.line_point_list:
                point.display()
                            
            for ball in self.ball_list:
                ball.display()
                
                for line in self.line_list:
                    ball.collide_line(line)

                for point in self.point_list:
                    ball.collide_point(point)


            pushStyle()
            textSize(20)
            fill(0)
            strokeWeight(5)
            if len(self.ball_list) < MAX_BALLS:
                text("Ball count = "+ str(len(self.ball_list)),40,RESOLUTION - 30)
            elif len(self.ball_list) == MAX_BALLS:
                text("Ball count = "+ str(MAX_BALLS)+" (max)",40,RESOLUTION - 30) #indicate max ball limit reached
            popStyle()
            
            self.exit_button.display()
            self.point_select.display()
            self.line_select.display()
            self.eraser_select.display()   
            self.clear_select.display()



game = Game(RESOLUTION, RESOLUTION)



def setup():
    size(game.w, game.h)
    frameRate(60)
    background(255)
    

def draw():
    background(255)
    
    game.display()

    
def mouseDragged():

    
    if game.point_select.Clicked == 1:
        for point in game.point_list:
            point.move(mouseX, mouseY)

    elif game.line_select.Clicked == 1:
        for line in game.line_list:
            line.move(mouseX, mouseY)
    elif game.eraser_select.Clicked == 1:
        game.erase_line()
        game.erase_point()
        
    else:
        for dropper in game.dropper_list:
            dropper.move(mouseX, mouseY)
          

def mouseReleased():
    #changes move state for every object to 0
    for line in game.line_list:
        line.p1.moving = 0
        line.p2.moving = 0
    
    for point in game.point_list:
        point.moving = 0

    for dropper in game.dropper_list:
        dropper.moving = 0


def mouseClicked():
    
    if mouseButton == LEFT:

        if game.state =="main_menu":
            
            game.play_button.switch()
            game.instructions.switch()

            if game.play_button.Clicked ==1 :
                play.trigger()
                game.clear()
                game.state = "play"
                game.play_button.Clicked = 0

            if game.instructions.Clicked == 1:
                instructions.trigger()
                game.state = "instructions"
                game.instructions.Clicked = 0

        elif game.state =="instructions":
            game.exit_button.switch()

            if game.exit_button.Clicked ==1 :
                exit_button.trigger()
                game.state = "main_menu"
                game.exit_button.Clicked = 0


        elif game.state == "play":
            game.point_select.switch()
            game.line_select.switch()
            game.eraser_select.switch()
            game.clear_select.switch()
            game.exit_button.switch()
    
            if game.exit_button.Clicked ==1 :
                game.line_select.Clicked   = 0
                game.point_select.Clicked  = 0
                game.clear_select.Clicked  = 0
                game.eraser_select.Clicked = 0
                exit_button.trigger()
                game.clear()
                game.state = "main_menu"
                game.exit_button.Clicked = 0
                


            if game.point_select.Clicked == 1 :
                game.line_select.Clicked   = 0
                game.eraser_select.Clicked = 0
                game.clear_select.Clicked  = 0
                
                if game.point_select.switch() == False and game.clear_select.switch() == False and game.line_select.switch() == False and game.eraser_select.switch() == False:
                    game.create_point()
                    
                else:
                    game.point_select.switch()
                    
            if game.line_select.Clicked == 1 :
                game.point_select.Clicked  = 0
                game.eraser_select.Clicked = 0
                game.clear_select.Clicked  = 0
                
                if game.point_select.switch() == False and game.clear_select.switch() == False and game.line_select.switch() == False and game.eraser_select.switch() == False:
                    game.create_line()
                    
                else:       
                    game.line_select.switch() 
            
            if game.eraser_select.Clicked == 1:
                game.line_select.Clicked  = 0
                game.point_select.Clicked = 0
                game.clear_select.Clicked = 0

                if game.point_select.switch() == False and game.clear_select.switch() == False and game.line_select.switch() == False and game.eraser_select.switch() == False:
                    game.erase_line()
                    game.erase_point()
                    
                else:
                    game.eraser_select.switch()


            if game.clear_select.Clicked == 1:
                game.line_select.Clicked   = 0
                game.point_select.Clicked  = 0
                game.eraser_select.Clicked = 0
                game.clear()
                game.clear_select.Clicked = 0
                
            
            if game.clear_select.Clicked == 0 and game.point_select.Clicked == 0 and game.line_select.Clicked == 0 and game.eraser_select.Clicked == 0 :
                for dropper in game.dropper_list:
                    dropper.switch()
