import pygame 
import sys 
import maps as m
  
  
# initializing the constructor 
pygame.init() 
  
# screen resolution 
res = (640,530) 
  
# opens up a window 
screen = pygame.display.set_mode(res) 
  
# white color 
color = (255,255,255) 
  
# light shade of the button 
color_light = (255,170,170) 
  
# dark shade of the button 
color_dark = (255,100,100) 
  
# stores the width of the 
# screen into a variable 
width = screen.get_width() 
  
# stores the height of the 
# screen into a variable 
height = screen.get_height() 
  
# defining a font 
smallfont = pygame.font.SysFont('Corbel',35) 
bigfont = pygame.font.SysFont('Corbel',50) 
  
# rendering a text written in 
# this font 
text = smallfont.render('Play Again?' , True , color) 
winners = bigfont.render('The Hunters Win!' , True , color) 
title = bigfont.render('Thanks for playing WhereRU' , True , color) 
  
while True: 
      
    for ev in pygame.event.get(): 
          
        if ev.type == pygame.QUIT: 
            pygame.quit() 
              
        #checks if a mouse is clicked 
        if ev.type == pygame.MOUSEBUTTONDOWN: 
              
            #if the mouse is clicked on the 
            # button the game is terminated 
            if width/2-120 <= mouse[0] <= width/2+240 and height/2-20 <= mouse[1] <= height/2+40: 
                m.run()
                  
    # fills the screen with a color 
    screen.fill((220,20,60)) 
      
    # stores the (x,y) coordinates into 
    # the variable as a tuple 
    mouse = pygame.mouse.get_pos() 
      
    # if mouse is hovered on a button it 
    # changes to lighter shade 
    if width/2 <= mouse[0] <= width/2+140 and height/2-20 <= mouse[1] <= height/2+40: 
        pygame.draw.rect(screen,color_light,[width/2-120,height/2-20,240,40]) 
          
    else: 
        pygame.draw.rect(screen,color_dark,[width/2-120,height/2-20,240,40]) 
      
    # superimposing the text onto our button 
    screen.blit(text , (width/2-95,height/2-20))
    screen.blit(winners , (width/2-150,height/2-140)) 
    screen.blit(title , (width/2-250,height/2-80)) 
      
    # updates the frames of the game 
    pygame.display.update() 