import pygame, sys,os
import datetime
from pyfingerprint.pyfingerprint import PyFingerprint
from mfrc522 import SimpleMFRC522
from button import MyButton
from inputbox import InputBox
import requests

os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
os.putenv('DISPLAY','')
# os 环境变量配置要早于pygame.init
WHITE=(255,255,255)
RED=(255,0,0)
GRAY=(128,128,128)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
pygame.init()

SCREEN = pygame.display.set_mode((480, 320))
pygame.display.set_caption("Menu")

def fingerprint_registration():
    SCREEN.fill(WHITE)
    ## Search for a finger

	## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    except Exception as e:
        TEXT1 = pygame.font.Font("assets/font.ttf", 10).render("The fingerprint sensor could not be initialized", True, BLACK)
        RECT1 = TEXT1.get_rect(center=(200, 10))
        SCREEN.blit(TEXT1, RECT1)
        pygame.display.update()
        pygame.time.delay(1000*2)
        main()

	## Tries to search the finger and calculate hash
    try:
        print("try to read image from sensor")
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

		## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)
        print("try to print convert")
		## Searchs template
        result = f.searchTemplate()
        positionNumber = result[0]
        #if position Number > -1,check database have this user or not, else
        if positionNumber > -1:
            #check database have user or not if have call main(), else pass  
            # url = "http://127.0.0.1:4523/mock/976143/person/list"
            # query_params = {"fingerprint":positionNumber} #use position number to indicate user
            # response = requests.get(url,params=query_params)

            # if(response.status_code == 200):
            #     main()
            # else:
            #     pass
            print("i will check user existence or not!")
        else: 
            print("i will store fingerprint")
            positionNumber = f.storeTemplate()
        return positionNumber
			
    
    except Exception as e:
        
        TEXT3 = pygame.font.Font("assets/font.ttf", 10).render("Operation failed", True, BLACK)
        RECT3 = TEXT3.get_rect(center=(100, 10))
        SCREEN.blit(TEXT3, RECT3)
        pygame.display.flip()
        pygame.time.delay(1000*2)
        main()

def registration_page():
    
    while True:

        SCREEN.fill(WHITE)
        MAIN_MOUSE_POS = pygame.mouse.get_pos()

        CURRENT_TIME_TEXT = pygame.font.Font("assets/font.ttf", 10).render(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True, BLACK)
        CURRENT_TIME_RECT = CURRENT_TIME_TEXT.get_rect(center=(240, 20))
        SCREEN.blit(CURRENT_TIME_TEXT, CURRENT_TIME_RECT)

        CHOICE_TEXT = pygame.font.Font("assets/font.ttf", 15).render("Registration method", True, BLACK)
        CHOICE_RECT = CHOICE_TEXT.get_rect(center=(240, 100))
        SCREEN.blit(CHOICE_TEXT, CHOICE_RECT)

        FINGERPRINT_BUTTON = MyButton(image=None, pos=(150, 200), text_input="FINGERPRINT", font=pygame.font.Font("assets/font.ttf", 10), base_color=BLACK, hovering_color=RED)
        FINGERPRINT_BUTTON.changeColor(MAIN_MOUSE_POS)
        FINGERPRINT_BUTTON.update(SCREEN)

        RFID_BUTTON = MyButton(image=None, pos=(330, 200), text_input="RFID", font=pygame.font.Font("assets/font.ttf", 10), base_color=BLACK, hovering_color=RED)
        RFID_BUTTON.changeColor(MAIN_MOUSE_POS)
        RFID_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if FINGERPRINT_BUTTON.checkForInput(MAIN_MOUSE_POS):
                    fingerprint_register_page(None)
                if RFID_BUTTON.checkForInput(MAIN_MOUSE_POS):
                    rfid_register(None)

        pygame.display.update()

def fingerprint_attendance():
	
    SCREEN.fill(WHITE)
    ## Search for a finger

	## Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    except Exception as e:
        TEXT1 = pygame.font.Font("assets/font.ttf", 10).render("The fingerprint sensor could not be initialized", True, BLACK)
        RECT1 = TEXT1.get_rect(center=(20, 10))
        SCREEN.blit(TEXT1, RECT1)
        pygame.time.delay(5000)
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
        print("attendance position:",positionNumber)
        
        if (positionNumber == -1):
            TEXT2 = pygame.font.Font("assets/font.ttf", 10).render("Do not match", True, BLACK)
            RECT2 = TEXT1.get_rect(center=(20, 10))
            SCREEN.blit(TEXT2, RECT2)
            pygame.display.update()
            pygame.time.delay(1000*2)
            main()
        else:
			#positionNumber 对应数据库中的fingerprint项，查找数据库中有无user的fingerprint与positionNumber对应
            #有的话，将数据扯出来传给success，否则回到main
            print("doing http request!")
            url = "http://192.168.1.20:4523/mock/976143/person/list"
            query_params = {"fingerprint":positionNumber}
            response = requests.get(url,params=query_params)
            print(response.json())
            if (response.status_code == 200):
                data = response.json()[0]
                success(data)
            else:
                main()
    
    except Exception as e:
        
        TEXT3 = pygame.font.Font("assets/font.ttf", 10).render("Operation failed", True, BLACK)
        RECT3 = TEXT3.get_rect(center=(20, 10))
        SCREEN.blit(TEXT3, RECT3)
        main()

def enterName(n):
    while True:
        SCREEN.fill(GRAY)
        rect = pygame.draw.rect(SCREEN, WHITE, pygame.Rect(0, 150, 480, 170))
        KEYBOARD = pygame.font.Font("assets/font.ttf", 10).render("Here will be keyboard", True, BLACK)
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
                        if n==0:
                            fingerprint_register_page (widget.returntext())
                        else:
                            rfid_register(widget.returntext())
                widget.handle_event(event)
            widget.draw(SCREEN)
            pygame.display.flip()
            clock.tick(15)
        pygame.display.update()

def popup(choice):
    while True:
        POPUP_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(GRAY)
        rect = pygame.draw.rect(SCREEN, WHITE, pygame.Rect(145, 85, 200, 100))
        
        message1 = pygame.font.Font("assets/font.ttf", 10).render("Sign up", True, BLACK)
        message1_rect = message1.get_rect(center=(242, 110))
        SCREEN.blit(message1, message1_rect)
        
        if choice == 0:
            message2 = pygame.font.Font("assets/font.ttf", 10).render("unsuccessfully", True, BLACK)
            message2_rect = message2.get_rect(center=(242, 130))
            SCREEN.blit(message2, message2_rect)
        else:
            message3 = pygame.font.Font("assets/font.ttf", 10).render("successfully", True, BLACK)
            message3_rect = message3.get_rect(center=(242, 130))
            SCREEN.blit(message3, message3_rect)
        
        MAIN_BACK = MyButton(image=None,pos=(242, 160), text_input="OK", font=pygame.font.Font("assets/font.ttf", 10), base_color=BLACK, hovering_color=RED)
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

def fingerprint_register_page (text):
    hash = None
    while True:
        
        REGISTER_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(WHITE)

        CURRENT_TIME_TEXT = pygame.font.Font("assets/font.ttf", 10).render(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True, BLACK)
        CURRENT_TIME_RECT = CURRENT_TIME_TEXT.get_rect(center=(240, 20))
        SCREEN.blit(CURRENT_TIME_TEXT, CURRENT_TIME_RECT)

        TEXT1 = pygame.font.Font("assets/font.ttf", 10).render("Please type your ID", True, BLACK)
        RECT1 = TEXT1.get_rect(center=(120, 70))
        SCREEN.blit(TEXT1, RECT1)

        if text == None:
            pygame.draw.rect(SCREEN, BLACK, pygame.Rect(20, 100, 200, 20),  2)
        else:
            #name should be stored to the database
            name = pygame.font.Font("assets/font.ttf", 20).render(text, True, BLACK)
            SCREEN.blit(name, name.get_rect(center=(120, 110)))

        ENTERNAME = MyButton(image=None,pos=(120, 140), text_input="ENTER", font=pygame.font.Font("assets/font.ttf", 10), base_color=BLUE, hovering_color=BLACK)
        ENTERNAME.changeColor(REGISTER_MOUSE_POS)
        ENTERNAME.update(SCREEN)

        TEXT2 = pygame.font.Font("assets/font.ttf", 10).render("Please scan your", True, BLACK)
        RECT2 = TEXT1.get_rect(center=(130, 170))
        SCREEN.blit(TEXT2, RECT2)
        TEXT3 = pygame.font.Font("assets/font.ttf", 10).render("fingerprint!", True, BLACK)
        RECT3 = TEXT3.get_rect(center=(120, 185))
        SCREEN.blit(TEXT3, RECT3)

        pygame.draw.rect(SCREEN, BLACK, pygame.Rect(20, 215, 200, 20),  2)
        SCAN = MyButton(image=None,pos=(120, 255), text_input="SCAN", font=pygame.font.Font("assets/font.ttf", 10), base_color=BLUE, hovering_color=BLACK)
        SCAN.changeColor(REGISTER_MOUSE_POS)
        SCAN.update(SCREEN)
        
        IMAGE = pygame.image.load('assets/Square.png')
        IMAGE = pygame.transform.scale(IMAGE, (200, 150))
        IMAGE_RECT = IMAGE.get_rect(center=(360, 160))
        SCREEN.blit(IMAGE, IMAGE_RECT)

        SUBMIT = MyButton(image=None,pos=(120, 300), text_input="SUBMIT", font=pygame.font.Font("assets/font.ttf", 10), base_color=BLACK, hovering_color=RED)
        SUBMIT.changeColor(REGISTER_MOUSE_POS)
        SUBMIT.update(SCREEN)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SUBMIT.checkForInput(REGISTER_MOUSE_POS):
                    if text == None :
                        continue
                    else:
                        # print(text)
                        # print(int(text))
                        user_id = int(text)
                        url = "http://192.168.1.20:4523/mock/976143/person/list"
                        query_params = {"id":user_id}
                        response = requests.get(url,params=query_params)
                        print("response:",response.json())
                        
                        if(response.status_code==404):
                            popup(0)
                        else:
                            
                            path = "http://192.168.1.20:4523/mock/976143/person/modify"
                            # need response name
                            data= {"id":user_id, "fingerprint": hash }
                            resp = requests.post(path,json=data)
                            if(resp.status_code==200):
                                popup(1)
                            else:
                                popup(0)
                if SCAN.checkForInput(REGISTER_MOUSE_POS):
                    hash = fingerprint_registration()
                if ENTERNAME.checkForInput(REGISTER_MOUSE_POS):
                    enterName(0)
        if hash!=None:
            pygame.draw.rect(SCREEN, WHITE, pygame.Rect(20, 215, 200, 20),  2) 
            FINGERPRINT_HASH = pygame.font.Font("assets/font.ttf", 10).render(str(hash), True, BLACK)
            FINGERPRINT_HASH_RECT = FINGERPRINT_HASH.get_rect(center=(120, 225))
            SCREEN.blit(FINGERPRINT_HASH, FINGERPRINT_HASH_RECT)
        pygame.display.update()

def success(hash):
    checkin_time = datetime.datetime.now()
    name=hash["name"]
    print(hash["id"])
    id=str(hash["id"])
    print("Id: ",id)
    print("into sucess!")
    #先通过得到的id去获取信息，然后将当前时间写到记录表
    while True:
        print("into while loop")
        SCREEN.fill(WHITE)

        CURRENT_TIME_TEXT = pygame.font.Font("assets/font.ttf", 10).render(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True, BLACK)
        CURRENT_TIME_RECT = CURRENT_TIME_TEXT.get_rect(center=(240, 20))
        SCREEN.blit(CURRENT_TIME_TEXT, CURRENT_TIME_RECT)
        print("probe 5")
        TEXT1 = pygame.font.Font("assets/font.ttf", 10).render("Check in successfully!", True, BLACK)
        RECT1 = TEXT1.get_rect(center=(120, 70))
        SCREEN.blit(TEXT1, RECT1)
        print("probe 4")
         #take from database based on hash
        NAME_TEXT = pygame.font.Font("assets/font.ttf", 10).render("Name: "+name, True, BLACK)
        NAME_RECT = NAME_TEXT.get_rect(center=(120, 110))
        SCREEN.blit(NAME_TEXT, NAME_RECT)
        print("probe 3")
         #take from database based on hash
        ID_TEXT = pygame.font.Font("assets/font.ttf", 10).render("ID: "+id, True, BLACK)
        ID_RECT = ID_TEXT.get_rect(center=(120, 150))
        SCREEN.blit(ID_TEXT, ID_RECT)
        print("probe 2")
        TEXT2 = pygame.font.Font("assets/font.ttf", 10).render("Your check in time:", True, BLACK)
        RECT2 = TEXT1.get_rect(center=(120, 190))
        SCREEN.blit(TEXT2, RECT2)
        print("probe 1")
        #better to take the value of check in time from database
        CHECKIN_TEXT = pygame.font.Font("assets/font.ttf", 10).render(checkin_time.strftime("%H:%M"), True, BLACK)
        CHECKIN_RECT = CHECKIN_TEXT.get_rect(center=(120, 220))
        SCREEN.blit(CHECKIN_TEXT, CHECKIN_RECT)
        print("probe 0")
        #take from database based on hash
        IMAGE = pygame.image.load('assets/Square.png')
        IMAGE = pygame.transform.scale(IMAGE, (200, 150))
        IMAGE_RECT = IMAGE.get_rect(center=(360, 160))
        SCREEN.blit(IMAGE, IMAGE_RECT)    
        print("what about here?")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        print("am i run?")
        pygame.time.delay(5000)
        main()

def rfid_attendance():
    SCREEN.fill(WHITE)
    reader = SimpleMFRC522()
    try: 
        rfid_id, name = reader.read()
        #insert data reading method
        print(name)
        query_params = {"fingerprint":rfid_id}
        url = "http://192.168.1.20:4523/mock/976143/person/list"
        response = requests.get(url,params=query_params)
        print(response.json())
        data = response.json()[0]
        
    except:
        TEXT = pygame.font.Font("assets/font.ttf", 10).render("User not found", True, BLACK)
        RECT = TEXT.get_rect(center=(20, 10))
        SCREEN.blit(TEXT, RECT)
        pygame.time.delay(5000)
        main()
    else:
        CURRENT_TIME_TEXT = pygame.font.Font("assets/font.ttf", 10).render(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True, BLACK)
        CURRENT_TIME_RECT = CURRENT_TIME_TEXT.get_rect(center=(240, 20))
        SCREEN.blit(CURRENT_TIME_TEXT, CURRENT_TIME_RECT)

        TEXT1 = pygame.font.Font("assets/font.ttf", 10).render("Check in successfully!", True, BLACK)
        RECT1 = TEXT1.get_rect(center=(120, 70))
        SCREEN.blit(TEXT1, RECT1)
        full_name = "Name: "
        name = data["name"]
        full_name = full_name+name
        print(len(name))
        print(full_name)
        NAME_TEXT = pygame.font.Font("assets/font.ttf", 10).render(full_name, True, BLACK)
        NAME_RECT = NAME_TEXT.get_rect(center=(120, 110))
        SCREEN.blit(NAME_TEXT, NAME_RECT)
        print("show name!")
        
        id=data["id"] #take from database based on name or rfid_id
        ID_TEXT = pygame.font.Font("assets/font.ttf", 10).render("ID: "+str(id), True, BLACK)
        ID_RECT = ID_TEXT.get_rect(center=(120, 150))
        SCREEN.blit(ID_TEXT, ID_RECT)

        TEXT2 = pygame.font.Font("assets/font.ttf", 10).render("Your check in time:", True, BLACK)
        RECT2 = TEXT1.get_rect(center=(120, 190))
        SCREEN.blit(TEXT2, RECT2)

        #better to take the value of check in time from database
        CHECKIN_TEXT = pygame.font.Font("assets/font.ttf", 10).render(datetime.datetime.now().strftime("%H:%M"), True, BLACK)
        CHECKIN_RECT = CHECKIN_TEXT.get_rect(center=(120, 220))
        SCREEN.blit(CHECKIN_TEXT, CHECKIN_RECT)

        #take from database 
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
  
def rfid_register(text):
    rfid_id= None
    name = None
    while True:
        
        REGISTER_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(WHITE)

        CURRENT_TIME_TEXT = pygame.font.Font("assets/font.ttf", 10).render(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True, BLACK)
        CURRENT_TIME_RECT = CURRENT_TIME_TEXT.get_rect(center=(240, 20))
        SCREEN.blit(CURRENT_TIME_TEXT, CURRENT_TIME_RECT)

        TEXT1 = pygame.font.Font("assets/font.ttf", 10).render("Please type your ID", True, BLACK)
        RECT1 = TEXT1.get_rect(center=(120, 70))
        SCREEN.blit(TEXT1, RECT1)

        if text == None:
            pygame.draw.rect(SCREEN, BLACK, pygame.Rect(20, 100, 200, 20),  2)
        else:
            #name should be stored to the database
            name = pygame.font.Font("assets/font.ttf", 20).render(text, True, BLACK)
            SCREEN.blit(name, name.get_rect(center=(120, 110)))

        ENTERNAME = MyButton(image=None,pos=(120, 140), text_input="ENTER", font=pygame.font.Font("assets/font.ttf", 10), base_color=BLUE, hovering_color=BLACK)
        ENTERNAME.changeColor(REGISTER_MOUSE_POS)
        ENTERNAME.update(SCREEN)

        TEXT2 = pygame.font.Font("assets/font.ttf", 10).render("Please scan your", True, BLACK)
        RECT2 = TEXT1.get_rect(center=(130, 170))
        SCREEN.blit(TEXT2, RECT2)
        TEXT3 = pygame.font.Font("assets/font.ttf", 10).render("fingerprint!", True, BLACK)
        RECT3 = TEXT3.get_rect(center=(120, 185))
        SCREEN.blit(TEXT3, RECT3)

        pygame.draw.rect(SCREEN, BLACK, pygame.Rect(20, 215, 200, 20),  2)
        SCAN = MyButton(image=None,pos=(120, 255), text_input="SCAN", font=pygame.font.Font("assets/font.ttf", 10), base_color=BLUE, hovering_color=BLACK)
        SCAN.changeColor(REGISTER_MOUSE_POS)
        SCAN.update(SCREEN)
        
        IMAGE = pygame.image.load('assets/Square.png')
        IMAGE = pygame.transform.scale(IMAGE, (200, 150))
        IMAGE_RECT = IMAGE.get_rect(center=(360, 160))
        SCREEN.blit(IMAGE, IMAGE_RECT)

        SUBMIT = MyButton(image=None,pos=(120, 300), text_input="SUBMIT", font=pygame.font.Font("assets/font.ttf", 10), base_color=BLACK, hovering_color=RED)
        SUBMIT.changeColor(REGISTER_MOUSE_POS)
        SUBMIT.update(SCREEN)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SUBMIT.checkForInput(REGISTER_MOUSE_POS):
                    if text == None :
                        continue
                    else:
                        # print(text)
                        # print(int(text))
                        user_id = int(text)
                        url = "http://192.168.1.20:4523/mock/976143/person/list"
                        query_params = {"id":user_id}
                        response = requests.get(url,params=query_params)
                        print("response:",response.json())
                        
                        if(response.status_code==404):
                            popup(0)
                        else:
                            
                            path = "http://192.168.1.20:4523/mock/976143/person/modify"
                            # need response name
                            data= {"id":user_id, "fingerprint": rfid_id }
                            resp = requests.post(path,json=data)
                            if(resp.status_code==200):
                                popup(1)
                            else:
                                popup(0)
                if SCAN.checkForInput(REGISTER_MOUSE_POS):
                    reader = SimpleMFRC522()
                    #reader.write(name)
                    rfid_id, name = reader.read()
                if ENTERNAME.checkForInput(REGISTER_MOUSE_POS):
                    enterName(1)
        if rfid_id!=None:
            pygame.draw.rect(SCREEN, WHITE, pygame.Rect(20, 215, 200, 20),  2) 
            RFID_ID_TEXT = pygame.font.Font("assets/font.ttf", 10).render(str(rfid_id), True, BLACK)
            RFID_ID_TEXT_RECT = RFID_ID_TEXT.get_rect(center=(120, 225))
            SCREEN.blit(RFID_ID_TEXT, RFID_ID_TEXT_RECT)
        pygame.display.update()    

def main():
    
    while True:

        SCREEN.fill(WHITE)
        MAIN_MOUSE_POS = pygame.mouse.get_pos()

        CURRENT_TIME_TEXT = pygame.font.Font("assets/font.ttf", 10).render(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True, BLACK)
        CURRENT_TIME_RECT = CURRENT_TIME_TEXT.get_rect(center=(240, 20))
        SCREEN.blit(CURRENT_TIME_TEXT, CURRENT_TIME_RECT)

        WELCOME_TEXT = pygame.font.Font("assets/font.ttf", 25).render("Welcome", True, BLACK)
        WELCOME_RECT = WELCOME_TEXT.get_rect(center=(240, 110))
        SCREEN.blit(WELCOME_TEXT, WELCOME_RECT)

        CHOICE_TEXT = pygame.font.Font("assets/font.ttf", 15).render("Scanning method", True, BLACK)
        CHOICE_RECT = CHOICE_TEXT.get_rect(center=(240, 160))
        SCREEN.blit(CHOICE_TEXT, CHOICE_RECT)

        FINGERPRINT_BUTTON = MyButton(image=None, pos=(150, 220), text_input="FINGERPRINT", font=pygame.font.Font("assets/font.ttf", 10), base_color=BLACK, hovering_color=RED)
        FINGERPRINT_BUTTON.changeColor(MAIN_MOUSE_POS)
        FINGERPRINT_BUTTON.update(SCREEN)

        RFID_BUTTON = MyButton(image=None, pos=(330, 220), text_input="RFID", font=pygame.font.Font("assets/font.ttf", 10), base_color=BLACK, hovering_color=RED)
        RFID_BUTTON.changeColor(MAIN_MOUSE_POS)
        RFID_BUTTON.update(SCREEN)

        REGISTER_BUTTON = MyButton(image=None, pos=(400, 50), text_input="REGISTRATION", font=pygame.font.Font("assets/font.ttf", 10), base_color=BLACK, hovering_color=RED)
        REGISTER_BUTTON.changeColor(MAIN_MOUSE_POS)
        REGISTER_BUTTON.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REGISTER_BUTTON.checkForInput(MAIN_MOUSE_POS):
                    registration_page()
                if FINGERPRINT_BUTTON.checkForInput(MAIN_MOUSE_POS):
                    fingerprint_attendance()
                if RFID_BUTTON.checkForInput(MAIN_MOUSE_POS):
                    rfid_attendance()
            #if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_0:  #if you press 0, register
                 #   register(None)
                #if event.key == pygame.K_1: #if ypu press 1, scan 
                 #   attendance_finger()
        pygame.display.update()

main()