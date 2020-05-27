import os
import random

import pygame as pg
from pygame.locals import *

#initialize pygame
from pygame.constants import QUIT, KEYDOWN, K_ESCAPE, K_q

pg.init()
#initialize clock
clock = pg.time.Clock()

#Toolkit
def sound(correct = None):
    if correct:
        pg.mixer.Sound(os.path.join("touch_reqs", "chime.wav")).play()

def pellet():
    if os.path.isfile('c:/pellet.exe'):
        os.system('c:/pellet.exe')
    else:
        print('Pellet')

def timer(length_of_time = None):
    time1 = pg.time.get_ticks()
    while time1 >= (pg.time.get_ticks() - length_of_time):
        quit_esc_q()
        clock.tick(60)

def quit_esc_q():
    for event in pg.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and (event.key in (K_ESCAPE, K_q))):
            raise SystemExit

def write_ln(filename = None, data = '', csv = True):
    '''
    :param filename: filepath to datafile
    :param data: list of data to be output
    :param csv: comma-delimited if True, tab if false.
    '''
    with open(filename, 'a+') as data_file:
        if csv:
            data_file.write(', '.join(map(str, data)) + '\n')
        else:
            data_file.write('\t'.join(map(str, data)) + '\n')

def get_params(var_names = None):
    '''
    read in all even lines from parameters.txt. Takes a list of variable names
    as argument and stores them with their values. Returns a dictionary
    '''

    params = {}
    with open('/home/pi/Desktop/PyCharm/parameters_train', 'r') as txt:
        for line_num, line in enumerate(txt):
            if line_num % 2 == 1:
                j = line_num // 2
                params[var_names[j]] = line.strip('\r\n')
        for key, val in params.items():
            exec ('params[key] = %s' % val)
        return params

#Screen
class Screen(object):
    def __init__(self, size = (800, 600), col = Color('black'), fullscreen = True):
        '''pygame screen on which to draw stimuli
        :param size: screen resolution in pixels
        :param col: screen background color
        :param fullscreen: fullscreen if True, not fullscreen
        '''
        self.rect = pg.Rect((0, 0), size)
        self.bg = pg.Surface(size)
        self.bg.fill(col)
        if fullscreen:
            self.fg = pg.display.set_mode(size, (NOFRAME and FULLSCREEN))
        else:
            self.fg = pg.display.set_mode(size)
    def refresh(self, clear_screen = None):
        '''blit background to screen and update display
        :param clear_screen: blit bg to fg if true, update and blit fg to bg if true or false
        '''
        if clear_screen:
            self.fg.blit(self.bg, (0, 0))
        pg.display.update()
        self.fg.blit(self.bg, (0, 0))

#Procedure
class TouchTrainProcedure(object):
    def __init__(self, screen = None):

        self.trial = 0
        self.screen = screen

        self.on_start_screen = None
        self.on_transition_screen = None

        self.stimuli_this_trial = None
        self.stimuli_rect = pg.Rect(random.randint(0, 480), random.randint(0, 480), 100, 100)
        #self.random_placement = 
        self.RT_start = None

    def new_trial(self):
        self.trial += 1
        self.on_start_screen = True
        self.on_reward_screen = False
        #self.screen.refresh(clear_screen=True)
        self.screen.fg.fill(Color('black'))
        pg.draw.rect(self.screen.fg,(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), self.stimuli_rect)
        self.screen.bg.blit(self.screen.fg, (0, 0))

    def start_screen(self):
        pos = pg.mouse.get_pos()
        pressed1, pressed2, pressed3 = pg.mouse.get_pressed()
        if self.stimuli_rect.collidepoint(pos) and pressed1:
            self.transition_to_reward_screen()

    def transition_to_reward_screen(self):
            self.on_start_screen = False
            self.on_reward_screen = True
            self.RT_start = pg.time.get_ticks()

    def reward_screen(self, correct = None):
        write_ln(filepath_to_data, [param_subject, param_date, self.trial, pg.time.get_ticks() - self.RT_start])
        print("clicked on square")
        sound(correct = True)
        self.screen.bg.fill(pg.Color('slateblue'))
        self.screen.refresh(clear_screen=True)
        pellet()
        timer(param_ITI)

        self.new_trial()

#Setup
globals().update(get_params(var_names=['param_subject',
                                       'param_fullscreen',
                                       'param_date',
                                       'param_ITI'
                                       ]))

touch_train_screen = Screen(size=(800,600), col=pg.Color('black'),
                            fullscreen=param_fullscreen)

filepath_to_data = os.path.join('/home/pi/Desktop/PyCharm', 'data', param_subject + '_' + '_TouchTrain.csv')
write_ln(filename=filepath_to_data, data=['subject', 'param_date', 'trial', 'RT'])
experiment = TouchTrainProcedure(screen=touch_train_screen)
experiment.new_trial()

#Gameloop

done = False
while not done:
    quit_esc_q()
    touch_train_screen.refresh(clear_screen=False)

    if experiment.on_start_screen:
        experiment.start_screen()
    elif experiment.on_reward_screen:
        experiment.reward_screen()

    clock.tick(30)