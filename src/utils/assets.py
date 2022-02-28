from cv2 import cv2
from os import listdir
import src.env as env
from src.utils import string
from src.utils.image import resizeImageForScale
from time import sleep

def loadHeroesImagesToHome():
    file_names = listdir('./targets/heroes-to-send-home')
    heroes = []
    for file in file_names:
        path = './targets/heroes-to-send-home/' + file
        # TODO: add scale?
        hero_image = cv2.imread(path)
        heroes.append(hero_image)

    print('>>---> %d heroes that should be sent home loaded' % len(heroes))
    return heroes

def loadImages():
    print('>>---> Loading Images BombCrypto')

    file_names = listdir('./targets/')
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        target_name = string.removeSuffix(file, '.png')
        temp_image = cv2.imread(path)
        if env.scale_image['enable']:
            targets[target_name] = resizeImageForScale(temp_image, env.scale_image['percent'])
        else:
            targets[target_name] = temp_image

    return targets

    
def loadImagesSpace(resolution = 1):
    if resolution == 1:
        dir_path = './img_compare/1366x768/'
    elif resolution == 2:
        dir_path ='./img_compare/1680x1050/'
    elif resolution == 3:
        dir_path ='./img_compare/1920x1080/'    
    file_names = listdir(dir_path)
    targets = {}
    for file in file_names:
        path = dir_path[2:] + file
        targets[string.removeSuffix(file, '.png')] = cv2.imread(path)
    return targets