# -*- coding: utf-8 -*-    
from cv2 import cv2
from os import listdir
from random import randint
from random import random
import numpy as np
import mss
import pyautogui
import time
import sys
import src.env as env

from src.utils.debug import Debug
import yaml
import datetime
import webbrowser


VERSAO_SCRIPT = "2.00"

c = env.space
st = c['ship_settings']
th = c['threshold']
ot = c['optimization_settings']
gs = c['general_settings']
rw = c['rewards']

global login_attempts
login_attempts = 0

# Tempo entre ações
pyautogui.PAUSE = ot['time_click']

# Adiciona a media de recompensas de cada boss
rewards = []
rewards.append(0)
rewards.append(rw['boss_1'])
rewards.append(rw['boss_2'])
rewards.append(rw['boss_3'])
rewards.append(rw['boss_4'])
rewards.append(rw['boss_5'])
rewards.append(rw['boss_6'])
rewards.append(rw['boss_7'])
rewards.append(rw['boss_8'])
rewards.append(rw['boss_9'])
rewards.append(rw['boss_10'])
rewards.append(rw['boss_11'])
rewards.append(rw['boss_12'])
rewards.append(rw['boss_13'])
rewards.append(rw['boss_14'])
rewards.append(rw['boss_15'])
rewards.append(rw['boss_16'])
rewards.append(rw['boss_17'])
rewards.append(rw['boss_18'])
rewards.append(rw['boss_19'])
rewards.append(rw['boss_20'])

total_rewards = 0
ships_clicks = 0
cont_boss = 1
dbg = Debug('debug.log')

def addRandomness(n, randomn_factor_size=None):
    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n
    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    return int(randomized_n)

def moveToWithRandomness(x,y,t):
    pyautogui.moveTo(addRandomness(x,10),addRandomness(y,10),t+random()/2)

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def show(rectangles, img = None):
    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))
    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)

def clickBtn(img,name=None, timeout=3, threshold = th['default']):
    if not name is None:
        pass
    start = time.time()
    while(True):
        matches = positions(img, threshold=threshold)
        if(len(matches)==0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    pass

                return False
            continue
        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        moveToWithRandomness(pos_click_x,pos_click_y,ot['move_speed_mouse'])
        pyautogui.click()
        return True

def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        return sct_img[:,:,:3]

def positions(target, threshold=th['default'],img = None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]
    yloc, xloc = np.where(result >= threshold)
    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def processLogin():
    dbg.console('Starting Login', 'INFO', 'ambos')
    sys.stdout.flush()
    loginSPG()
    time.sleep(2)
    playSPG()

def scroll(clickAndDragAmount):
    flagScroll = positions(env.images_space['spg-flag-scrool'], th['commom'])    
    if (len(flagScroll) == 0):
        return
    x,y,w,h = flagScroll[len(flagScroll)-1]
    moveToWithRandomness(x,y,ot['move_speed_mouse'])
    pyautogui.dragRel(0,clickAndDragAmount,duration=1, button='left')


def loginSPG():
    global login_attempts    
    if login_attempts > 3:
        dbg.console('Too many login attempts, refreshing', 'ERROR', 'ambos')
        login_attempts = 0
        processLogin()
        return
    if clickBtn(env.images_space['connect-wallet'], name='connectWalletBtn', timeout = 10):
        dbg.console('Connect wallet button detected, logging in!', 'INFO', 'ambos')       
        login_attempts = login_attempts + 1
    if clickBtn(env.images_space['sign'], name='sign button', timeout=30):
        login_attempts = login_attempts + 1
        return
    if clickBtn(env.images_space['sign'], name='signBtn', timeout = 20):
        login_attempts = login_attempts + 1
    
def playSPG():
    if clickBtn(env.images_space['play'], name='okPlay', timeout=30):
        dbg.console('played SPG','INFO', 'ambos')   

def login():
    if len(positions(env.images_space['connect-wallet'], th['commom'])) > 0:        
        processLogin() 
        return True
    else:
        return False

def save_reward(type_value, average_value, result):   
    global total_rewards
    global cont_boss    
    first_write = False
    hora_rede_local = time.strftime("%H:%M:%S", time.localtime())
    total_rewards = total_rewards + result
    arquivo = open('rewards.log','a')
    str_log = '[' + str(format(datetime.date.today())) + '] [' + str(hora_rede_local) + '] [BOSS: ' + str(cont_boss) + '] [AVERAGE_VALUE:' + str(average_value) + '] [REWARD:' + str(type_value) + '] [RESULT:' + str(result) + '] [TOTAL:' +  str(round(total_rewards, 2)) + ']'
    arquivo.write(str_log + '\n')
    arquivo.close()

def look_rewards():
    global cont_boss
    value = 0     
    if st['get_rewards'] == True:
        if len(positions(env.images_space['rewards-x05'], th['rewards'])) > 0:
            result = rewards[cont_boss]*0.5
            dbg.console('Reward x0.5','INFO', 'ambos')
            save_reward('x0.5', rewards[cont_boss], result)
        elif len(positions(env.images_space['rewards-x1'], th['rewards'])) > 0:
            result = rewards[cont_boss]*1
            dbg.console('Reward x1','INFO', 'ambos')
            save_reward('x1', rewards[cont_boss], result)
        elif len(positions(env.images_space['rewards-x2'], th['rewards'])) > 0:  
            result = rewards[cont_boss]*2
            dbg.console('Reward x2','INFO', 'ambos')
            save_reward('x2', rewards[cont_boss], result)
        elif len(positions(env.images_space['rewards-x100'], th['rewards'])) > 0: 
            result = rewards[cont_boss]*100
            dbg.console('Reward x100','INFO', 'ambos')
            save_reward('x100', rewards[cont_boss], result)

def confirm():
    global cont_boss
    confirm_action = False
    if len(positions(env.images_space['lose'], th['commom'])) > 0 and cont_boss > 1:
        if clickBtn(env.images_space['confirm-lose'], name='okBtn', timeout=1, threshold  = th['confirm-end-boss']):
            time.sleep(2) 
            endFight()  
            confirm_action = True
    if len(positions(env.images_space['victory'], th['commom'])) > 0:  
        if len(positions(env.images_space['confirm-victory-1'], th['commom'])) > 0 or len(positions(env.images_space['confirm-victory-2'], th['commom'])) > 0:
            look_rewards()
            if clickBtn(env.images_space['confirm-victory-1'], name='okVicBtn', timeout=2) or clickBtn(env.images_space['confirm-victory-2'], name='okVicBtn', timeout=2):
                #dbg.console('Confirm victory encontrado','INFO', 'ambos')
                dbg.console('Boss ' + str(cont_boss) + " derrotado",'INFO', 'ambos')
                cont_boss = cont_boss + 1
                confirm_action = True
                if st['boss_surrender'] != 0:
                    if cont_boss == st['boss_surrender']:
                        dbg.console("Surrender boss: " + str(st['boss_surrender']), 'INFO', 'ambos')
                        time.sleep(3)
                        clickBtn(env.images_space['spg-surrender'])
                        time.sleep(1)
                        clickBtn(env.images_space['confirm-surrender'], name='okVicBtn', timeout=2)
                        cont_boss = 1
                        if st['select_spaceship_after_surrender'] == True:                 
                            time.sleep(6)
                            returnBase()
                if st['key_waves'] == True: 
                    if cont_boss == 9:
                        time.sleep(30) 
                        dbg.console("Boss 9, refresh ships", 'DEBUG', 'ambos')
                        clickBtn(env.images_space['ship'], threshold = th['commom'])
                    if cont_boss == 14:
                        time.sleep(30) 
                        dbg.console("Boss 14, refresh ships", 'DEBUG', 'ambos')
                        clickBtn(env.images_space['ship'], threshold = th['commom'])
                    if cont_boss == 19:
                        time.sleep(30) 
                        dbg.console("Boss 19, refresh ships", 'DEBUG', 'ambos')
                        clickBtn(env.images_space['ship'], threshold = th['commom'])
    return confirm_action

def removeSpaceships():
    global ships_clicks
    time.sleep(2)   
    retry_max = 20
    cnt_remove_ships = 0
    while True: 
        buttons = positions(env.images_space['spg-x'], threshold=th['hard'])
        buttonsNewOrder = []
        if len(buttons) > 0:
            index = len(buttons)
            while index > 0:
                index -= 1
                buttonsNewOrder.append(buttons[index])
            for (x, y, w, h) in buttonsNewOrder:
                moveToWithRandomness(x+(w/2),y+(h/2),ot['move_speed_mouse'])
                pyautogui.click()
                cnt_remove_ships = cnt_remove_ships + 1
                time.sleep(0.1) 
        if len(buttons) == 0 or cnt_remove_ships >= retry_max:
            ships_clicks = 0
            break
        if len(positions(env.images_space['close'], th['commom'])) > 0:    
            screen_close()
            break

def clickButtonsFight():
    global ships_clicks
    offset_x = 60
    offset_y = 35
    interval_buttons = 50
    inteval_common = 30

    if st['send_only_common'] == True:
        common_ships = positions(env.images_space['common-ship'], th['ships_rarity'])
        rare_ships = positions(env.images_space['rare-ship'], th['ships_rarity'])
        ships_to_work = []
        for bar in common_ships:
            ships_to_work.append(bar)
        for bar in rare_ships:
            ships_to_work.append(bar)                      
        #for (x_c, y_c, w_c, h_c) in ships_to_work:       
        #    dbg.console('Commum: ' + str(x_c) + ". Y: " + str(y_c), 'INFO', 'ambos')  
    
    if st['send_ships_full'] == True:        
        green_bars = positions(env.images_space['ship-full'], th['green_bar'])
        buttons = positions(env.images_space['spg-go-fight'], th['go-fight'])
        for (x, y, w, h) in green_bars:   
            for (x_b, y_b, w_b, h_b) in buttons:       
                if y_b < y+interval_buttons and y_b > y-interval_buttons:
                    #dbg.console('Have buttom', 'INFO', 'ambos') 
                    if st['send_only_common']:                        
                        for (x_c, y_c, w_c, h_c) in ships_to_work:       
                            if y_c < y+inteval_common and y_c > y-inteval_common:
                                dbg.console('Is commom', 'INFO', 'ambos')   
                                moveToWithRandomness(x+offset_x+(w/2),y+offset_y+(h/2),ot['move_speed_mouse'])
                                pyautogui.click()
                                ships_clicks = ships_clicks + 1        
                                if ships_clicks >= st['qtd_send_spaceships']:
                                    return -1
                    else:                        
                        moveToWithRandomness(x+offset_x+(w/2),y+offset_y+(h/2),ot['move_speed_mouse'])
                        pyautogui.click()
                        ships_clicks = ships_clicks + 1        
                        if ships_clicks >= st['qtd_send_spaceships']:
                            return -1
                        return 1            
        return len(green_bars)
    elif st['send_ships_full'] == False:
        buttons = positions(env.images_space['spg-go-fight'], th['go-fight'])
        count_ships_available = 0
        for (x, y, w, h) in buttons:
            if st['send_only_common']:     
                dbg.console('Bottons: ' + str(x) + ". Y: " + str(y), 'INFO', 'ambos')
                dbg.console('Range: <' + str(y+30) + " - " + str(y-30) + '>', 'INFO', 'ambos')                   
                for (x_c, y_c, w_c, h_c) in ships_to_work:       
                    #dbg.console('Commum: ' + str(x) + ". Y: " + str(y), 'INFO', 'ambos')
                    if y_c < y+10 and y_c > y-70:
                        #dbg.console('Is commom', 'INFO', 'ambos') 
                        count_ships_available = count_ships_available + 1  
                        moveToWithRandomness(x+(w/2),y+(h/2),ot['move_speed_mouse'])
                        pyautogui.click()
                        ships_clicks = ships_clicks + 1        
                        if ships_clicks >= st['qtd_send_spaceships']:
                            return -1
            else:
                moveToWithRandomness(x+(w/2),y+(h/2),0.1)
                #pyautogui.moveTo(x+(w/2),y+(h/2))
                pyautogui.click()
                ships_clicks = ships_clicks + 1        
                if ships_clicks >= st['qtd_send_spaceships']:
                    return -1
                return 1
        #return count_ships_available
        return len(buttons)

def refreshPage():
    pyautogui.hotkey('ctrl','f5')
    time.sleep(5) 

def screen_close():
    global cont_boss
    confirm_click = False
    if clickBtn(env.images_space['close'],timeout=1):
        dbg.console('Encontrou close', 'ERROR', 'ambos')        
        cont_boss = 1
        confirm_click = True
        refreshPage()
    if clickBtn(env.images_space['bt-ok'], timeout=1):
        dbg.console('Encontrou ok', 'ERROR', 'ambos')        
        cont_boss = 1
        confirm_click = True
    return confirm_click

def reloadSpacheship():
    global cont_boss
    if len(positions(env.images_space['spg-base'], th['commom'])) > 0 and len(positions(env.images_space['fight-boss'], th['hard']))  > 0:
        clickBtn(env.images_space['spg-base'], name='closeBtn', timeout=4)
        time.sleep(5)
        clickBtn(env.images_space['ship'], name='closeBtn', timeout=4, threshold = th['commom'])
        time.sleep(3)        
        cont_boss = 1

def ships_15_15():
    if len(positions(env.images_space['15-15-ships'], th['15-15-ships'])) > 0:
        dbg.console('Encontrou 15-15 tela naves', 'DEBUG', 'ambos')
        return True
    else:
        return False

def refreshSpaceships(qtd):
    global cont_boss
    global ships_clicks
    dbg.console('Refresh Spaceship to Fight', 'INFO', 'ambos')
    buttonsClicked = 1
    go_to_boss = False
    cda =  100
    aux_ships = 0
    
    if ot['set_filter_max_ammo'] == True and len(positions(env.images_space['fight-boss'], th['hard']))  > 0:
        if len(positions(env.images_space['max-ammo'], th['hard'])) == 0:
            dbg.console('Setando max ammo', 'INFO', 'ambos')
            if clickBtn(env.images_space['min-ammo'], timeout=1) or clickBtn(env.images_space['newest'], timeout=1):        
                time.sleep(0.2)
                clickBtn(env.images_space['max-ammo-sel'], timeout=4, threshold = th['hard'])
    empty_scrolls_attempts = 8
    if ships_clicks > 0:
        dbg.console('Quantidade ja selecionada:' + str(ships_clicks), 'DEBUG', 'ambos')
        if ships_clicks == st['qtd_send_spaceships']:
            empty_scrolls_attempts = 0
            goToFight()
    if ships_15_15():
        go_to_boss = True
        empty_scrolls_attempts = 0
    while(empty_scrolls_attempts >0):    
        is_repair()    
        aux_ships = ships_clicks
        buttonsClicked = clickButtonsFight()          
        if aux_ships != ships_clicks:
            dbg.console('Spaceships sent to Fight: ' + str(ships_clicks), 'INFO', 'ambos')   
        if buttonsClicked == 0:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
            scroll(-cda)
        elif buttonsClicked == -1:            
            dbg.console('Finish Click ships', 'INFO', 'ambos')
            empty_scrolls_attempts = 0   
        else:
            if buttonsClicked > 0:    
                time.sleep(0.1)            
                if ships_15_15():
                    go_to_boss = True
                    break
                continue   
        if len(positions(env.images_space['close'], th['commom'])) > 0:    
            screen_close()
            break     
        time.sleep(1.5)

    if ships_clicks == st['qtd_send_spaceships'] or cont_boss > 1 or go_to_boss == True:
        empty_scrolls_attempts = 0
        goToFight()
    else:
        reloadSpacheship()
        
def goToFight():
    global ships_clicks
    global cont_boss
    ships_clicks = 0 
    clickBtn(env.images_space['fight-boss'])
    time.sleep(4)
    if clickBtn(env.images_space['confirm-lose'], timeout = 4, threshold = th['commom']):
        cont_boss = 1

def endFight():
    global cont_boss    
    cont_boss = 1
    dbg.console("End fight", 'INFO', 'ambos')
    time.sleep(3) 
    returnBase()
    time.sleep(15) 
    if len(positions(env.images_space['fight-boss'], th['hard']))  > 0:
        if st['remove_ships'] == True:
            removeSpaceships()
        time.sleep(1) 
        refreshSpaceships(0)
    else:
        refreshPage()

def goToSpaceShips():
    if clickBtn(env.images_space['ship'], threshold = th['commom']):        
        global login_attempts
        login_attempts = 0

def returnBase():
    goToSpaceShips()

def zero_ships():
    if len(positions(env.images_space['spg-surrender'], th['commom'])  ) > 0:
        start = time.time()
        has_timed_out = False
        while(not has_timed_out):
            matches = positions(env.images_space['0-15'], th['0-15'])
            if(len(matches)==0):
                has_timed_out = time.time()-start > 1
                continue
            elif(len(matches)>0):
                dbg.console("Zero ships, volta spaceships", 'INFO', 'ambos')
                time.sleep(1)
                clickBtn(env.images_space['ship'],timeout = 5, threshold = th['commom'])
                return True
    return False  

def spaceships(): 
    if len(positions(env.images_space['fight-boss'], th['hard']))  > 0:
        if st['remove_ships'] == True:
            removeSpaceships()
        refreshSpaceships(0)
        return True
    else:
        return False

def is_repair():
    if len(positions(env.images_space['repair'], th['commom']))  > 0:
        if clickBtn(env.images_space['btn-repair'],timeout = 5, threshold = th['commom']):
            clickBtn(env.images_space['btn-yes'],timeout = 5, threshold = th['commom'])
            return True
    return False