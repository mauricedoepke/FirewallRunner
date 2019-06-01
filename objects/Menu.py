# -*- coding: UTF-8 -*-

#standart lib
import pygame

#game objects
from World import World

class Menu(object):
    def __init__(self, size = (640, 360)):
        #PYGAME INITIALISATION
        pygame.mixer.pre_init(44100, -16, 2, 1024)
        pygame.init()
        pygame.key.set_repeat(180, 100)

        self.clock = pygame.time.Clock()

        #WINDOW SETTINGS
        self.standart_size = 1280, 720
        self.size = size
        self.ratio = (float(size[0])/float(self.standart_size[0])), (float(self.size[1])/float(self.standart_size[1]))

        self.GAMEFPS = 60
        self.MENUFPS = 60

        pygame.display.set_caption('Firewall Runner')
        self.screen = pygame.display.set_mode(self.size)
        self.icon = pygame.image.load('graphic/icon.png').convert()
        pygame.display.set_icon(self.icon)
        pygame.mouse.set_visible(False)

        #MUSIC AND SOUNDS
        pygame.mixer.music.load('music/firewallrunner.ogg')
        pygame.mixer.music.set_volume(.7)#7

        self.fire_sound = pygame.mixer.Sound('music/fire.ogg')
        self.fire_sound.set_volume(.8)#8

        self.jump_sound = pygame.mixer.Sound('music/jump.ogg')
        self.jump_sound.set_volume(.8)#8

        self.success_sound = pygame.mixer.Sound('music/success.ogg')
        self.success_sound.set_volume(.8)#8

        self.screenlist = {"game" : (self.gameScreen, self.GAMEFPS), "pause" : (self.pauseScreen, self.GAMEFPS), "home" : (self.homeScreen, self.MENUFPS), "score" : (self.scoreScreen, self.MENUFPS), "help" : (self.helpScreen, self.MENUFPS), "credits" : (self.creditsScreen, self.MENUFPS)}
        self.nextscreen = "home"
        self.lastscreen = "home"

        self.running = True

        #COLORS
        self.textcolor = 64, 169, 64
        self.bgcolor = 0, 0, 0

        #MENUFONTS
        self.FONTSIZE = int(self.ratio[1] * 40)
        self.BIGFONTSIZE = int(self.ratio[1] * 90)
        self.REALBIGFONTSIZE = int(self.ratio[1] * 110)

        self.font = pygame.font.Font(None, self.FONTSIZE)
        self.bigfont = pygame.font.Font(None, self.BIGFONTSIZE)
        self.realbig = pygame.font.Font(None, self.REALBIGFONTSIZE)

        #FONTRESIZE
        self.BIGFONTNUMBERSIZE = self.bigfont.size("0123456789")[0] / 10

        #MENUTEXTS
        #--GENERAL
        self.title = self.realbig.render("Firewall Runner", True, self.textcolor, self.bgcolor)
        #--HOME
        self.cursor = self.realbig.render(">", True, self.textcolor, self.bgcolor)
        self.start = self.bigfont.render("Start Game", True, self.textcolor, self.bgcolor)
        self.help = self.bigfont.render("Help", True, self.textcolor, self.bgcolor)
        self.credits = self.bigfont.render("Credits", True, self.textcolor, self.bgcolor)
        self.quit = self.bigfont.render("Quit", True, self.textcolor, self.bgcolor)
        self.icon = pygame.transform.scale(self.icon, (int(self.ratio[0]*64), int(self.ratio[0]*64)))
        #--SCORE
        self.gmo = self.realbig.render("Game Over", True, self.textcolor, self.bgcolor)
        self.q = self.font.render("Press [Q] to get to the Main Menu", True, self.textcolor, self.bgcolor)
        self.restart = self.font.render("Press [RETURN] to restart", True, self.textcolor, self.bgcolor)
        #--PAUSE
        self.pausetext = self.realbig.render("Pause", True, self.textcolor, self.bgcolor)
        self.resume = self.font.render("Press any key to resume", True, self.textcolor, self.bgcolor)
        #--HELP
        self.helptitle = self.realbig.render("Help", True, self.textcolor, self.bgcolor)
        
        self.storyline1 = self.font.render("You're a virus und you were detected.", True, self.textcolor, self.bgcolor)
        self.storyline2 = self.font.render("Now run for your life or the Firewall will get you!", True, self.textcolor, self.bgcolor)
        
        self.controlltitle = self.bigfont.render("Controlls", True, self.textcolor, self.bgcolor)
        
        self.controllline1 = self.font.render("Press [Space] to jump", True, self.textcolor, self.bgcolor)
        self.controllline2 = self.font.render("Press [P] to pause the game", True, self.textcolor, self.bgcolor)
        self.controllline3 = self.font.render("Press [Q] to quit the game", True, self.textcolor, self.bgcolor)

        self.pickuptitle = self.bigfont.render("PickUps", True, self.textcolor, self.bgcolor)
        
        self.pickupline1 = self.font.render("fast-forward", True, self.textcolor, self.bgcolor)
        self.pickupline2 = self.font.render("you can do double jumps", True, self.textcolor, self.bgcolor)
        self.pickupline3 = self.font.render("point multiplicator", True, self.textcolor, self.bgcolor)

        self.forwardimage = pygame.image.load('graphic/forward/00001.png').convert()
        self.forwardimage = pygame.transform.scale(self.forwardimage, (int(self.ratio[0]*80), int(self.ratio[1]*60)))
        self.forwardimage.set_colorkey((255,255,255))
        self.multiplierimage = pygame.image.load('graphic/multiplier/00001.png').convert()
        self.multiplierimage = pygame.transform.scale(self.multiplierimage, (int(self.ratio[0]*80), int(self.ratio[1]*60)))
        self.multiplierimage.set_colorkey((255,255,255))
        self.jumpimage = pygame.image.load('graphic/jump/00001.png').convert()
        self.jumpimage = pygame.transform.scale(self.jumpimage, (int(self.ratio[0]*80), int(self.ratio[1]*60)))
        self.jumpimage.set_colorkey((255,255,255))

        self.stumbletitle = self.bigfont.render("Old Data", True, self.textcolor, self.bgcolor)

        self.stumbleimage = pygame.image.load('graphic/olddata/1.png').convert()
        self.stumbleimage.set_colorkey((255,255,255))
        self.stumbleline = self.font.render("collect those to slow you down", True, self.textcolor, self.bgcolor)
        #--CREDITS
        self.creditstitle = self.realbig.render("Credits", True, self.textcolor, self.bgcolor)

        self.programming = self.font.render("Programming:", True, self.textcolor, self.bgcolor)
        self.morris = self.font.render(u"Maurice Döpke", True, self.textcolor, self.bgcolor)

        self.level = self.font.render("Leveldesign:", True, self.textcolor, self.bgcolor)

        self.grafik = self.font.render("Graphic:", True, self.textcolor, self.bgcolor)
        self.philip = self.font.render("Philip Molares", True, self.textcolor, self.bgcolor)
        self.sdcrad = self.font.render("http://www.richandstephsipe.com/wordpress/2008/10/02/", True, self.textcolor, self.bgcolor)
        self.sdcrad2 = self.font.render("free-sd-card-vector-illustration/", True, self.textcolor, self.bgcolor)
        self.music  = self.font.render("Music:", True, self.textcolor, self.bgcolor)
        self.torben = self.font.render(u"Torben Böhnke", True, self.textcolor, self.bgcolor)
        
        self.audio  = self.font.render("Sounds", True, self.textcolor, self.bgcolor)
        self.fire   = self.font.render("Fire:         http://www.freesound.org/people/Dynamicell/sounds/17548/", True, self.textcolor, self.bgcolor)
        self.jump   = self.font.render("Jump:      http://www.freesound.org/people/fins/sounds/146726/", True, self.textcolor, self.bgcolor)
        self.success   = self.font.render("Success:  http://www.freesound.org/people/grunz/sounds/109662/", True, self.textcolor, self.bgcolor)

        #TEXTRESIZE
        #calculate relative positions for resolution independent menues

        #--GENERAL
        self.title_size = self.realbig.size("Firewall Runner")[0]
        self.title_centered = self.size[0] / 2 - self.title_size / 2
        #--HOME
        self.start_size = self.bigfont.size("Start Game")[0]
        self.start_centered = self.size[0] / 2 - self.start_size / 2
        self.help_size = self.bigfont.size("Help")[0]
        self.help_centered = self.size[0] / 2 - self.help_size / 2
        self.credits_size = self.bigfont.size("Credits")[0]
        self.credits_centered = self.size[0] / 2 - self.credits_size / 2
        self.quit_size = self.bigfont.size("Quit")[0]
        self.quit_centered = self.size[0] / 2 - self.quit_size / 2
        #--SCORE
        self.gmo_size = self.realbig.size("Game Over")[0]
        self.gmo_centered = self.size[0] / 2 - self.gmo_size / 2
        self.q_size = self.font.size("Press [Q] to get to the Main Menu")[0]
        self.q_centered = self.size[0] / 2 - self.q_size / 2
        self.restart_size = self.font.size("Press any other key to restart")[0]
        self.restart_centered = self.size[0] / 2 - self.restart_size / 2
        #--PAUSE
        self.pausetext_size = self.realbig.size("Pause")[0]
        self.pausetext_centered = self.size[0] / 2 - self.pausetext_size / 2
        self.resume_size = self.font.size("Press any key to resume")[0]
        self.resume_centered = self.size[0] / 2 - self.resume_size / 2
        #--HELP
        self.helptitle_size = self.realbig.size("Help")[0]
        self.helptitle_centered = self.size[0] / 2 -self.helptitle_size / 2
        self.storyline1_size = self.font.size("You're a virus und you were detected.")[0]
        self.storyline1_centered = self.size[0] / 2 - self.storyline1_size / 2
        self.storyline2_size = self.font.size("Now run for your life or the Firewall will get you!")[0]
        self.storyline2_centered = self.size[0] / 2 - self.storyline2_size / 2
        self.controlltitle_size = self.bigfont.size("Controlls")[0]
        self.controlltitle_centered = self.size[0] / 4 - self.controlltitle_size / 2
        self.controllline1_size = self.font.size("Press [Space] to jump")[0]
        self.controllline1_centered = self.size[0] / 4 - self.controllline1_size / 2
        self.controllline2_size = self.font.size("Press [P] to pause the game")[0]
        self.controllline2_centered = self.size[0] / 4 - self.controllline2_size / 2
        self.controllline3_size = self.font.size("Press [Q] to quit the game")[0]
        self.controllline3_centered = self.size[0] / 4 - self.controllline3_size / 2
        self.pickuptitle_size = self.bigfont.size("PickUps")[0]
        self.pickuptitle_centered = self.size[0] / 2 - self.pickuptitle_size / 2
        self.pickupline2_size = self.font.size("you can do double jumps")[0]
        self.pickupline2_centered = self.size[0] / 2 - self.pickupline2_size / 2
        self.stumbletitle_size = self.bigfont.size("Old Data")[0]
        self.stumbletitle_centered = self.size[0] *3/4 - self.stumbletitle_size / 2
        self.stumbleline_size = self.font.size("collect those to slow you down")[0]
        self.stumbleline_centered = self.size[0] *3/4 - self.stumbleline_size / 2
        #--CREDITS
        self.creditstitle_size = self.realbig.size("Credits")[0]
        self.creditstitle_centered = self.size[0] / 2 - self.creditstitle_size / 2
        self.programming_size = self.font.size("Programming:")[0]
        self.programming_centered = self.size[0] / 4 - self.programming_size / 2 - self.ratio[1] * 120
        self.morris_size = self.font.size("Maurice Döpke")[0]
        self.morris_centered = self.size[0] / 2 - self.ratio[1] * 260


        #MENUVARIABLES
        #--HOME
        self.cursorposition = 0
        self.choicecount = 3

        #--GAME
        self.spaceUp = True

        #--SCORE
        self.score = None
        self.scorelen = None


        ########################startgamemenu
        self.mainloop()


    def gameScreen(self):
        #this is the "gameloop", its not really a loop, but called by the mainloop until it changes the self.nextscreen variable
        fps = self.clock.get_fps()
        timer = 60.0/(fps if fps != 0 else 60.0)
        #the timer variable is necessary for physics and animation to run with the same speed at different framerates
        #all settings are choosen for fps rate of 60 frames/s
        #if the real framerate is 30 fps, timer will be 60/30 = 2 - that will double all movings velocitys/frame to keep the same speed as with real 60 fps
        self.world.setTimer(timer)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.nextscreen = "home"
                    pygame.mixer.music.stop()
                    self.fire_sound.stop()
                if event.key == pygame.K_p:
                    self.nextscreen = "pause"
                    self.world.PowerUpManager.setPause()
                if event.key == pygame.K_SPACE:
                    if self.spaceUp:
                        #initiate a jump when pressing space
                        self.spaceUp = False
                        self.world.player.jump(self.jump_sound)
                    else:
                        #makes the jump stronger if space keeps pressed
                        self.world.player.jumpEnergy += 0.2
                        if self.world.player.jumpEnergy > self.world.player.maxJumpEnergy:
                            self.world.player.jumpEnergy = self.world.player.maxJumpEnergy

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.spaceUp = True
                    
        self.world.render()
        
        #displays the FPS in the upper left corner of the screen (FOR DEBUG ONLY)
        #fps = self.font.render("fps: " + str(fps), True, self.textcolor, self.bgcolor)
        #self.screen.blit(fps,(40,65)) 

        #displays the points in the upper right corner of the screen   
        points = self.bigfont.render(str(int(self.world.points)), True, self.textcolor, self.bgcolor)
        self.screen.blit(points ,(self.size[0] - self.ratio[1] * 20 -( self.BIGFONTNUMBERSIZE * len(str(int(self.world.points)))),self.ratio[1] * 20))
        
        #displays the Speed in the upper left corner of the screen (FOR DEBUG ONLY)
        #speedtext = self.font.render("speed: " + str(self.world.player.speed), True, self.textcolor, self.bgcolor)
        #self.screen.blit(speedtext,(40,85)) 

        if not self.world.player.life:
            self.nextscreen = "score"
            self.score = self.bigfont.render(str(int(self.world.points)), True, self.textcolor, self.bgcolor)
            self.scorelen = len(str(int(self.world.points)))

    def pauseScreen(self):
        #shows the pause screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.nextscreen = "game"
                self.world.PowerUpManager.setPause()

        self.screen.blit(self.pausetext,(self.pausetext_centered, self.ratio[1] * 100))
        self.screen.blit(self.resume,(self.resume_centered, self.ratio[1] * 620))

    def homeScreen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            #menu functionality
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.cursorposition += 1
                    if self.cursorposition > self.choicecount:
                        self.cursorposition = 0
                if event.key == pygame.K_UP:
                    self.cursorposition -= 1
                    if self.cursorposition < 0:
                        self.cursorposition = self.choicecount
                if event.key == pygame.K_RETURN:
                    if self.cursorposition == 0:
                        self.nextscreen = "game" #starts the game after selecting it in menu
                        self.world = World(self.screen, size = self.size, ratio = self.ratio, successound = self.success_sound)
                        self.world.player.life = True
                        pygame.mixer.music.play(-1)
                        self.fire_sound.play(-1)
                    if self.cursorposition == 1:
                        self.nextscreen  = "help" #shows the helpscreen after selecting it
                    if self.cursorposition == 2:
                        self.nextscreen = "credits" #shows the credits after selecting it
                    if self.cursorposition == 3:
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
        self.screen.blit(self.icon,(self.title_centered - self.ratio[0] * 50, self.ratio[1] * 100))
        self.screen.blit(self.title,(self.title_centered + self.ratio[0] * 50, self.ratio[1] * 100))
        self.screen.blit(self.start,(self.start_centered, self.ratio[1] * 300))
        self.screen.blit(self.help,(self.help_centered, self.ratio[1] * 400))
        self.screen.blit(self.credits,(self.credits_centered, self.ratio[1] * 500))
        self.screen.blit(self.quit,(self.quit_centered, self.ratio[1] * 600))

        self.screen.blit(self.cursor,(self.title_centered, (self.ratio[1] * 286 + (self.ratio[1] * 100 * self.cursorposition))))

    def helpScreen(self):
        #shows all the helptexts
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.nextscreen = "home" #shows the homescreen after pressing any key

        self.screen.blit(self.helptitle,(self.helptitle_centered, self.ratio[1] * 20))
        self.screen.blit(self.storyline1,(self.storyline1_centered, self.ratio[1] * 100))
        self.screen.blit(self.storyline2,(self.storyline2_centered, self.ratio[1] * 130))

        self.screen.blit(self.controlltitle,(self.controlltitle_centered, self.ratio[1] * 200))
        self.screen.blit(self.controllline1,(self.controllline1_centered, self.ratio[1] * 280))
        self.screen.blit(self.controllline2,(self.controllline2_centered, self.ratio[1] * 320))
        self.screen.blit(self.controllline3,(self.controllline3_centered, self.ratio[1] * 360))

        self.screen.blit(self.pickuptitle,(self.pickuptitle_centered, self.ratio[1] * 430))
        self.screen.blit(self.pickupline1,(self.pickupline2_centered, self.ratio[1] * 510))
        self.screen.blit(self.pickupline2,(self.pickupline2_centered, self.ratio[1] * 580))
        self.screen.blit(self.pickupline3,(self.pickupline2_centered, self.ratio[1] * 650))
        self.screen.blit(self.forwardimage,(self.pickupline2_centered - (self.ratio[0] * 100), self.ratio[1] * 490))
        self.screen.blit(self.jumpimage,(self.pickupline2_centered - (self.ratio[0] * 100), self.ratio[1] * 560))
        self.screen.blit(self.multiplierimage,(self.pickupline2_centered - (self.ratio[0] * 100), self.ratio[1] * 630))

        self.screen.blit(self.stumbletitle,(self.stumbletitle_centered, self.ratio[1] * 200))
        self.screen.blit(self.stumbleimage,(self.stumbleline_centered - (self.ratio[0] * 100), self.ratio[1] * 300))
        self.screen.blit(self.stumbleline,(self.stumbleline_centered, self.ratio[1] * 320))

    def creditsScreen(self):
        #shows the credits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.nextscreen = "home"

        self.screen.blit(self.creditstitle,(self.creditstitle_centered, self.ratio[1] * 20))

        self.screen.blit(self.programming,(self.programming_centered, self.ratio[1] * 180))
        self.screen.blit(self.morris,(self.morris_centered, self.ratio[1] * 180))

        self.screen.blit(self.level,(self.programming_centered, self.ratio[1] * 240))
        self.screen.blit(self.philip,(self.morris_centered, self.ratio[1] * 240))

        self.screen.blit(self.grafik,(self.programming_centered, self.ratio[1] * 300))
        self.screen.blit(self.philip,(self.morris_centered, self.ratio[1] * 300))
        self.screen.blit(self.sdcrad,(self.morris_centered, self.ratio[1] * 330))
        self.screen.blit(self.sdcrad2,(self.morris_centered, self.ratio[1] * 360))

        self.screen.blit(self.music,(self.programming_centered, self.ratio[1] * 420))
        self.screen.blit(self.torben,(self.morris_centered, self.ratio[1] * 420))

        self.screen.blit(self.audio,(self.programming_centered, self.ratio[1] * 520))
        self.screen.blit(self.fire,(self.morris_centered, self.ratio[1] * 520))
        self.screen.blit(self.jump,(self.morris_centered, self.ratio[1] * 550))
        self.screen.blit(self.success,(self.morris_centered, self.ratio[1] * 580))

    def scoreScreen(self):
        #shows the highscore after dying
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.nextscreen = "home"
                        pygame.mixer.music.stop()
                        self.fire_sound.stop()
                    if event.key == pygame.K_RETURN:
                        self.nextscreen = "game" #shows the homescreen after pressing any key
                        self.nextscreen = "game" #starts the game after selecting it in menu
                        self.world = World(self.screen, size = self.size, ratio = self.ratio, successound = self.success_sound)
                        self.world.player.life = True
                        pygame.mixer.music.play(-1)

        self.screen.blit(self.gmo,(self.gmo_centered, self.ratio[1] * 100))
        self.screen.blit(self.score,((self.size[0] - (self.BIGFONTNUMBERSIZE * self.scorelen))/2, self.ratio[1] * 300))
        self.screen.blit(self.q,(self.q_centered, self.ratio[1] * 580))
        self.screen.blit(self.restart,(self.resume_centered, self.ratio[1] * 640))

    def mainloop(self):
        #the mainloop runs all necessary game logic
        #it runs menuscreens or the game itself, which are implemented in the functions above
        while self.running:
            self.clock.tick(self.screenlist[self.nextscreen][1])
            if self.lastscreen != self.nextscreen:
                self.lastscreen = self.nextscreen
                if self.nextscreen == "game":
                    pygame.key.set_repeat(1, 40)
                else:
                    pygame.key.set_repeat(180, 100)
            self.screen.fill(self.bgcolor)
            self.screenlist[self.nextscreen][0]()
            pygame.display.update()

