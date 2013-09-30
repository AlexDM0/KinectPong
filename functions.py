import math,numpy,pygame,time,os
  
  
tictac_time = 0
  
def tic():
    global tictac_time
    tictac_time = time.time()
  
def tac(comment = "tictac time"):
    global tictac_time
    time_passed = time.time() - tictac_time
    print comment, " took: ", time_passed, "seconds."
    tictac_time = 0
                
def getBox(x,y,(r,g,b,a),color_factor = 1,alpha_override = -1):
    box = pygame.Surface((x,y),pygame.SRCALPHA, 32)
    if alpha_override == -1:
        box.set_alpha(a*color_factor)
    else:
        box.set_alpha(alpha_override)
    
    box.fill((r*color_factor,g*color_factor,b*color_factor)) 
    return box
  
def getTransparentBox(x,y):
    box = pygame.Surface((x,y),pygame.SRCALPHA, 32)
    box = box.convert_alpha()
    return box
  
def getBorderedBox(x,y,(r,g,b,a),(border_r,border_g,border_b,border_a),width,color_factor = 1):
    box = pygame.Surface((x,y))
    box.set_alpha(a*color_factor)
    box.fill((r*color_factor,g*color_factor,b*color_factor)) 
      
    border = pygame.Surface((x+2*width,y+2*width))
    border.set_alpha(border_a)
    border.fill((border_r,border_g,border_b)) 
      
    border_surface = pygame.Surface((x+2*width,y+2*width),pygame.SRCALPHA, 32)
    border_surface = border_surface.convert_alpha()
      
    border_surface.blit(border,(0,0))
    border_surface.blit(box,(width,width))
    return border_surface
    
def deleteAllFilesInFolder(path):
    if path[-1] == "/":
        path = path[:-1]
    files_in_folder = os.listdir(path)
    for filename in files_in_folder:
        os.remove(path + "/" + filename)
        
def siground(float_value, decimals, plain=False): #round to significant numbers
    formating_string = '%.'+str(decimals)+'g'
    if plain:
        return '%s' % float(formating_string % getFloat(float_value))
    else:
        return '%s' % (formating_string % getFloat(float_value))
  

def getFloat(value):
    value_string = str(value)
    value_final = ""
    if 'e' in value_string.lower():
        value_array = value_string.lower().split('e')
        try:
            value_final = float(value_array[0])*math.pow(10,int(value_array[1]))
        except ValueError:
            value_final = 0
            if value_string != "":
                function_notifications.append("Illegal number detected!")     
    else:
        try:
            value_final = float(value_string)
        except ValueError:
            value_final = 0
            if value_string != "":
                function_notifications.append("Illegal number detected!")     
    return value_final  

