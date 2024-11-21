import pygame
import os
import sys
import time
pygame.init()
clock = pygame.time.Clock()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Button():
    def __init__(self, x, y, image, size) -> None:
        self.__x = x
        self.__y = y
        self.image = image
        self.clicked = False
        if(size != 0):
            self.image = pygame.transform.scale(self.image, (size[0], size[1]))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.__x,self.__y)
            
        
    def draw(self, surface):
        action = False
        #Get moust position
        pos = pygame.mouse.get_pos()
        if(self.rect.collidepoint(pos)):
            if pygame.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                action = True
                
            # if pygame.mouse.get_pressed()[0] and self.clicked == True:
            #     print("The Button Has Already Been Clicked")
            
            if pygame.mouse.get_pressed()[0] == False:
                self.clicked = False
        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

class Room():
    def __init__(self, display, result, objects, gameStateManager) -> None:
        self.display = display
        self.objects = objects
        self.gameStateManager = gameStateManager
        self.result = []
        self.result.append(result)
        
    def run(self):
        self.display.fill((0,0,0))
        
class Shrine(Room):
    def __init__(self, display, result, objects, gameStateManager, homeRoom) -> None:
        super().__init__(display, result, objects, gameStateManager)
        self.base_font = pygame.font.Font(None, 32)
        self.homeRoom = homeRoom
        self.name = "shrine"
    
    def setRoom(self, newHomeRoom):
        self.homeRoom = newHomeRoom
        
    def run(self):        
        while(True):
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    pygame.quit()
            #Write Out The Shrine
            if self.objects["shrine_btn1"].draw(self.display):
                #Move to the first room.
                print("Shrine Clicked")
                self.gameStateManager.setCurrentState("home")            
                return
            if self.objects["shrine_btn2"].draw(self.display):
                #Move to the first room.
                print("Shrine Clicked")
                self.gameStateManager.setCurrentState("home")            
                return
            if self.objects["shrine_btn3"].draw(self.display):
                #Move to the first room.
                print("Shrine Clicked")
                self.gameStateManager.setCurrentState("home")            
                return
            pygame.display.flip()
            clock.tick(60)
            self.display.fill((0,0,0))

class Mirror(Room):
    def __init__(self, display, result, objects, gameStateManager, homeRoom, alex) -> None:
        super().__init__(display, result, objects, gameStateManager)
        self.base_font = pygame.font.Font(None, 32)
        self.homeRoom = homeRoom
        self.name = "mirror"
        self.alex = alex
    
    def setRoom(self, newHomeRoom):
        self.homeRoom = newHomeRoom
        
    def run(self):
        if(self.result[-1]=="None"):
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    pygame.quit()
                self.display.fill((0,0,0))
                if self.objects["mirror_btn"].draw(self.display):
                    #Move to the first room.
                    print("Mirror Clicked")
                    self.gameStateManager.setCurrentState("specChoose")
                    self.result.remove("None")
                    return
                pygame.display.flip()
                clock.tick(60)
        elif(self.result[-1]=="beg" or "bluff" or "blackmail"):
            if(self.result[-1]=="beg"):
                print("beg")
                skills = [3,2,1]
                self.result.remove("beg")
            elif(self.result[-1]=="bluff"):
                print("bluff")
                skills = [2,2,2]
                self.result.remove("bluff")
            elif(self.result[-1]=="blackmail"):    
                print("blackmail")
                skills = [1,2,3]
                self.result.remove("blackmail")            
            self.alex.redoSkills(skills)
            self.alex.printChar(self.display, self.gameStateManager, self.homeRoom.name)
            #Call the create alex thing.
        #catch all the new results and turn it into a thing. 
        # Then display the character sheet.
        #Then go back to home
        pass

class textBoxList():
    def __init__(self, display, speed, textFilename, next_room, font, gameState):
        self.textFilename = textFilename
        self.next_room = next_room
        self.display = display
        self.speed = speed
        self.font = font
        self.gameState = gameState
        self.text_lines = self.split_file()
        self.text_boxes = []
        self.create_list()
    
    def split_file(self):
        total_text = ""
        with open(self.textFilename, 'r') as text2:
            total_text = text2.readlines()
        return total_text
        
    def add(self, text):
        #create the textbox with the list of 1-3 lines. ending with the >
        text_box = textBox(self.display, self.speed, text, self.font, self.gameState)
        #Add the text box to the text box list.
        self.text_boxes.append(text_box)
    
    def create_list(self):
        if(os.path.getsize(self.textFilename) == 0):
            print("Error. No Text In File")
            return
        text = []
        for line in self.text_lines:
            line = line.strip()
            # print(line[-1])
            if(line == ""):
                continue
            text.append(line)
            if(line[-1] == ">"):
                self.add(text)
                text = []
    
    def run(self):
        #go through the lists textBox and then go to the last room.
        for textBox in self.text_boxes:
            textBox.run()
        self.gameState.setCurrentState(self.next_room)
        
class textBox():
    def __init__(self, display, speed, text, font, gameState):
        self.surface = display
        self.active_text = 0
        self.text = text
        self.texts = text[self.active_text]
        self.font = font
        self.speed = speed
        self.gameState = gameState
        self.text_in_progress = True
        self.counter = 0
        
        #Draw the text a bit at a time.
        
        
            #This then chains into the next text Box. maybe create a linked list class
            
    def run(self):
        Ongoing = True
        while(Ongoing):
            #This draws the black background and the white box.
            self.surface.fill((0,0,0))
            pygame.draw.rect(self.surface, "white", (0, 500, 600, 100), 2)
            if(self.text_in_progress):
                        current_text = self.font.render(self.texts[0:self.counter//self.speed], True, (255,255,255))
                        for i in range(self.active_text):
                                self.surface.blit(self.font.render(self.text[i], True, (255,255,255)),(10,510+(i*24)))
                        self.surface.blit(current_text, (10, 510+(self.active_text*24)))
                        self.counter += 1
            else:
                for i in range(len(self.text)):
                    self.surface.blit(self.font.render(self.text[i], True, (255,255,255)),(10,510+(i*24)))
            if(self.counter >= self.speed*len(self.texts)):
                    if(self.active_text+1 == len(self.text)):
                        self.text_in_progress = False
                    else:
                        self.active_text += 1
                        self.texts = self.text[self.active_text] 
                        self.counter = 0
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if(event.key == pygame.K_RETURN):
                        if (self.text_in_progress == False):
                            Ongoing = False
                            self.counter = 0
                            self.active_text = 0
                            self.text_in_progress = True
                            self.texts = self.text[self.active_text]
                            return
                        if(self.active_text+1 == len(self.text)):
                            self.text_in_progress = False
                        else:
                            self.active_text += 1
                            self.texts = self.text[self.active_text]
                            self.counter = 0
                    elif(event.key == pygame.K_ESCAPE):
                        return
                #Set up an if statement that checks if the enter key is pressed and all the words are written
                # if so it moves on to the room pointed next in the linked list
            pygame.display.flip()
            clock.tick(60)
        return
    
class textInput(textBox):
    def __init__(self, display, speed, text, font, gameState, room, returns) -> None:
         super().__init__(display, speed, text, font, gameState)
         #Add in the personal font of Alex. Since it's the same no matter what no need to pass it in.
         self.pFont = None
         self.userInput = ''
         self.room = room
         self.returns = returns
    
    def setRoom(self, room):
        self.room = room
    
    def run(self):
        #Draw the text imediately no scrolling. 
        #Then in a text box above the text box have them type their answer. 
        #send that answer back to the room. and then have that answer change the result attribute.
        Ongoing = True
        while(Ongoing):
            self.surface.fill((0,0,0))
            pygame.draw.rect(self.surface, "white", (0, 500, 600, 100), 2)
            pygame.draw.rect(self.surface, "white", (0, 450, 600, 50), 2)
            for i in range(len(self.text)):
                current_text = self.font.render(self.text[i], True, (255,255,255))        
                self.surface.blit(current_text, (10, 510+i*10))
            user_text = self.font.render(self.userInput, True, (255,255,255))
            self.surface.blit(user_text, (10, 460))
            for event in pygame.event.get():
                    if(event.type == pygame.QUIT):
                        pygame.quit()
                    if(event.type == pygame.KEYDOWN):
                        if(event.key == pygame.K_BACKSPACE):
                            self.userInput = self.userInput[:-1]
                        elif(event.key == pygame.K_RETURN):
                            try:
                                self.room.result.append(self.returns[self.userInput])
                                self.userInput = ""
                                Ongoing = False
                                self.gameState.setCurrentState(self.room.name)
                                return 
                            except KeyError:
                                print("Not a provided answer")
                        #Would need to restructure several things to implement this.
                        # elif(event.key == pygame.K_ESCAPE):
                        #     self.gameState.alex.printChar(self.screen, )
                        elif(event.key == pygame.K_ESCAPE):
                            pass             
                        else:
                            self.userInput += event.unicode
                        
                                        
            pygame.display.flip()
            clock.tick(60)
        return


class Alex():
    def __init__(self, hp, skills):
        self.hp = hp
        self.skills = skills
        
    def printChar(self, screen, gameState, homeRoom):
        #Do this in the text box.
        texts = []
        texts.append("Name: Alex")
        texts.append("Beg: " + str(self.skills["beg"]))
        texts.append("Bluff: " + str(self.skills["bluff"]))
        texts.append("Blackmail: " + str(self.skills["blackmail"]))
        # smaller font size and it would be the custom font.
        textBox(screen, 5, texts, pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), gameState).run() 
        
        gameState.setCurrentState(homeRoom)
        
    def redoSkills(self, skills):
        self.skills["beg"] = skills[0]
        self.skills["bluff"] = skills[1]
        self.skills["blackmail"] = skills[2]
        
    def useBeg(self):
        print(self.skills)
        self.skills["beg"] = self.skills["beg"] + 3
        self.skills["bluff"] = self.skills["bluff"] -1
        self.skills["blackmail"] = self.skills["blackmail"]-1
        if(self.skills["beg"] > 10):
            self.skills["beg"] = 10
        if(self.skills["bluff"] <= 0):
            self.skills["bluff"] = 0
        if(self.skills["blackmail"] <= 0):
            self.skills["blackmail"] = 0
        print(self.skills)
        
            
    def useBluff(self):        
        self.skills["beg"] = self.skills["beg"] - 1
        self.skills["bluff"] = self.skills["bluff"] + 3
        self.skills["blackmail"] -= self.skills["blackmail"]-1
        if(self.skills["bluff"] > 10):
            self.skills["bluff"] = 10
        if(self.skills["beg"] <= 0):
            self.skills["beg"] = 0
        if(self.skills["blackmail"] <= 0):
            self.skills["blackmail"] = 0
        
            
    def useBlackmail(self):
        self.skills["beg"] -= self.skills["beg"] - 1
        self.skills["bluff"] = self.skills["bluff"]- 1
        self.skills["blackmail"] = self.skills["blackmail"]+3
        if(self.skills["blackmail"] > 10):
            self.skills["blackail"] = 10
        if(self.skills["bluff"] <=0):
            self.skills["bluff"] = 0
        if(self.skills["beg"] <=0):
            self.skills["beg"] = 0    

skills = {"beg":1, "bluff":1, "blackmail":1}
alex = Alex(4, skills)

class gameStateManager():
    def __init__(self, current, alex):
        self.__currentState = current
        self.alex = alex
        self.result = ["None"]
        
    def setCurrentState(self, new):
        self.__currentState = new
        
    def getCurrentState(self):
        return self.__currentState


# ---Rooms---
class Home():
    def __init__(self, display, result, objects, gameStateManager) -> None:
        self.display = display 
        self.result = ["None"]
        self.name = "home"
        self.result.append(result)
        self.objects = objects
        self.gameStateManager = gameStateManager
        self.base_font = pygame.font.Font(None, 16)
        self.starter_text = "I open the store, I buy the Hero's goods, I close the store, I cry "
            
    def run(self):
        counter = 0
        if(self.result[0] == "None"):
            while(True):
                self.display.fill((0,0,0))
                text_surface = self.base_font.render(self.starter_text, True, (255,255,255))
                if(counter <= 5):
                    for i in range(counter):
                        time.sleep(1/counter)
                        self.display.blit(text_surface,(150+i*5,300+i*5))
                else:
                    for i in range(counter):
                        time.sleep(.09/counter)
                        self.display.blit(text_surface,(150+i*5,300+i*5))
                if(counter == 61):
                    self.starter_text = "10 Years"
                counter +=1
                #Create the text box class
                for event in pygame.event.get():
                    if(event.type == pygame.QUIT):
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if(event.key == pygame.K_RETURN):
                            #Change to new room once built.
                            if(self.starter_text == "10 Years"):
                                self.starter_text = "I open the store, I buy the Hero's goods, I close the store, I cry "
                                self.result.remove("None")
                                self.result.append("entered")
                                self.gameStateManager.setCurrentState("exposition")                                
                                return
                pygame.display.flip()
                clock.tick(60)
        elif("firstMirror" == self.result[-1]):
            self.result.append("doneMirror")
            self.gameStateManager.setCurrentState("mirror")
        elif("firstShrine" == self.result[-1]):
            self.result.remove("firstShrine")
            self.gameStateManager.setCurrentState("shrine")
        elif("firstShop" == self.result[-1]):
            if("doneMirror" in self.result):                
                self.result.remove("firstShop")
                self.result.append("doneShop")
                self.gameStateManager.setCurrentState("storeExpo")
            else:
                textBox(self.display, 5, ["You Must Face Your Present Before Your Future"], pygame.font.SysFont("stixgeneralbolita", 24, bold=False, italic=False), self.gameStateManager).run() 
                self.gameStateManager.setCurrentState("firstPrompt")
        elif("doneShop" in self.result):
            self.gameStateManager.result.append(self.result[-1])
            self.gameStateManager.setCurrentState("guardExpo")
        elif("entered" in self.result):
            # print(self.result)
            #Set the state to a text input box.          
            self.gameStateManager.setCurrentState("firstPrompt")
            
class Menu(Room):
    def __init__(self, display, objects, gameStateManager, result) -> None:
        super().__init__(display, objects, gameStateManager, result)
        self.base_font = pygame.font.Font(None, 32)
        self.starter_text = "Empty Eyes Can Still Dream" 
        self.counter = 0
    
    def run(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
            self.display.fill((23,34,78))
            text_surface = self.base_font.render(self.starter_text, True, (255,255,255))
            self.display.blit(text_surface,(150,100))
            if self.objects["start_btn"].draw(self.display):
                #Move to the first room.
                print("Start Clicked")
                self.gameStateManager.setCurrentState("home")
            if self.objects["end_btn"].draw(self.display):
                print("End Clicked")
                # self.gameStateManager.setCurrentState("end")
                pygame.quit()
            if self.objects["eye_btn"].draw(self.display):
                print("Eye Clicked")
            self.counter += 1
            pygame.display.flip()
            clock.tick(60)
            
class Hedonist(Room):
    def __init__(self, display, objects, gameStateManager, result) -> None:
        super().__init__(display, objects, gameStateManager, result)
        self.base_font = pygame.font.Font(None, 32)
        self.counter = 0
        self.name = "hedonist"
        
    def run(self, alex):
        while(True):
            print(alex.skills)
            for event in pygame.event.get():
                    if(event.type == pygame.QUIT):
                        pygame.quit()
            if(self.result[-1]=="None"):
                self.display.fill((0,0,0))
                if self.objects["bottle_btn"].draw(self.display):
                    #Move to the first room.
                    print("Bottle Clicked")
                    print("Meeting of the Eyes Initiated")
                    self.result.append("MotE")
            elif("MotE" in self.result):
                print(self.gameStateManager)
                #Pop up a text.textBoxList here on the first go around.
                if(self.counter == 0):
                    hedExpo =  textBoxList(self.display, 2, resource_path("hedExpo.txt"), "hedonist", pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager)
                    hedExpo.run()
                if(self.counter > 3):
                    #textBox here then quit
                    textBox(self.display, 5, ["In A Flash", "You Die, Your Head Smashed Open By A Bottle Of Whiskey", "In Your Last Moments You're Not Sure If You Regretted This"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    sys.quit()
                #Set up a bunch of dialogue checks to see what Jason says.
                print(self.result)
                if(self.result[-1] == "begSuccess" or self.result[-1] == "lieSuccess"):
                    alex.useBeg()
                    textBox(self.display, 5, ["Jason", "No they have to care about me", "I've lost so much for them", "They're all I have left"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["Alex", "They're not all you have left", "I'm here"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                if(self.result[-1] == "begFail" or self.result[-1] == "devLieFail"):
                    textBox(self.display, 5, ["The Hedonist", "Do you think I'm so pathetic that I would accept whatever scraps of love were tosed my way", "I'm a kind one for not smashing your head in right now"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["Alex", "I deeply truly mean it Jason", "I'm here"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                if(self.result[-1] == "devLieSuccess"):
                    alex.useBluff()
                    textBox(self.display, 5, ["The Hedonist", "No you haven't", "You can go past"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["Alex", "Thank you Jason"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    self.gameStateManager.setCurrentState("idealogue")
                    return
                if(self.result[-1] == "devLieMixed"):
                    alex.useBluff()
                    textBox(self.display, 5, ["The Hedonist", "*The Hedonist's face twisted into a frown he says*", "Yes, yes you have, you lied just now, why?", "*An uneasy expressions crosses his face, the Hedonist is unsure how to proceded*"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["Alex", "I didn't lie Jason"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                if(self.result[-1] == "disguiseLieSuccess"):
                    alex.useBluff()
                    textBox(self.display, 5, ["The Hedonist", "Of Course Sir", "*Jason hastily moves aside a couple bottles*","You can go past"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["Alex", "Thank you Jason"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    self.gameStateManager.setCurrentState("idealogue")
                    return
                if(self.result[-1] == "killHedonist"):
                    textBox(self.display, 5, ["The Hedonist", "*In a moment of distraction you sink the obsidian knife into The Hedonist*", "*It writhes in pain, as the obsidian shatters inside its body*","*It stares back up at you confused, as it bleeds out and dies*"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["Alex", "*I breathe in and out, my stomach heaving as I stare at the corpse*", "Unable to take it any longer the contents of my stomach spew on the floor, some bits splattering over the corpse", "I wipe my mouth of the bile before stepping over it and moving on"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    self.gameStateManager.setCurrentState("idealogue")
                    return
                if(self.result[-1] == "failBlackmail" or self.result[-1] == "failBribe"):
                    textBox(self.display, 5, ["The Hedonist", "*The Hedonist's face twists into a horrifying scowl", "Do you think I am a rat, one to scurry around for your whims", "*The Hedonist approaches you a bottle in his hand*"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["Alex", "I raise my hands over my head as I scream","No Please Wait"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["In A Flash", "You Die, Your Head Smashed Open By A Bottle Of Whiskey", "In Your Last Moments You're Not Sure If You Regretted This"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    sys.quit()
                if(self.result[-1] == "bribeSuccess"):
                    alex.useBeg()
                    self.gameStateManager.result.remove("pStone")                    
                    textBox(self.display, 5, ["The Hedonist", "Eh you're right", "You can go past"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["Alex", "Thank you Jason"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    self.gameStateManager.setCurrentState("idealogue")
                    return
                if(self.result[-1] == "bribeMixed"):
                    alex.useBeg()                    
                    textBox(self.display, 5, ["The Hedonist", "I'm no rat I refuse your paltry bribe", "Keep the Pull Stone"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["Alex", "*scowling a bit*", "Alright I'll accept that"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                if(self.result[-1] == "inspireJason"):
                    alex.useBeg()
                    textBox(self.display, 5, ["Jason", "You're right, even if they were my friends it wouldn't matter if it meant helping them hurt Mary", "*Jason presses a gun he pulled out from somewhere into your hand and walks away*","You can go past"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["Alex", "Thank you Jason"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    self.gameStateManager.setCurrentState("idealogue")
                    return
                if(self.result[-1] == "lieHelpSuccess"):
                    alex.useBluff()                    
                    textBox(self.display, 5, ["The Hedonist", "Huh didn't know you were that important", "*Jason hastily moves aside a couple bottles*","You can go past"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["The Hedonist", "Hell have a bottle from me", "*Jason hastily moves grabs one of the rare full bottles and hands it to you*"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["Alex", "Thank you Jason", "I'll put in a good word for you"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    self.gameStateManager.setCurrentState("idealogue")
                    return
                if(self.result[-1] == "destroyJason"):                    
                    textBox(self.display, 5, ["Jason", "*Jason's face twists into a horrific grimace*", "Jason on the floor babbles, No, No, No, I'm not worthless"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["As a gun clatters to the floor you pick it up", "Then with a casual jaunt you step over Jason's comatose body"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    self.gameStateManager.setCurrentState("idealogue")
                    return
                #From here have a loop of checks that figure out what dialogue options there are then initiate a prompt
                answers = {}
                dialogue = []
                if(alex.skills["beg"] >= 1):
                    dialogue.append("1. Jason what are you doing here, do you really think these people are your friends if you're standing gaurd outside barely wearing a thing")
                    answers["1"] = "begSuccess"
                    self.gameStateManager.result.append("inspireHedonist")
                if(alex.skills["beg"] < 1):
                    dialogue.append("1. Jason what are you doing here, do you really think these people are your friends if you're standing gaurd outside barely wearing a thing")
                    answers["1"] = "begFail"                    
                if(alex.skills["bluff"] >= 1):
                    dialogue.append("2. (Lie) Jason I care about you")
                    answers["2"] = "lieSuccess"
                elif(alex.skills["bluff"] < 1):                    
                    dialogue.append("2. (Lie) Jason what are you doing here, do you really think these people are your friends if you're standing gaurd outside barely wearing a thing")
                    answers["2"] = "lieSuccess"
                if(alex.skills["bluff"] >= 3 and "lieSuccess" in self.result):                    
                    dialogue.append("3. (Lie) You know me Jason, have I ever lied to you let me pass")
                    answers["3"] = "devLieSucess"
                    self.gameStateManager.result.append("devastatingLieHedonist")
                if(alex.skills["bluff"] < 3 and "lieSuccess" in self.result):                    
                    dialogue.append("3. (Lie) You know me Jason, have I ever lied to you let me pass")
                    answers["3"] = "devLieMixed"
                if("hatOD" in self.gameStateManager.result):                    
                    dialogue.append("4. (Hat Of Disguise) *Transform into Cultist* May I come in?")
                    answers["4"] = "disguiseLieSuccess"
                    self.gameStateManager.result.append("harmlessLieHedonist")
                if("knife" in self.gameStateManager.result and ("distracted" in self.result or "devLieMixed")):
                    dialogue.append("5. (Knife) While The Hedonist is distracted, you stab him in the back")
                    answers["5"] = "killHedonist"
                    self.gameStateManager.result.append("killedHedonist")
                elif("knife" in self.gameStateManager.result):
                    dialogue.append("5. (Knife) You threaten The Hedonist with the Knife")
                    answers["5"] = "failBlackmail"                    
                if("pStone" in self.gameStateManager.result and alex.skills["beg"] >=5):                    
                    dialogue.append("6. (Pull Stone) You could buy a lot of alchohol with this Jason")                    
                    answers["6"] = "bribeSuccess"
                    self.gameStateManager.result.append("furtherAddictionHedonist")
                elif("pStone" in self.gameStateManager.result and alex.skills["beg"] >=3):                    
                    dialogue.append("6. (Pull Stone) If I give you this Pull Stone will you let me slip past")
                    answers["6"] = "bribeMixed"
                elif("pStone" in self.gameStateManager.result and alex.skills["beg"] < 3):                    
                    dialogue.append("6. (Pull Stone) If I give you this Pull Stone will you let me slip past")
                    answers["6"] = "bribeFail"
                if("begSuccess" in self.result or alex.skills["beg"] >=5):                    
                    dialogue.append("7. You matter Jason, and if you help me, you can finally be someone you can be proud of")
                    answers["7"] = "inspireJason"
                    self.gameStateManager.result.append("gun")
                    self.gameStateManager.result.append("inspireHedonist")
                if(alex.skills["bluff"] >= 5):                    
                    dialogue.append("8. Jason, I'm one important motherfucker and if you help me, I'll make sure the big guy knows you helped me out")
                    answers["8"] = "lieHelpSuccess"
                    self.gameStateManager.result.append("alchohol")
                    self.gameStateManager.result.append("harmlessLieHedonist")
                if(alex.skills["blackmail"] >=5 or "devLieSuccess" in self.result or "devLieMixed" in self.result):                    
                    dialogue.append("9. Jason, Jason, Jason did you really believe me when I said we were friends? You don't have any friends, you're a worthless drunk idiot")
                    answers["9"] = "destroyJason"
                    self.gameStateManager.result.append("gun")
                    self.gameStateManager.result.append("devastateHedonist")
                
                #Run
                print(self.result)
                check = textInput(self.display, 5, dialogue, pygame.font.SysFont("stixgeneralbolita", 10, bold=False, italic=False), self.gameStateManager, self, answers)
                check.run()
                #After the prompt is done, increment by one 
                print(self.counter)
                self.counter += 1
            pygame.display.flip()
            clock.tick(60)
            

class Idealogue(Room):
    def __init__(self, display, objects, gameStateManager, result) -> None:
        super().__init__(display, objects, gameStateManager, result)
        self.base_font = pygame.font.Font(None, 32)
        self.counter = 0
        self.name = "idealogue"
        
    def run(self, alex):
        while(True):
            print(self.gameStateManager.result)
            for event in pygame.event.get():
                    if(event.type == pygame.QUIT):
                        pygame.quit()
            if(self.result[-1]=="None"):
                if(self.counter == 0):
                    hedExpo = textBoxList(self.display, 2, resource_path("ideaExpo.txt"), "idealogue", pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager)
                    hedExpo.run()
                    self.counter += 1 
                self.display.fill((0,0,0))
                if self.objects["idea_btn"].draw(self.display):
                    #Move to the first room.
                    print("Mask Clicked")
                    print("Meeting of the Eyes Initiated")
                    self.result.append("MotE")
                    self.counter = 0
            elif("MotE" in self.result):
                print(self.gameStateManager)                    
                if(self.counter > 3):
                    #textBox here then quit
                    textBox(self.display, 5, ["In A Flash", "You Die, Your Head Flying Off In An Instant", "In Your Last Moments You're Not Sure If You Regretted This"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    pygame.quit()
                #Set up a bunch of dialogue checks to see what Jason says.
                print(self.result)
                if(self.result[-1] == "question"):
                    alex.useBeg()
                    textBox(self.display, 5, ["The Idealogue", "Because fDrEeSePdAoImR is greather than I", "I can entrust the truth to them", "I am one amongst many, who have each found the truth through their eyes"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()                    
                if(self.result[-1] == "blackSuccess"):
                    alex.useBlackmail()
                    textBox(self.display, 5, ["The Idealogue", "They would never do such a thing to me their most valued servant", "*An Involuntary shivver rings through them*"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                if(self.result[-1] == "askLeader"):
                    alex.useBeg()
                    alex.useBluff()
                    textBox(self.display, 5, ["The Idealogue", "Hmm that makes sense I'll consult with them"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                if(self.result[-1] == "disguiseSuccess"):
                    alex.useBluff()
                    textBox(self.display, 5, ["The Idealogue", "*They look at you and scrunch their eyes underneath their blindfold*", "Who are you again?"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["Alex", "I'm a new recruit", "I just saw someone sneak away while you weren't looking", "So"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["The Idealogue", "*An alarmed expression flashes across their blank face*", "Oh, oh no. If they were running they really were an intruder", "*They stride off looking quite alarmed*"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()                    
                    self.gameStateManager.setCurrentState("fDrEeSePdAoImR")
                    return
                if(self.result[-1] == "failAskLeader"):
                    textBox(self.display, 5, ["The Idealogue", "*Their empty eyes twitch* No my word is his will miscreant", "Be Still And SILENT!", "With a shing a previously unseen swords lops your head off"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    pygame.quit()
                if(self.result[-1] == "bribeSuccess"):
                    alex.useBeg()
                    textBox(self.display, 5, ["The Idealogue", "*Briefly a conflicted look pops up on their blank face before they wipe it away*", "This could be quite useful", "Alright I won't bother you, it's not like you'll succeed anyway."], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    self.gameStateManager.setCurrentState("fDrEeSePdAoImR")
                    return
                if(self.result[-1] == "killIdealogue"):
                    textBox(self.display, 5, ["The Idealogue", "One moment they stare at you smugly the next, with a clatter and a series of bangs, they're on the floor dead", "It seems too small for such a larger than life figure, now they're nothing more than a bleeding pile of flesh"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    if("killedHedonist" in self.gameStateManager.result):
                        textBox(self.display, 5, ["Alex", "Oh Above and Below she was frightening" "*I pick up the sword that clattered to the ground*"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    else:
                        textBox(self.display, 5, ["Alex", "*I breathe in and out, my stomach heaving as I stare at the corpse*", "Unable to take it any longer the contents of my stomach spew on the floor, some bits splattering over the corpse", "I wipe my mouth of the bile before stepping over it and moving on"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    self.gameStateManager.setCurrentState("fDrEeSePdAoImR")
                    return
                if(self.result[-1] == "freeJanice"):                    
                    textBox(self.display, 5, ["Janice", "*Jason's face twists into a horrific grimace*", "Jason on the floor babbles, No, No, No, I'm not worthless"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    textBox(self.display, 5, ["As a gun clatters to the floor you pick it up", "Then with a casual jaunt you step over Jason's comatose body"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), self.gameStateManager).run()
                    self.gameStateManager.setCurrentState("fDrEeSePdAoImR")
                    return
                #From here have a loop of checks that figure out what dialogue options there are then initiate a prompt
                answers = {}
                dialogue = []
                if(alex.skills["beg"] > 1):
                    dialogue.append("1. If life has no meaning then how can they give it meaning, if you can't?")
                    answers["1"] = "question"                    
                if(alex.skills["blackmail"] >= 1 and "question" in self.result):
                    dialogue.append("2. If you're just one amongst many aren't you disposable")                    
                    answers["2"] = "blackSuccess"
                if(alex.skills["beg"] >= 5):                    
                    dialogue.append("3. Wait, wait, before you do anything shouldn't you check with the leader first")
                    answers["3"] = "askLeader"                    
                elif(alex.skills["bluff"] >= 3):                    
                    dialogue.append("3. Hey hey I'm not some ordinary bloke, I'm in the middle of the caves shouldn't you get prior authorization first")
                    answers["3"] = "askLeader"
                elif(alex.skills["beg"] < 5 and alex.skills["bluff"] < 3):
                    dialogue.append("3. If you are such a nincompoop that you can't even think of your own philosophy then shouldn't you ask")
                    answers["3"] = "failAskLeader"
                if("pStone" in self.gameStateManager.result or "alchohol" in self.gameStateManager.result):                    
                    dialogue.append("4. (Pull Stone/Alchohol) You look like someone who's been searching for a gift, I wonder if this would work for you")
                    answers["4"] = "bribeSuccess"
                    self.gameStateManager.result.append("bribeIdealogue")
                if("gun" in self.gameStateManager.result):
                    dialogue.append("5. (Gun) You pull the trigger of the gun and keep pulling until they're dead")
                    answers["5"] = "killIdealogue"
                    self.gameStateManager.result.append("killedIdealogue")
                if("hatOD" in self.gameStateManager.result and "askLeader" in self.result):                    
                    dialogue.append("6. (Hat Of Disguise) While the Idealogue was turned around going off to ask their leader for advice you put on a disguise and snuck off")
                    self.gameStateManager.result.remove("hatOD")
                    answers["6"] = "disguiseSuccess"
                    self.gameStateManager.result.append("spareHedonist")
                if("blackSuccess" in self.result and alex.skills["blackmail"] >=3):                    
                    dialogue.append("7. Is a minion that understands that it's disposable a good minion, what would happen if I were to tell your boss")
                    answers["7"] = "disheartenJanice"
                    self.gameStateManager.result.append("disheartenIdealogue")
                elif("blackSuccess" in self.result and not alex.skills["blackmail"] >= 3):                    
                    dialogue.append("7. Is a minion that understands that it's disposable a good minion, what would happen if I were to tell your boss")
                    answers["7"] = "failDisheartenJanice"
                if(alex.skills["bluff"] >=5):                    
                    dialogue.append("8. What you've said makes so much sense, I think I'm going to convert?")
                    answers["8"] = "lieSurrender"
                    self.gameStateManager.result.append("harmlessLieIdealogue")
                if(alex.skills["beg"] >=7 and "blackSuccess" in self.result):                    
                    dialogue.append("9. If you're so worthless to him, and to be discarded so easily then why do you follow him")
                    answers["9"] = "freeJanice"
                    self.gameStateManager.result.append("sword")
                    self.gameStateManager.result.append("freeJanice")
                
                #Run
                print(self.result)
                check = textInput(self.display, 5, dialogue, pygame.font.SysFont("stixgeneralbolita", 10, bold=False, italic=False), self.gameStateManager, self, answers)
                check.run()
                #After the prompt is done, increment by one 
                print(self.counter)
                self.counter += 1
            pygame.display.flip()
            clock.tick(60)
            
class End(Room):
    def __init__(self, display, objects, gameStateManager) -> None:
        self.displays = display
        self.objects = objects
        self.gameStateManager = gameStateManager
        self.name = "fDrEeSePdAoImR"
        self.clicked = False
        self.base_font = pygame.font.Font(None, 32)
        
        
    def run(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
            self.displays.fill((23,34,78))
            if self.objects["eye_btn"].draw(self.displays):
                self.clicked =True
                print("The End")
            if(self.clicked == True):
                text_surface = self.base_font.render("The End.", True, (255,255,255))
                self.displays.blit(text_surface,(250,100))
                text_surface = self.base_font.render("Made By Titanopera for the 2024 Game Jam", True, (255,255,255))
                self.displays.blit(text_surface,(80,150))
        pygame.display.flip()
        clock.tick(60)
            
class Leader(Room):
    def __init__(self, display, objects, gameStateManager) -> None:
        self.displays = display
        self.objects = objects
        self.gameStateManager = gameStateManager
        self.name = "fDrEeSePdAoImR"
        
    def run(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
            print(self.displays)
            self.displays.fill((0,0,0))
            if self.objects["leader_btn"].draw(self.displays):
                self.gameStateManager.setCurrentState("epilogue")
        pygame.display.flip()
        clock.tick(60)
            

screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

#load button images
start_img = pygame.image.load(resource_path("start_btn.jpg")).convert_alpha()
# load_img = pygame.image.load("images/load_btn.png").convert_alpha()
end_img = pygame.image.load(resource_path("end_btn.jpg")).convert_alpha()
empty_eye_img = pygame.image.load(resource_path("empty_eye.jpg")).convert_alpha() 
shrine_img1 = pygame.image.load(resource_path("shrine_img1.jpg")).convert_alpha() 
shrine_img2 = pygame.image.load(resource_path("shrineImg2.jpg")).convert_alpha() 
shrine_img3 = pygame.image.load(resource_path("shrineImg3.jpg")).convert_alpha() 
bottle_img = pygame.image.load(resource_path("hedonism.jpg")).convert_alpha() 
MMR_img = pygame.image.load(resource_path("mightMakesRight.jpg")).convert_alpha() 
leader_img = pygame.image.load(resource_path("despairFreedom.jpg")).convert_alpha() 
populist_img = pygame.image.load(resource_path("populist.jpg")).convert_alpha() 
idea_img = pygame.image.load(resource_path("idealogue.jpg")).convert_alpha() 
FullEye_img = pygame.image.load(resource_path("full_eye_img.jpg")).convert_alpha() 
        
start_btn = Button(125, 375, start_img, (150, 60))
end_btn = Button(325, 375, end_img, (150, 60))
eye_btn = Button(100, 200, empty_eye_img, (400, 100))
mirror_btn = Button(100, 200, empty_eye_img, (400, 100))
shrine_btn1 = Button(100, 50, shrine_img1, (400, 500))
shrine_btn2 = Button(50, 25, shrine_img2, (200, 200))
shrine_btn3 = Button(250 ,300, shrine_img3, (200, 200))
bottle_btn = Button(200, 100, bottle_img, (200, 400))
MMR_btn = Button(200, 100, MMR_img, (100, 400))
populist_btn = Button(200, 100, populist_img, (100, 400))
idea_btn = Button(150, 100, idea_img, (300, 400))
leader_btn = Button(100, 100, leader_img, (400, 400))
FullEye_btn = Button(100, 200, FullEye_img, (400, 100))
        
#Create the game state and set it to menu
gameState = gameStateManager("menu", alex)
old_base_font = pygame.font.Font(None, 24)
base_font = pygame.font.SysFont("stixgeneralbolita", 18, bold=False, italic=False)

states = {
    "home": Home(screen, 0, "None", gameState), 
    "menu": Menu(screen, 0, {"eye_btn":eye_btn, "start_btn":start_btn, "end_btn":end_btn, "leader_btn":leader_btn}, gameState), 
    "exposition":textBoxList(screen, 2, resource_path("expo.txt"), "home", pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), gameState),
    "firstPrompt":textInput(screen, 5, ["You find yourself in your home above your store front, you can move towards", "1. The Mirror Find Your Present", "2. The Shrine Find Your Past", "3.The Shop Find Your Future"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), gameState, "", {"1":"firstMirror", "2":"firstShrine", "3":"firstShop",}),
    "mirror":Mirror(screen, "None", {"mirror_btn":mirror_btn}, gameState, "", alex),
    "specChoose":textInput(screen, 5, ["Do You Wish To Specialize In", "1. Begging, see into others greatest desires, invoke pity, and persuade others", "2. Blackmail, see into others greatest fears, wield fear, and intimidate others", "3. Bluff, see what others want right now, wield lies, confuse others"], pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), gameState, "", {"1":"beg", "2":"blackmail", "3":"bluff",}),
    "shrine":Shrine(screen, "None", {"shrine_btn1":shrine_btn1, "shrine_btn2":shrine_btn2, "shrine_btn3":shrine_btn3}, gameState, ""),
    "storeExpo":textBoxList(screen, 2, resource_path("storeExpo.txt"), "store", pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), gameState),    
    "store":textInput(screen, 5, ["Before You Are Three Options", "1. A Knife, honed but fragile", "2. A Pull Stone, condensed wealth, will wealth help?", "3. Hat Of Disguise, a new face, it won't stick"], pygame.font.SysFont("stixgeneralbolita", 10, bold=False, italic=False), gameState, "", {"1":"knife", "2":"pStone", "3":"hatOD",}),
    "guardExpo":textBoxList(screen, 2, resource_path("guardExpo.txt"), "hedonist", pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), gameState),
    "hedonist":Hedonist(screen, "None", {"bottle_btn":bottle_btn, "eye_btn":eye_btn}, gameState),
    "storeExpo":textBoxList(screen, 2, resource_path("storeExpo.txt"), "store", pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), gameState),
    "idealogue":Idealogue(screen, "None", {"idea_btn":idea_btn, "eye_btn":eye_btn}, gameState),
    "fDrEeSePdAoImR":Leader(screen, {"leader_btn":leader_btn}, gameState),
    "epilogue":textBoxList(screen, 2, resource_path("epi.txt"), "end", pygame.font.SysFont("stixgeneralbolita", 12, bold=False, italic=False), gameState),
    "end":End(screen, {"eye_btn":FullEye_btn}, gameState), 
}

#attaching the room to be changed here.
def setRoomFast(room, newRoom):
    states[room].setRoom(states[newRoom])

setRoomFast("firstPrompt", "home")
setRoomFast("mirror", "home")
setRoomFast("specChoose", "mirror")
setRoomFast("shrine", "home")
setRoomFast("store", "home")


play = True
while(play):
    try:
        #To be deleted
        screen.fill((23,34,78))
        states[gameState.getCurrentState()].run()
    except TypeError:
        #To be deleted
        screen.display.fill((23,34,78))
        states[gameState.getCurrentState()].run(alex)
    clock.tick(60)