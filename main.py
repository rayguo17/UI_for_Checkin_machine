import pygame, sys
import datetime
import hashlib
#from pyfingerprint import PyFingerprint
from button import MyButton
from inputbox import InputBox


pygame.init()

SCREEN = pygame.display.set_mode((480, 320))
pygame.display.set_caption("Menu")

def registration_finger():
    SCREEN.fill("White")
    ## Search for a finger

	## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 9600, 0xFFFFFFFF, 0x00000000)
    except Exception as e:
        TEXT1 = pygame.font.Font("assets/font.ttf", 10).render("The fingerprint sensor could not be initialized", True, "Black")
        RECT1 = TEXT1.get_rect(center=(20, 10))
        SCREEN.blit(TEXT1, RECT1)
        main()

	## Tries to search the finger and calculate hash
    try:
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

		## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

		## Searchs template
        result = f.searchTemplate()
        ## Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
        val_hash = hashlib.sha256(characterics).hexdigest()
			
    
    except Exception as e:
        
        TEXT3 = pygame.font.Font("assets/font.ttf", 10).render("Operation failed", True, "Black")
        RECT3 = TEXT3.get_rect(center=(20, 10))
        SCREEN.blit(TEXT3, RECT3)
        main()

def attendance_finger():
	
    SCREEN.fill("White")
    ## Search for a finger

	## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 9600, 0xFFFFFFFF, 0x00000000)
    except Exception as e:
        TEXT1 = pygame.font.Font("assets/font.ttf", 10).render("The fingerprint sensor could not be initialized", True, "Black")
        RECT1 = TEXT1.get_rect(center=(20, 10))
        SCREEN.blit(TEXT1, RECT1)
        main()

	## Tries to search the finger and calculate hash
    try:
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

		## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

		## Searchs template
        result = f.searchTemplate()
        
        positionNumber = result[0]
        accuracyScore = result[1]
        
        if (positionNumber == -1):
            TEXT2 = pygame.font.Font("assets/font.ttf", 10).render("Do not match", True, "Black")
            RECT2 = TEXT1.get_rect(center=(20, 10))
            SCREEN.blit(TEXT2, RECT2)
            main()
        else:
			## Create Hash Value for finger

			## Loads the found template to charbuffer 1
            f.loadTemplate(positionNumber, 0x01)

			## Downloads the characteristics of template loaded in charbuffer 1
            characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
            val_hash = hashlib.sha256(characterics).hexdigest()
			
            success(val_hash)
    
    except Exception as e:
        
        TEXT3 = pygame.font.Font("assets/font.ttf", 10).render("Operation failed", True, "Black")
        RECT3 = TEXT3.get_rect(center=(20, 10))
        SCREEN.blit(TEXT3, RECT3)
        main()

def enterName():
    while True:
        SCREEN.fill("Gray")
        rect = pygame.draw.rect(SCREEN, "White", pygame.Rect(0, 150, 480, 170))
        KEYBOARD = pygame.font.Font("assets/font.ttf", 10).render("Here will be keyboard", True, "Black")
        SCREEN.blit(KEYBOARD, KEYBOARD.get_rect(center=(240, 250)))
        widget=InputBox(150,90)
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        register (widget.returntext())
                widget.handle_event(event)
            widget.draw(SCREEN)
            pygame.display.flip()
            clock.tick(15)
        pygame.display.update()

def popup(choice):
    while True:
        POPUP_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("Gray")
        rect = pygame.draw.rect(SCREEN, "White", pygame.Rect(145, 85, 200, 100))
        
        message1 = pygame.font.Font("assets/font.ttf", 10).render("Sign up", True, "Black")
        message1_rect = message1.get_rect(center=(242, 110))
        SCREEN.blit(message1, message1_rect)
        
        if choice == 0:
            message2 = pygame.font.Font("assets/font.ttf", 10).render("unsuccessfully", True, "Black")
            message2_rect = message2.get_rect(center=(242, 130))
            SCREEN.blit(message2, message2_rect)
        else:
            message3 = pygame.font.Font("assets/font.ttf", 10).render("successfully", True, "Black")
            message3_rect = message3.get_rect(center=(242, 130))
            SCREEN.blit(message3, message3_rect)
        
        MAIN_BACK = MyButton(image=None,pos=(242, 160), text_input="OK", font=pygame.font.Font("assets/font.ttf", 10), base_color="Black", hovering_color="Red")
        MAIN_BACK.changeColor(POPUP_MOUSE_POS)
        MAIN_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MAIN_BACK.checkForInput(POPUP_MOUSE_POS):
                    main()

        pygame.display.update()

def register(text):
    
    while True:
        
        REGISTER_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("White")

        CURRENT_TIME_TEXT = pygame.font.Font("assets/font.ttf", 10).render(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True, "Black")
        CURRENT_TIME_RECT = CURRENT_TIME_TEXT.get_rect(center=(240, 20))
        SCREEN.blit(CURRENT_TIME_TEXT, CURRENT_TIME_RECT)

        TEXT1 = pygame.font.Font("assets/font.ttf", 10).render("Please type your ID", True, "Black")
        RECT1 = TEXT1.get_rect(center=(120, 70))
        SCREEN.blit(TEXT1, RECT1)

        if text == None:
            pygame.draw.rect(SCREEN, "Black", pygame.Rect(20, 100, 200, 20),  2)
        else:
            #name should be stored to the database
            name = pygame.font.Font("assets/font.ttf", 20).render(text, True, "Black")
            SCREEN.blit(name, name.get_rect(center=(120, 110)))

        ENTERNAME = MyButton(image=None,pos=(120, 140), text_input="ENTER", font=pygame.font.Font("assets/font.ttf", 10), base_color="Blue", hovering_color="Black")
        ENTERNAME.changeColor(REGISTER_MOUSE_POS)
        ENTERNAME.update(SCREEN)

        TEXT2 = pygame.font.Font("assets/font.ttf", 10).render("Please scan your", True, "Black")
        RECT2 = TEXT1.get_rect(center=(130, 170))
        SCREEN.blit(TEXT2, RECT2)
        TEXT3 = pygame.font.Font("assets/font.ttf", 10).render("fingerprint!", True, "Black")
        RECT3 = TEXT3.get_rect(center=(120, 185))
        SCREEN.blit(TEXT3, RECT3)

        pygame.draw.rect(SCREEN, "Black", pygame.Rect(20, 215, 200, 20),  2)
        SCAN = MyButton(image=None,pos=(120, 255), text_input="SCAN", font=pygame.font.Font("assets/font.ttf", 10), base_color="Blue", hovering_color="Black")
        SCAN.changeColor(REGISTER_MOUSE_POS)
        SCAN.update(SCREEN)
        
        IMAGE = pygame.image.load('assets/Square.png')
        IMAGE = pygame.transform.scale(IMAGE, (200, 150))
        IMAGE_RECT = IMAGE.get_rect(center=(360, 160))
        SCREEN.blit(IMAGE, IMAGE_RECT)

        SUBMIT = MyButton(image=None,pos=(120, 300), text_input="SUBMIT", font=pygame.font.Font("assets/font.ttf", 10), base_color="Black", hovering_color="Red")
        SUBMIT.changeColor(REGISTER_MOUSE_POS)
        SUBMIT.update(SCREEN)

        hash = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SUBMIT.checkForInput(REGISTER_MOUSE_POS):
                    #if there is a record:
                        #popup(1)
                    #else:
                        #popup(0)
                    popup(0)
                if SCAN.checkForInput(REGISTER_MOUSE_POS):
                    hash = registration_finger()
                if ENTERNAME.checkForInput(REGISTER_MOUSE_POS):
                    enterName()
        if hash!=None:
            pygame.draw.rect(SCREEN, "White", pygame.Rect(20, 215, 200, 20),  2) 
            FINGERPRINT_HASH = pygame.font.Font("assets/font.ttf", 10).render(str(hash), True, "Black")
            FINGERPRINT_HASH_RECT = FINGERPRINT_HASH.get_rect(center=(120, 225))
            SCREEN.blit(FINGERPRINT_HASH, FINGERPRINT_HASH_RECT)
        pygame.display.update()

def success(hash):
    
    while True:

        SCREEN.fill("White")

        CURRENT_TIME_TEXT = pygame.font.Font("assets/font.ttf", 10).render(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True, "Black")
        CURRENT_TIME_RECT = CURRENT_TIME_TEXT.get_rect(center=(240, 20))
        SCREEN.blit(CURRENT_TIME_TEXT, CURRENT_TIME_RECT)

        TEXT1 = pygame.font.Font("assets/font.ttf", 10).render("Check in successfully!", True, "Black")
        RECT1 = TEXT1.get_rect(center=(120, 70))
        SCREEN.blit(TEXT1, RECT1)
    
        name="bob" #take from database based on hash
        NAME_TEXT = pygame.font.Font("assets/font.ttf", 10).render("Name: "+name, True, "Black")
        NAME_RECT = NAME_TEXT.get_rect(center=(120, 110))
        SCREEN.blit(NAME_TEXT, NAME_RECT)
        
        id="123" #take from database based on hash
        ID_TEXT = pygame.font.Font("assets/font.ttf", 10).render("ID: "+id, True, "Black")
        ID_RECT = ID_TEXT.get_rect(center=(120, 150))
        SCREEN.blit(ID_TEXT, ID_RECT)

        TEXT2 = pygame.font.Font("assets/font.ttf", 10).render("Your check in time:", True, "Black")
        RECT2 = TEXT1.get_rect(center=(120, 190))
        SCREEN.blit(TEXT2, RECT2)

        #better to take the value of check in time from database
        CHECKIN_TEXT = pygame.font.Font("assets/font.ttf", 10).render(datetime.datetime.now().strftime("%H:%M"), True, "Black")
        CHECKIN_RECT = CHECKIN_TEXT.get_rect(center=(120, 220))
        SCREEN.blit(CHECKIN_TEXT, CHECKIN_RECT)

        #take from database based on hash
        IMAGE = pygame.image.load('assets/Square.png')
        IMAGE = pygame.transform.scale(IMAGE, (200, 150))
        IMAGE_RECT = IMAGE.get_rect(center=(360, 160))
        SCREEN.blit(IMAGE, IMAGE_RECT)    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        pygame.time.delay(5000)
        main()

def main():
    
    while True:

        SCREEN.fill("White")
        MAIN_MOUSE_POS = pygame.mouse.get_pos()

        CURRENT_TIME_TEXT = pygame.font.Font("assets/font.ttf", 10).render(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True, "Black")
        CURRENT_TIME_RECT = CURRENT_TIME_TEXT.get_rect(center=(240, 20))
        SCREEN.blit(CURRENT_TIME_TEXT, CURRENT_TIME_RECT)

        SCAN_BUTTON = MyButton(image=None, pos=(240, 180), text_input="SCAN", font=pygame.font.Font("assets/font.ttf", 10), base_color="Black", hovering_color="Red")
        SCAN_BUTTON.changeColor(MAIN_MOUSE_POS)
        SCAN_BUTTON.update(SCREEN)

        REGISTER_BUTTON = MyButton(image=None, pos=(240, 140), text_input="REGISTER", font=pygame.font.Font("assets/font.ttf", 10), base_color="Black", hovering_color="Red")
        REGISTER_BUTTON.changeColor(MAIN_MOUSE_POS)
        REGISTER_BUTTON.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REGISTER_BUTTON.checkForInput(MAIN_MOUSE_POS):
                    register(None)
                if SCAN_BUTTON.checkForInput(MAIN_MOUSE_POS):
                    attendance_finger()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:  #if you press 0, register
                    register(None)
                if event.key == pygame.K_1: #if ypu press 1, scan 
                    attendance_finger()
        pygame.display.update()

main()