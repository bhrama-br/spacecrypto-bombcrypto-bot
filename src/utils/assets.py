from cv2 import cv2
from os import listdir
import src.env as env
from src.utils import string
from src.utils.image import resizeImageForScale

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

    
def loadImagesSpace(resize):
    print('>>---> Loading Images SpaceCrypto')
    if resize:
        file_names = listdir('./img_compare/')
    else:
        file_names = listdir('./img_compare/1600x900/')
    targets = {}
    for file in file_names:
        if resize:
            path = 'img_compare/' + file
        else:
            path = 'img_compare/1600x900/' + file
        
        target_name = string.removeSuffix(file, '.png')
        target_name = string.removeSuffix(target_name, '.PNG')
        temp_image = cv2.imread(path)
        targets[target_name] = temp_image
    return targets