import time
import sys
import os

if os.name == 'nt':
    import pygetwindow as pygetwindow

if os.name == 'posix':
    import pygetwindowmp as pygetwindow

from src.utils.number import addRandomness
import src.bot.logger as Log
import src.env as env
import src.bot.heroes as Heroes
import src.bot.login as Auth
import src.bot.action as Action
import src.bot.spacecrypto as Space
from src.utils.config import loadConfigsFromFile

global space
global cfg
cfg = loadConfigsFromFile()
space = cfg['space']

def runMultiAccount():
    intervals = env.cfg['time_intervals']
    time.sleep(2)

    windows = []
    titlesBomb = []
    titlesSpace = []

    Log.logger('🆗 Start')
    Log.logger('Searching for windows with contains ', color='yellow')

    title_bomb = env.multi_account_same_monitor['window_contains_title']
    title_space = 'Space Crypto -'

    alltitles = pygetwindow.getAllTitles()

    
    for t in alltitles:
        if title_bomb in t:
            titlesBomb.append(t)
        if title_space in t:
            titlesSpace.append(t)

    titlesBomb = set(titlesBomb)
    titlesSpace = set(titlesSpace)
    for i in titlesSpace:
        for w in pygetwindow.getWindowsWithTitle(i):
            windows.append({
                "window": w,
                "login" : 0,
                "title": 'space',
                "close" : 0,
                "login" : 0,
                "refresh_page": time.time(),

                "check_close" : 5,  
                "check_login" : 1,
                "check_refresh_page": env.space['ship_settings']['refresh_page'],
            })
    for i in titlesBomb:
        for w in pygetwindow.getWindowsWithTitle(i):
            windows.append({
                "window": w,
                "login" : 0,
                "heroes" : 0,
                "new_map" : 0,
                "refresh_heroes" : 0,
                'title': 'bomb'
            })
    

    Log.logger('Found {} window(s):'.format(len(windows)), color='cyan')
    for index, last in enumerate(windows):
        Log.logger('{} -> {}'.format(index+1, last['window'].title), color='cyan')

    if len(windows) == 0:
        Log.logger('Exiting because dont have windows contains "{}" title', color='red')
        exit()

    while True:
        now = time.time()
        action_found = False
        
        for last in windows:
            env.window_object = last["window"]
            Log.logger('Client active window: {}'.format(last['window'].title), color='green')
            time.sleep(5)
            
            if last["title"] == "bomb":
                if now - last["login"] > addRandomness(intervals['check_for_login'] * 60):
                    Action.activeWindow()
                    sys.stdout.flush()
                    last["login"] = now
                    Auth.login()

                if now - last["heroes"] > addRandomness(intervals['send_heroes_for_work'] * 60):
                    Action.activeWindow()
                    last["heroes"] = now
                    Heroes.refreshHeroes()

                if now - last["new_map"] > intervals['check_for_new_map_button']:
                    Action.activeWindow()
                    last["new_map"] = now
                    Action.goToNextMap()

                if now - last["refresh_heroes"] > addRandomness( intervals['refresh_heroes_positions'] * 60):
                    Action.activeWindow()
                    last["refresh_heroes"] = now
                    Action.refreshHeroesPositions()

                Log.logger(None, progress_indicator=True)
                sys.stdout.flush()

                time.sleep(1)

            if last["title"] == "space":

                actual_time = now
   
                Log.logger('Qtd naves total: ' + str(env.space['ship_settings']['empty_qtd_spaceships']), color='cyan')
                Log.logger('Qtd naves enviar: ' + str(env.space['ship_settings']['qtd_send_spaceships']), color='cyan')
                
                Action.activeWindow()
                
                if actual_time - last["login"] > addRandomness(last['check_login'] * 60):                    
                    Action.activeWindow()
                    last["login"] = actual_time
                    if Space.login():
                        action_found = False 
                    else:
                        action_found = False   
                if Space.spaceships():
                    action_found = True 
                if Space.confirm():
                    action_found = True 
                if Space.zero_ships():
                    action_found = True               
                if actual_time - last["close"] > last['check_close']:
                    last["close"] = actual_time
                    if Space.screen_close():
                        action_found = True
                if action_found == False:
                    print('Nenhuma acao encontrada')
                    if (actual_time - last['refresh_page']) > last['check_refresh_page']:
                        Action.activeWindow()

                        print('Atualização da Página')
                        last['refresh_page'] = actual_time      
                        Space.refreshPage()  
                else:
                    last['refresh_page'] = actual_time

                Log.logger(None, progress_indicator=True)
                sys.stdout.flush()

                time.sleep(1)