import pygame, sys, random, math, csv
from pandas import *
from pygame.mouse import *
from pygame.locals import *
from pygame.sprite import Sprite
pygame.init() #Pygame initialisation 
clock = pygame.time.Clock() #For frame rate ticks
pygame.font.init() #For Fonts

black = [0, 0, 0] #Colours
grey = [128, 128, 128] 
white = [255, 255, 255]
blue = [50, 30, 200]
lightblue =[173, 216, 230]
red = [170, 20, 40]
purple = [155, 42, 135]
green = [34,139,34]

screen_width = 1280 #Window 
screen_height = 720 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Nova Bow') #Name of window

menuMusic = 'audio/AcidJazz.wav' #Music
gameMusic = 'audio/AquariumPark.wav'
puzzleMusic = 'audio/puzzle.wav'
selectSound = pygame.mixer.Sound('audio/select.wav') #Sound effects
backSound = pygame.mixer.Sound('audio/back.wav')
textboxSound = pygame.mixer.Sound('audio/textbox.wav')
submitSound = pygame.mixer.Sound('audio/submit.wav')
errorSound = pygame.mixer.Sound('audio/error.wav')
hitSound = pygame.mixer.Sound('audio/hit.wav')
shotSound = pygame.mixer.Sound('audio/shot.wav')
impactSound = pygame.mixer.Sound('audio/impact.wav')

titlefont = pygame.font.SysFont('arial', 60) #Fonts
menufont = pygame.font.SysFont('Corbel', 30) 
iconfont = pygame.font.SysFont('helvetica', 20)
inputfont = pygame.font.SysFont('arial', 40)

titletext = titlefont.render('Nova Bow', True, white) #Render fonts and text
newGameTitle = titlefont.render('New Game', True, white)
loadGameTitle = titlefont.render('Load Game', True, white)
leaderboardTitle = titlefont.render('Leaderboard', True, white)
optionsTitle = titlefont.render('Options', True, white)
puzzleTitle = titlefont.render('Puzzle', True, white)
menuText = iconfont.render('Main Menu', True, white)
quitText = iconfont.render('Quit', True, white) 

menuBG = pygame.image.load('images/mainMenu.png') #Images
menuImg = pygame.image.load('images/logo.png')
backButtonImg = pygame.image.load('images/backButton.png')
area1Img = pygame.image.load('images/area1.png')
area2Img = pygame.image.load('images/area2.png')
area3Img = pygame.image.load('images/area3.png')
area4Img = pygame.image.load('images/area4.png')
area5Img = pygame.image.load('images/area5.png')
area6Img = pygame.image.load('images/area6.png')
area7Img = pygame.image.load('images/area7.png')
area8Img = pygame.image.load('images/area8.png')
area9Img = pygame.image.load('images/area9.png')
puzzleBoxImg = pygame.image.load('images/puzzleBox.png')
player1L = pygame.image.load('images/player1L.png')
player1U = pygame.image.load('images/player1U.png')
player1R = pygame.image.load('images/player1R.png')
player1D = pygame.image.load('images/player1D.png')
player1LBow = pygame.image.load('images/player1LBow.png')
player1RBow = pygame.image.load('images/player1RBow.png')
arrowL = pygame.image.load('images/arrowL.png')
arrowR = pygame.image.load('images/arrowR.png')
enemy1L = pygame.image.load('images/enemy1L.png')
enemy1R = pygame.image.load('images/enemy1R.png')
enemy2L = pygame.image.load('images/enemy2L.png')
enemy2R = pygame.image.load('images/enemy2R.png')

newAccount = True #New or returning player
playerRecord = [] #List for storing user details

class Button(): #Menu buttons
  def __init__(self, x, y, text, restColour, hoverColour):
    self.x = x
    self.y = y
    self.text =  iconfont.render(text, True, white)
    self.colour = restColour
    self.restColour = restColour #When mouse is not hovering over button
    self.hoverColour = hoverColour #When mouse is hovering over button
    self.selected = False #Determine whether mouse over button or not
    self.saved = False #For save button (avoid multiple savings)
    self.clicked = False #If button is clicked or not
  
  def draw(self, mouse):
    button = pygame.Rect(self.x, self.y, 150, 50) #Button rect
    pygame.draw.rect(screen, self.colour, button) #Draw button on screen
    screen.blit(self.text, (self.x + 25, self.y + 15)) #Put text on button
    if button.collidepoint(mouse): #Hover effect
      self.colour = self.hoverColour #Button selected (change colour)
      self.selected = True
    else:
      self.colour = self.restColour #Default if not hovered
      self.selected = False

  def handleEvent(self,event): #Clicking on box
    if event.type == pygame.MOUSEBUTTONDOWN and self.selected:
      selectSound.play() #Button sound
      self.clicked = True 
    else:
      self.clicked = False

class Back(Button): #Back button
  def __init__(self, x, y):
    super().__init__(x, y, '', grey, blue) #superclass used for shared attributes
    self.image = backButtonImg
  
  def draw(self,mouse):
    button = pygame.Rect(self.x, self.y, 100, 25)
    pygame.draw.rect(screen, self.colour, button)
    screen.blit(self.image, (self.x+10, self.y-10)) #Account for image size
    if button.collidepoint(mouse):
      self.colour = blue
      self.selected = True
    else:
      self.colour = grey
      self.selected = False
  
  def handleEvent(self, event): #Clicking to go back
    if event.type == pygame.MOUSEBUTTONDOWN and self.selected:
      backSound.play()
      self.clicked = True
    else:
      self.clicked = False

class textBox(Button): #For user entering text
  def __init__(self, x, y, width, height):
    super().__init__(x, y, '', grey, white)
    self.inputText = '' #Text user can enter
    self.width = width
    self.height = height
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
  
  def draw(self):
    self.txtSurface = inputfont.render(self.inputText, True, black) #Render inputted text each time
    pygame.draw.rect(screen, self.colour, self.rect)
    screen.blit(self.txtSurface, (self.x + 15, self.y + 5))
  
  def handleEvent(self,event, mouse): #Entering text only when active
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(mouse):
        textboxSound.play()
        self.colour = white #Show that it is active
        self.selected = True
      else:
        self.colour = grey
        self.selected = False

    if self.selected: #Enter text into box
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE: #Delete chars
          self.inputText = self.inputText[0:-1] #Create substring (0 -> last char -1)
        else:
          self.inputText += event.unicode #Add Unicode to string for characters
        self.txtSurface = inputfont.render(self.inputText, True, black) #Render inputted text again

class Player(pygame.sprite.Sprite): #Class for player
  def __init__(self, x, y): #For sprite info
    super().__init__()
    self.x = x
    self.y = y
    self.width = 64
    self.height = 64
    self.left = False #Sprite direction
    self.up = False
    self.right = True
    self.down = False
    self.image = player1R
    self.rect = self.image.get_rect() #Rect around image surface for collisions
    self.life = 10 
    self.score = 0
    self.speed = 5 #Distance player moves with each direction press
    self.mins = 0 #For timer
    self.secs = 0
    self.delay = 0
    self.time = 0
    self.archery = False #Switching between normal movement and archery mode 
    self.damageCount = 0 #For timing damages with enemies (avoid spam)
    self.damaged = False #If hit or not
 
  def draw(self): #Place correct player sprite depending on direction
    if self.up == True:
      self.image = player1U
    if self.left == True:
      if self.archery == True: #Different sprite for archery mode
        self.image = player1LBow
      else:
        self.image = player1L
    if self.down == True:
      self.image = player1D
    if self.right == True:
      if self.archery == True:
        self.image = player1RBow
      else:
        self.image = player1R
    screen.blit(self.image, (self.x, self.y))

  def update(self):
    self.rect.center = [self.x, self.y] #Move box with player (always called)

  def collide(self): #Collisions with other sprite groups
    hitPuzzle = pygame.sprite.spritecollide(player, boxes, True) #Touching a puzzle box (sprite, spritegroup to check against, remove or not)
    hitEnemy = pygame.sprite.spritecollide(player, enemies, False)#Touching enemy
    if hitPuzzle:
      selectSound.play()
      puzzleScreen() #Puzzle shown
      pb = puzzleBox((random.randint(200, 1000)), (random.randint(100, 600))) #Respawn a new box
      boxes.add(pb)

    if hitEnemy: #Hit enemy
      if not self.damaged: #Damage
        hitSound.play()
        self.life -= 1
        self.damaged = True
    
    if self.damaged: #If damaged recently (temporary protection)
      self.damageCount += 1 #Increase damage timer
      if self.damageCount % 2 == 1: #If odd, be dark
        self.image.set_alpha(50)
      if self.damageCount % 2 == 0: #If even, be light
        self.image.set_alpha(255)
      if self.damageCount % 60 == 0: #60 seconds of protection
          self.damaged = False
    else:
      self.image.set_alpha(255)
  
class Arrow(pygame.sprite.Sprite): #Bow aim, power and arrow firing
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.width = 20
    self.height = 10
    self.image = arrowR
    self.rect = self.image.get_rect()
    self.shot = False #If fired or not
  
  def draw(self):
    if not self.shot:
      if player.left or player.up:
        self.image = arrowL
      if player.right or player.down:
        self.image = arrowR
    screen.blit(self.image,(self.x - 5, self.y + 15)) #Account for player dimensions
  
  def update(self):
    self.rect.center = [self.x, self.y]
  
  def arrowPath(self, startX, startY, power, angle, arrowTime): #Trajectory once released
    velX = math.cos(angle) * power #Components of velocity
    velY = math.sin(angle) * power
    distX = velX * arrowTime #No drag or horizontal acceleration
    distY = (velY * arrowTime) + ((-20 * (arrowTime)**2)/2)  #s = (ut) + ((at^2)/2) 

    newX = round(startX + distX) #Change values after flight in air
    newY = round(startY - distY)

    return(newX, newY) #New position

class puzzleBox(pygame.sprite.Sprite): #Icons player touches for puzzles
  def __init__(self, x, y):
    super().__init__() #Super class
    self.x = x
    self.y = y
    self.image = puzzleBoxImg
    self.rect = self.image.get_rect()#Rect around image
  
  def draw(self):
    screen.blit(puzzleBoxImg, (self.x, self.y))
  def update(self):
    self.rect.center = [self.x, self.y]

class Enemy(pygame.sprite.Sprite): #Main enemy superclass (Standard horizontal)
  def __init__(self, x, y, turn):
    super().__init__()
    self.x = x
    self.y = y
    self.width = 64
    self.height = 64
    self.direction = True
    self.image = enemy1R
    self.rect = self.image.get_rect() #Hitbox used around sprite for collision
    self.turn = turn #Coordinate where direction changed
    self.path = [self.x, self.turn] #Horizontal path followed
    self.speed = 8
    self.life = 5
    self.alive = True #For removing off screen once life = 0
    self.damageCount = 0
    self.damaged = False
  
  def draw(self):
    if self.alive: #Don't move if not alive
      self.rect.center = [self.x, self.y]
      if self.speed > 0: # Speed positive = Going right
        screen.blit(enemy1R, (self.x, self.y))
        if self.x + self.speed < self.path[1]: #Check if current x is before limit x, allow movement
          self.x += self.speed
        else:
          self.speed = self.speed * -1 #Flip direction if at limit
      if self.speed < 0: #Negative = Going left
        screen.blit(enemy1L, (self.x, self.y))
        if self.x - self.speed > self.path[0]: #Check current x is greater than starting x
          self.x += self.speed
        else:
          self.speed = self.speed * -1 #Flip direction if at start
  
  def update(self):
    self.rect.center = [self.x, self.y]
  
  def collide(self): #When arrow collides with enemy
    hitEnemy = pygame.sprite.spritecollide(arrow, enemies, False)
    if hitEnemy and pygame.Rect.colliderect(arrow.rect, self.rect) and arrow.shot: #Only execute if rects overlapping
      if not self.damaged: #If damaged
        impactSound.play()
        arrow.shot = False
        self.life -= 1
        if self.life <= 0: #Defeated
          if pygame.sprite.spritecollide(arrow, enemies, True): #Remove from group
            self.alive = False
            player.score += 2
        self.damaged = True
    
    if self.damaged: #If damaged recently (temporary protection)
      self.damageCount += 1 #Increase damage timer
      if self.damageCount % 2 == 1: #If odd, be dark
        self.image.set_alpha(50)
      if self.damageCount % 2 == 0: #If even, be light
        self.image.set_alpha(255)
      if self.damageCount % 60 == 0: #60 seconds of protection
        self.damaged = False
    else:
      self.image.set_alpha(255)

class EnemyV(Enemy): #Vertical enemy
  def __init__(self, x, y, turn):
    super().__init__(x, y, turn)
    self.image = enemy2R
    self.path = [self.y, self.turn] #Vertical path followed
    self.speed = 5
  
  def draw(self): #Overide method
    if self.alive:
      if self.speed > 0: # Speed positive = Going down (Y is inverted)
        screen.blit(enemy2R, (self.x, self.y))
        if self.y + self.speed < self.path[1]: #Check if current y is before limit y, allow movement
          self.y += self.speed
        else:
          self.speed = self.speed * -1 #Flip direction if at limit (Go up)                
      if self.speed < 0: #Negative = Going up
        screen.blit(enemy2L, (self.x, self.y))
        if self.y - self.speed > self.path[0]: #Check current x is greater than starting x
          self.y += self.speed
        else:
          self.speed = self.speed * -1 #Flip direction if at start (Go down)
    self.rect.center = [self.x, self.y]

newGameBox = Button(50, 300,'New Game', black, lightblue) #Objects
loadGameBox = Button(50, 400, 'Load Game', black, lightblue)
lbBox = Button(50, 550, 'Leaderboard', black, lightblue)
optionBox = Button(250, 550, 'Options', black, lightblue)
submitBox = Button(250, 550, 'Submit', black, purple)
menuBox = Button(500, 400, 'Main Menu', black, lightblue)
saveBox = Button(500, 500, 'Save', black, purple)
quitBox = Button(500, 600, 'Quit', black, red)
backButton = Back(50, 200)
usernameBox = textBox(100, 250, 500, 50)
passwordBox = textBox(100, 350, 500, 50)
workingBox = textBox(100, 300, 950, 200)
entryBox = textBox(700,550, 350, 50)
clearBox = Button(700, 600, 'Clear', black, red)
musicBox = textBox(300, 230, 100, 50)
effectsBox = textBox(300, 330, 100, 50)
brightnessBox = textBox(300, 430, 100, 50)
player = Player(100, 200) 
arrow = Arrow(player.x, player.y) 
boxes = pygame.sprite.Group() #Group for managing all puzzle boxes
enemies = pygame.sprite.Group() #Group for managing all enemies

musicBox.inputText = '10' #Default settings
effectsBox.inputText = '10'
brightnessBox.inputText = '10'

def setMusicVolume(volume): #Music volume
  pygame.mixer.music.set_volume(volume)

def setEffectsVolume(volume): #Sound effects volume
  selectSound.set_volume(volume)
  selectSound.set_volume(volume)
  selectSound.set_volume(volume)
  selectSound.set_volume(volume)
  selectSound.set_volume(volume)
  selectSound.set_volume(volume)
  selectSound.set_volume(volume)
  selectSound.set_volume(volume)

def hashValue(plainText): #Convert string to hash value
  hash = 0
  for char in plainText:
    hash = (hash*281  ^ ord(char)*997) & 0xFFFFFFFF #Borrowed online
  return hash #Hash value returned

def convertTime(timeString): #Convert time (as stored in file) to mins and secs
  player.mins = int(timeString[0]) #First character is mins
  if timeString[-2] == "0": #Check if secs is 1 digit
    player.secs = int(timeString[-1])
  else:
    player.secs = int(timeString[-2:]) #Last two characters

def area1(): #First area, objects drawn
  global newArea
  screen.blit(area1Img, (0, 0))
  if newArea: #Transitioned into a new screen (respawn objects)
    enemy1 = Enemy(400, 300, 1100) 
    enemy2 = EnemyV(800, 100, 650)
    for i in range(3): #Different boxes and enemies
      pb = puzzleBox((random.randint(200, 1000)), (random.randint(100, 600))) #Boxes in area
      boxes.add(pb)
    enemies.add(enemy1)
    enemies.add(enemy2) 
def area2():
  screen.blit(area2Img, (0, 0))
  if newArea:
    enemy1 = Enemy(100, 500, 1100) 
    enemy2 = EnemyV(500, 50, 650)
    for i in range(4): 
      pb = puzzleBox((random.randint(200, 1000)), (random.randint(100, 600))) 
      boxes.add(pb)
    enemies.add(enemy1)
    enemies.add(enemy2) 
def area3():
  screen.blit(area3Img, (0, 0))
  if newArea:
    enemy1 = Enemy(100, 600, 1100) 
    enemy2 = EnemyV(510, 50, 650)
    for i in range(3): 
      pb = puzzleBox((random.randint(200, 1000)), (random.randint(100, 600))) 
      boxes.add(pb)
    enemies.add(enemy1)
    enemies.add(enemy2) 
def area4():
  screen.blit(area4Img, (0, 0))
  if newArea:
    enemy1 = Enemy(100, 500, 1100) 
    enemy2 = EnemyV(500, 50, 650)
    for i in range(4): 
      pb = puzzleBox((random.randint(200, 1000)), (random.randint(100, 600))) 
      boxes.add(pb)
    enemies.add(enemy1)
    enemies.add(enemy2) 
def area5():
  screen.blit(area5Img, (0, 0))
  if newArea:
    enemy1 = Enemy(70, 400, 1000) 
    enemy2 = EnemyV(500, 50, 600)
    for i in range(2): 
      pb = puzzleBox((random.randint(200, 1000)), (random.randint(100, 600))) 
      boxes.add(pb)
    enemies.add(enemy1)
    enemies.add(enemy2) 
def area6():
  screen.blit(area6Img, (0, 0))
  if newArea:
    enemy1 = Enemy(100, 500, 1100) 
    enemy2 = EnemyV(600, 50, 500)
    for i in range(1): 
      pb = puzzleBox((random.randint(200, 1000)), (random.randint(100, 600))) 
      boxes.add(pb)
    enemies.add(enemy1)
    enemies.add(enemy2) 
def area7():
  screen.blit(area7Img, (0, 0))
  if newArea:
    enemy1 = Enemy(150, 500, 1100) 
    enemy2 = EnemyV(300, 50, 650)
    for i in range(3): 
      pb = puzzleBox((random.randint(200, 1000)), (random.randint(100, 600))) 
      boxes.add(pb)
    enemies.add(enemy1)
    enemies.add(enemy2) 
def area8():
  screen.blit(area8Img, (0, 0))
  if newArea:
    enemy1 = Enemy(200, 600, 1000) 
    enemy2 = EnemyV(350, 50, 650)
    for i in range(2): 
      pb = puzzleBox((random.randint(200, 1000)), (random.randint(100, 600)))
      boxes.add(pb)
    enemies.add(enemy1)
    enemies.add(enemy2) 
def area9():
  screen.blit(area9Img, (0, 0))
  if newArea:
    enemy1 = Enemy(500, 500, 900) 
    enemy2 = EnemyV(400, 50, 500)
    for i in range(3): 
      pb = puzzleBox((random.randint(200, 1000)), (random.randint(100, 600))) 
      boxes.add(pb)
    enemies.add(enemy1)
    enemies.add(enemy2) 

currentArea = 1 #Start from first area
newArea = False 
def mainLoop(): #Main game loop
  pygame.mixer.music.stop()
  pygame.mixer.music.load(gameMusic)
  pygame.mixer.music.play(-1) #Continuously play music
  global currentArea #Use global variable version
  global newArea #Cheching if in a new area
  arrowTime = 0 #For use in SUVAT equation, constant for speed
  power = 0 #Distance of line
  angle = 0 #From horizontal
  run = True
  while run:
    previousArea = currentArea #For checking if a new area is entered
    keys = pygame.key.get_pressed() #For detecting if a key is held
    mouse = pygame.mouse.get_pos() #Gets coordiantes of mouse

    if keys[K_w] and player.y > player.speed: #Player control - only when not shooting and within screen
      player.up = True
      player.left = False
      player.down = False
      player.right = False
      player.y -= player.speed #Move up
      if not arrow.shot: #Arrow follows player until shot
        arrow.y -= player.speed #Move arrow position too
    if keys[K_a] and player.x > player.speed:
      player.up = False
      player.left = True
      player.down = False
      player.right = False
      player.x -= player.speed #Move left
      if not arrow.shot:
        arrow.x -= player.speed
    if keys[K_s] and player.y < screen_height - player.height:
      player.up = False
      player.left = False
      player.down = True
      player.right = False
      player.y += player.speed #Move down
      if not arrow.shot:
        arrow.y += player.speed
    if keys[K_d] and player.x < screen_width - player.width:
      player.up = False
      player.left = False
      player.down = False
      player.right = True
      player.x += player.speed #Move right
      if not arrow.shot:
        arrow.x += player.speed

    if currentArea == 1:#Screen Transitions
      area1()
      if player.x >= 1200: #Meet edge
        currentArea = 2 #Update area
        player.x = 50 #Reset position for natural transition
      if player.y <= 10:
        currentArea = 4
        player.y = 600

    if currentArea == 2:
      area2()
      if player.x <= 10: 
        currentArea = 1
        player.x = 1100
      if player.x >= 1200:
        currentArea = 3
        player.x = 50
      if player.y <= 10: 
        currentArea = 5
        player.y = 600

    if currentArea == 3:
      area3()
      if player.x <= 10:
        currentArea = 2
        player.x = 1100
      if player.y <= 10:
        currentArea = 6
        player.y = 600

    if currentArea == 4:
      area4()
      if player.x >= 1200:
        currentArea = 5
        player.x = 50
      if player.y <= 10:
        currentArea = 7
        player.y = 600
      if player.y >= 650:
        currentArea = 1
        player.y = 50

    if currentArea == 5:
      area5()
      if player.x <= 10:
        currentArea = 4
        player.x = 1100
      if player.x >= 1200:
        currentArea = 6
        player.x = 50
      if player.y <= 10:
        currentArea = 8
        player.y = 600
      if player.y >= 650:
        currentArea = 2
        player.y = 50

    if currentArea == 6:
      area6()
      if player.x <= 10:
        currentArea = 5
        player.x = 1100
      if player.y <= 10:
        currentArea = 9
        player.y = 600
      if player.y >= 650:
        currentArea = 3
        player.y = 50

    if currentArea == 7:
      area7()
      if player.x >= 1200:
        currentArea = 8
        player.x = 50
      if player.y >= 650:
        currentArea = 4
        player.y = 50

    if currentArea == 8:
      area8()
      if player.x <= 10:
        currentArea = 7
        player.x = 1100
      if player.y >= 650:
        currentArea = 5
        player.y = 50
      if player.x >= 1200:
        currentArea = 9
        player.x = 50

    if currentArea == 9:
      area9()
      if player.x <= 10:
        currentArea = 8
        player.x = 1100
      if player.y >= 650:
        currentArea = 6
        player.y = 50
    
    if currentArea != previousArea: #New area
      newArea = True
      enemies.empty()
      boxes.empty()
    else:
      newArea = False
    
    player.draw()
    if arrow.shot: #Only draw when shot
      arrow.draw()
 
    playerTime = (str(player.mins) + ":" + str(player.secs)) #Hotbar ->timer format places colon between mins and secs
    if len(str(player.secs)) == 1: #1 digit second requires ':0' in front
      playerTime = (str(player.mins) + ":0" + str(player.secs))
    
    player.delay += 1
    if player.delay == 30: #1s 
      player.secs += 1
      player.delay = 0
    if player.secs == 60: #60s -> 1m
      player.mins += 1
      player.secs = 0
      player.delay = 0
  
    lifeText = iconfont.render('Life: ' + str(player.life), True, (white)) #Rendered text added to player attributes (stats)
    screen.blit(lifeText, (50, 15)) #Place text in top position
    timerText = iconfont.render('Time: ' + str(playerTime), True, (white)) 
    screen.blit(timerText, (520, 15))
    scoreText = iconfont.render('Score: ' + str(player.score), True, (white))
    screen.blit(scoreText, (1000, 15))
    player.time = playerTime #Give string to player class

    targetLine = [(arrow.x+32, arrow.y+32), (mouse)] #Target line coming from arrow, formed from two points

    if arrow.shot: #Fired
      if 5 < arrow.y < screen_height and 5 < arrow.x < screen_width: #If collided with corner of screen
        arrowTime += 0.07 #Speed in air multiplier
        position = arrow.arrowPath(arrowX,arrowY,power,angle,arrowTime) #returns new position
        arrow.x = position[0]
        arrow.y = position[1]
      else:
        arrow.x = player.x #Reset positions
        arrow.y = player.y 
        arrow.shot = False #Not fired
    else: #Arrow should always be with player unless shot
      arrow.x = player.x
      arrow.y = player.y
    
    player.update() #Update objects
    arrow.update()
    player.collide()
    for box in boxes:
      box.update()
      box.draw()
    for enemy in enemies:
      enemy.collide()
      enemy.draw()

    for event in pygame.event.get(): #Check for any events
      if event.type == pygame.QUIT: #For clicking 'x'
        run = False #Exit loop
      if event.type == pygame.KEYDOWN: #For clicking a key
        if event.key == pygame.K_ESCAPE: #Paused if escape key pressed
          errorSound.play()
          pause()
        if event.key == pygame.K_e: #Change archery mode
          player.archery = not player.archery
      if event.type == pygame.MOUSEBUTTONDOWN: #For clicking the mouse to shoot
        if arrow.shot == False: #Check not already released
          shotSound.play()
          arrow.shot = True
          arrowX = arrow.x
          arrowY = arrow.y
          arrowTime = 0 #Start of arrow in the air
          horizontal = (targetLine[1][0] - targetLine[0][0]) #change in x
          vertical = (targetLine[1][1] - targetLine[0][1]) #change in y
          power = math.sqrt((horizontal)**2 + (vertical)**2)/5 #Length of target line (hypotenuse) to get power (Divided for moderation)
          angle = calculateAngle(mouse) #Angle to fire arrow

    if player.archery and arrow.shot == False: #Only allow one shot at a time
      pygame.draw.line(screen, white, targetLine[0], targetLine[1]) #Line coming from arrow
    if player.life == 0:
      gameOver() #Player runs out of life

    clock.tick(30)
    pygame.display.update()
  pygame.quit() #Close Pygame if run = False
  quit()

def calculateAngle(mouse): #Angle between arrow and horizontal
  sX = arrow.x
  sY = arrow.y
  try:
    angle = math.atan((sY - mouse[1]) / (sX - mouse[0])) #Default case
  except:
    angle = math.pi / 2 #Angle = 90, shoot up        
  if mouse[1] < sY and mouse[0] > sX: #Top right quadrant
    arrow.image = arrowR
    angle = abs(angle) #Absolute value -> magnitude
  elif mouse[1] < sY and mouse[0] < sX:#Top left
    arrow.image = arrowL
    angle = math.pi - angle #Pi = Horizontal
  elif mouse[1] > sY and mouse[0] < sX: #Bottom left
    arrow.image = arrowL
    angle = math.pi + abs(angle) #Fire below horizontal
  elif mouse[1] > sY and mouse[0] > sX: #Bottom right
    arrow.image = arrowR
    angle = (math.pi * 2) - angle #Full revolution - angle
  return angle
 
def leaderboard(): #Displaying top 10 scores
  screen.fill(red)
  screen.blit(leaderboardTitle, (50, 50))
  screen.blit(menuImg, (1000, 50)) #Table structure
  screen.blit(iconfont.render('Username                                  Time                  Score', True, black), (300, 120))
  screenRow = 150 #Y coordinate for first row
  lbList = [] #2D list for storing the sorted list of player rows 
  with open('files/players.csv', 'r') as playerFile:
    playerLines = playerFile.readlines() #List of strings in file (each line is a string)
    for line in playerLines:
      playerRow = line.split(',') #Split fields in string with commas
      if playerRow[5] == ('score'): #Skip past header row
        pass
      else:
        playerRow[5] = int(playerRow[5]) #Make integer for comparison
        lbList.append(playerRow)   
    playerFile.close()
  lbList = sorted(lbList,key=lambda l:l[5], reverse=True) #Sort in descending score order
  for row in lbList:
    playerName = menufont.render(row[0], True, white) #Username, time and score for each line
    playerTime = menufont.render(row[4], True, white)
    playerScore = menufont.render(str(row[5]), True, white)
    screen.blit(playerName, (300, screenRow)) #Blit across screen
    screen.blit(playerTime, (600, screenRow))
    screen.blit(playerScore, (800, screenRow))
    screenRow += 55 #Next row 
    if screenRow == 700: #Stop after 10 rows
      break
  while True:
    mouse = pygame.mouse.get_pos() #Mouse position
    backButton.draw(mouse)
    for event in pygame.event.get(): #Quit the game if the quit button is clicked
      if event.type == pygame.QUIT: #Close if exit button clicked 
        pygame.quit() 
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN: #Back button
        if backButton.selected:
          backSound.play()
          return
      pygame.display.update()

def options(): #Options menu for settings
  screen.fill(purple)
  screen.blit(optionsTitle, (50, 50))
  screen.blit(menuImg, (1000, 50)) #Put image on menu
  screen.blit(iconfont.render('Music:', True, white), (50, 250)) #Controls text displayed
  screen.blit(iconfont.render('Sound effects:', True, white), (50, 350))
  screen.blit(iconfont.render('Brightness:', True, white), (50, 450))
  screen.blit(menufont.render('Controls:', True, white), (800, 250))
  screen.blit(iconfont.render('W/A/S/D = Move up/left/down/right', True, white), (800, 300))
  screen.blit(iconfont.render('E = Draw/Undraw bow', True, white),(800, 350))
  screen.blit(iconfont.render('Right click = Shoot arrow', True, white),(800, 400))
  while True:
    mouse = pygame.mouse.get_pos() #Mouse detection (0, 1) = (x, y)
    backButton.draw(mouse)
    musicBox.draw()
    effectsBox.draw()
    brightnessBox.draw()
    submitBox.draw(mouse)
    for event in pygame.event.get(): 
      musicBox.handleEvent(event,mouse) #Changing volumes 
      effectsBox.handleEvent(event,mouse)
      brightnessBox.handleEvent(event,mouse)
      if event.type == pygame.QUIT: #Close if exit button clicked 
        pygame.quit() 
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if backButton.selected:
          backSound.play()
          return
        if submitBox.selected: #Change volume (0 lowest 1 highest)
          setMusicVolume(int(musicBox.inputText)/10)
          setEffectsVolume(int(effectsBox.inputText)/10)
    pygame.display.update()

def save(): #Write player record to file
  global playerRecord
  global currentArea
  global newAccount
  updatedFile = [] #For updating records

  if newAccount: #Write a new record
    playerRecord.append(currentArea)
    playerRecord.append(player.life)
    playerRecord.append(player.time) #Time format
    playerRecord.append(player.score)
    playerRecord.append(player.x)
    playerRecord.append(player.y)
    playerRow = tuple(playerRecord) #Convert to tuple for writing to file
    file = open('files/players.csv', 'a') #Open for appending
    writer = csv.writer(file) #Writer
    writer.writerow(playerRow) #Writer list as one row

  else: #Update a record
    playerRecord.clear() #Clean first, Update details in playerRecord
    playerRecord = [usernameBox.inputText, passwordBox.inputText, str(currentArea), str(player.life), player.time, str(player.score), str(player.x), str(player.y)]
    file = open('files/players.csv', 'r') #Open for reading
    playerLines = file.readlines() 
    for line in playerLines:
      playerRow = line.split(',')
      updatedFile.append(playerRow) #All lines added to list
    updatedFile.append(playerRecord) #New list has all of player file and updated record
    for row in updatedFile:
      row[7] = str(row[7]).strip('\n')
      if row[0] == playerRecord[0]: #Find player's original record using username as identifier
        updatedFile.remove(row)
    file.close()
    file = open('files/players.csv', 'w')
    writer = csv.writer(file) #Writer (overwrite without commas)
    writer.writerows(updatedFile)
  playerRecord.clear() #Reset for new user

def gameOver():
  while True:
    pygame.mixer.music.stop() #Stop music
    mouse = pygame.mouse.get_pos()
    screen.fill(grey)
    endText = titlefont.render('Game Over', True, red)
    screen.blit(endText, (450, 300))
    menuBox.draw(mouse)
    quitBox.draw(mouse)
    for event in pygame.event.get(): 
      if event.type == pygame.MOUSEBUTTONDOWN:
        if quitBox.selected: 
          pygame.quit() 
          sys.exit()
    pygame.display.update()

def pause(): #For stopping game (keys variable needed to unpause)
  pygame.mixer.music.pause() #Pause game music
  pauseText = titlefont.render('Paused', True, white)
  usernameText = iconfont.render(usernameBox.inputText, True, white)
  while True:
    mouse = pygame.mouse.get_pos()
    screen.blit(pauseText, (500, 300))
    pygame.draw.rect(screen, blue, (100, 100, 120, 50)) 
    screen.blit(usernameText, (110, 120)) #Box for displaying username
    menuBox.draw(mouse)
    saveBox.draw(mouse)
    quitBox.draw(mouse)
    for event in pygame.event.get(): 
      if event.type == pygame.MOUSEBUTTONDOWN: #Close if quit button clicked 
        if menuBox.selected:
          backSound.play()
          pygame.mixer.music.load(menuMusic)
          pygame.mixer.music.play(-1) #Continuously play music
          mainMenu()
        if saveBox.selected:
          if not saveBox.saved: #Not saved
            submitSound.play()
            save()
            saveBox.text = iconfont.render('Saved', True, white) #Avoid saving again accidentally
            saveBox.restColour = green
            saveBox.hoverColour = green
            saveBox.saved = True #If saved successfully
        if quitBox.selected: 
          pygame.quit() 
          sys.exit()
      if event.type == KEYDOWN and event.key == K_ESCAPE: #Break out of loop if escape key pressed again (return to game)
        pygame.mixer.music.unpause() #Unpause
        return
    pygame.display.update()

def newPuzzle(): #Called when puzzle box touched
  currentPuzzle = [] #Array for storing the current puzzle record being used
  with open('files/puzzles.csv', 'r') as puzzleFile: #Open puzzles file for reading
    puzzleReader = csv.reader(puzzleFile, delimiter='\t') #Read all of the file (tab separation)
    header = next(puzzleReader) #Skip over first row (names of fields)
    randPuzzleNum = random.randint(1, 25) #Number of avaliable puzzles
    for line in puzzleReader:
      line[0] = line[0].strip() #Remove tab spacing
      if line[0] == str(randPuzzleNum):
        currentPuzzle.append(line[0]) #Add record to current puzzle list (for each element)
        currentPuzzle.append(line[1])
        currentPuzzle.append(line[2])
        currentPuzzle.append(line[3])
    puzzleFile.close()
    return currentPuzzle

def puzzleScreen():
  pygame.mixer.music.stop()
  pygame.mixer.music.load(puzzleMusic)
  pygame.mixer.music.play(-1) #Continuously play music
  currentPuzzle = newPuzzle() #Get a new puzzle from file
  puzzleSurface = iconfont.render(currentPuzzle[1], True, white)
  resultSurface = titlefont.render('', True, black) #Determined based on correct or not
  workingBox.inputText = ''
  entryBox.inputText = ''
  submitBox.x = 900 #Adjust submit box for puzzle screen
  submitBox.y = 600
  while True:
    mouse = pygame.mouse.get_pos()
    screen.blit(puzzleTitle, (50, 50))
    pygame.draw.rect(screen, black, (50, 115, 1150, 20))
    screen.blit(puzzleSurface, (50, 115))
    pygame.draw.rect(screen, black, (100, 550, 300, 90))
    screen.blit(resultSurface, (110, 560))
    workingBox.draw() #Boxes for puzzle screen
    entryBox.draw()
    clearBox.draw(mouse)
    submitBox.draw(mouse)
    backButton.draw(mouse)

    pygame.draw.rect(screen, black, (500, 10, 120, 40)) #Boarder around time

    playerTime = (str(player.mins) + ":" + str(player.secs)) #Continue to update time when on puzzle screen
    if len(str(player.secs)) == 1: 
      playerTime = (str(player.mins) + ":0" + str(player.secs))
    
    player.delay += 1
    if player.delay == 30: #1s 
      player.secs += 1
      player.delay = 0
    if player.secs == 60: #60s -> 1m
      player.mins += 1
      player.secs = 0
      player.delay = 0
    
    clock.tick(30)
    
    timerText = iconfont.render('Time: ' + str(playerTime), True, (white)) 
    screen.blit(timerText, (520, 15))

    for event in pygame.event.get():
      workingBox.handleEvent(event, mouse)
      entryBox.handleEvent(event, mouse)
      if clearBox.clicked: #Reset boxes
        workingBox.inputText = ''
        entryBox.inputText = ''
        workingBox.draw()
        entryBox.draw()
        pygame.display.update()
      if event.type == pygame.MOUSEBUTTONDOWN: #Click on submit
        if backButton.selected:
          backSound.play()
          pygame.mixer.music.stop()
          pygame.mixer.music.load(gameMusic)
          pygame.mixer.music.set_volume(0.5) #Volume
          pygame.mixer.music.play(-1) #Continuously play music
          return
        if submitBox.selected: 
          run = 0 #For small pause 
          response = entryBox.inputText.lower() #Lowercase
          if response == currentPuzzle[2]: #Check for correct answer
            submitSound.play()
            resultSurface = titlefont.render('Correct!', True, green)
            pygame.draw.rect(screen, black, (100, 550, 300, 90))
            screen.blit(resultSurface, (150, 560)) #Display answer
            player.score += int(currentPuzzle[3]) #Increase score by puzzle worth 
            pygame.display.update()
            while run < 30: #Delay for correct answer screen
              clock.tick(30) #Limits speed
              run += 1
            pygame.mixer.music.stop()
            pygame.mixer.music.load(gameMusic)
            pygame.mixer.music.set_volume(0.5) #Volume
            pygame.mixer.music.play(-1) #Continuously play music
            return
          else:
            errorSound.play()
            pygame.draw.rect(screen, black, (100, 550, 300, 90))
            resultSurface = titlefont.render('Incorrect', True, red) #Incorrect message
            screen.blit(resultSurface, (150, 560))
    pygame.display.update()

def checkLogin(usernameText, passwordText): #Check if username and password match on a row
  global playerRecord
  with open('files/players.csv', 'r') as playerFile:
    playerLines = playerFile.readlines() #List of strings in file (each line is a string)
    for line in playerLines:
      playerRow = line.split(',') #Split fields in string with commas
      if playerRow[0] == usernameText and playerRow[1] == passwordText:
        playerRecord = playerRow
        return True 
  
def checkSignUp(usernameText, passwordText): #Validify account creation
  file = read_csv('files/players.csv') #Open file 
  fileUsernames = file['username'].tolist() #Convert usernames column into list
  unique = True #If username is unique
  passCap = False #If password has a capital letter
  usernameValid = False
  passwordValid = False
  for x in fileUsernames: #Check username against every name in list
    if usernameText == x: #False if username already exists
      unique = False
  for letter in passwordText:
    if letter.isupper(): #At least one is cap
      passCap = True
  if 4 <= len(usernameText) <= 15 and unique: #Only valid if both length valid and unique
    usernameValid = True
  if 8 <= len(passwordText) <= 16 and not(passwordText.isalpha()) and passCap: #Ensure it is not just alphabet characters
    passwordValid = True
  if usernameValid and passwordValid: #Only valid if both valid
    return True
  else:
    return False

def accountScreen(newAccount): #Creating an account/Logging in (empty strings passed)
  global currentArea
  usernameHeader = iconfont.render('Username: 4-15 chars', True, white) #Titles for boxes
  passwordHeader = iconfont.render('Password: 8-16 chars with a capital letter and number', True, white)
  resultSurface = iconfont.render('', True, black)
  usernameBox.inputText = '' #Clear strings
  passwordBox.inputText = ''
  submitBox.x = 250
  submitBox.y = 550
  while True:
    mouse = pygame.mouse.get_pos() #Mouse detection (0, 1) = (x, y)
    screen.blit(menuBG, (0, 0))
    screen.blit(menuImg, (1000, 50)) #Put image on menu
    screen.blit(usernameHeader, (usernameBox.x - 20, usernameBox.y - 20)) #Place titles above boxes
    screen.blit(passwordHeader, (passwordBox.x - 20, passwordBox.y - 20))
    pygame.draw.rect(screen, purple, (100, 450, 400, 50))
    screen.blit(resultSurface, (100, 460))
    backButton.draw(mouse)
    usernameBox.draw()
    passwordBox.draw()
    submitBox.draw(mouse)
    if newAccount:
      screen.blit(newGameTitle, (50, 50)) #Putting the appropriate title on the screen 
    else:
      screen.blit(loadGameTitle, (50, 50)) 
    for event in pygame.event.get():
      if event.type == pygame.QUIT: #Close if exit button clicked 
        pygame.quit() 
        sys.exit()
      usernameBox.handleEvent(event, mouse) #Check if clicked
      passwordBox.handleEvent(event, mouse)
      backButton.handleEvent(event)
      if backButton.clicked:
        return
      if event.type == pygame.MOUSEBUTTONDOWN:
        if submitBox.selected: #Clicking on submit button to start
          if newAccount:
            if checkSignUp(usernameBox.inputText, passwordBox.inputText): #Check valid sign in
              playerRecord.append(usernameBox.inputText) #Add player username and password to their record
              playerRecord.append(hashValue(passwordBox.inputText)) #Add hash value of password
              submitSound.play()
              mainLoop() #Enter game loop
            else:
              errorSound.play() #Error
              resultSurface = iconfont.render('Invalid sign up', True, black)
              screen.blit(resultSurface, (100, 460))
          else:
            if checkLogin(usernameBox.inputText, str(hashValue(passwordBox.inputText))): #Check valid login
              usernameBox.inputText = playerRecord[0]
              passwordBox.inputText = playerRecord[1]
              currentArea = int(playerRecord[2]) #Load in values from record into game
              player.life = int(playerRecord[3])
              player.time = playerRecord[4]
              player.score = int(playerRecord[5])
              player.x = int(playerRecord[6])
              player.y = int(playerRecord[7])
              arrow.x = player.x
              arrow.y = player.y
              convertTime(player.time)
              submitSound.play()
              mainLoop() #Enter game loop
            else: 
              errorSound.play()
              resultSurface = iconfont.render('Username or Password incorrect', True, black)
              screen.blit(resultSurface, (100, 460))
    pygame.display.update()

def mainMenu(): #First menu seen to user
  pygame.mixer.music.load(menuMusic)
  pygame.mixer.music.play(-1) #Continuously play music
  global newAccount
  global playerRecord
  playerRecord.clear() #Reset to avoid multpile records being added to each other
  player.life = 10 #Reset for new account instance (to account for if a previous session finished)
  player.mins = 0
  player.secs = 0
  player.score = 0
  player.x = 100 
  player.y = 200
  saveBox.saved = False 
  saveBox.text = iconfont.render('Save', True, white)
  saveBox.restColour = black
  saveBox.hoverColour = purple

  while True:
    mouse = pygame.mouse.get_pos() #Mouse detection (0, 1) = (x, y)
    screen.blit(menuBG, (0, 0)) #Place background image
    screen.blit(titletext, (50, 50)) #Putting the text on the screen
    screen.blit(menuImg, (1000, 50)) #Put image on menu
    newGameBox.draw(mouse) #Draw boxes 
    loadGameBox.draw(mouse)
    lbBox.draw(mouse)
    optionBox.draw(mouse)

    for event in pygame.event.get(): #Quit the game if the quit button is clicked
      if event.type == pygame.QUIT: #Close if exit button clicked 
        pygame.quit() 
        sys.exit()
      newGameBox.handleEvent(event) #Check for if boxes clicked
      loadGameBox.handleEvent(event)
      lbBox.handleEvent(event)
      optionBox.handleEvent(event)
      if newGameBox.clicked:
        newAccount = True
        accountScreen(newAccount) #New Account
      if loadGameBox.clicked:
        newAccount = False
        accountScreen(newAccount) #For logging into a previously made account
      if lbBox.clicked:
        leaderboard()
      if optionBox.clicked:
        options()
    pygame.display.update()#Update the screen

mainMenu() #First function called