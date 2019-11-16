#! /Users/mcwa/Marc-perso/Python/virt
#encoding:utf-8

import logging
import threading
import datetime as d
import time

class Vanne():
    def __init__(self, nom):
        self.nom = nom
        self.mode = 'off'
        self.sortie = self.check_output()
        self.prog = {}
        self.actif = {}

    def change_mode(self, mode):
        """modifie le mode de Vanne ('on, 'off', prog')"""
        if mode in ['on', 'off', 'prog']:
            logging.debug('change mode de {} à {}'.format(self.mode, mode))
            self.mode = mode
            self.sortie = self.check_output()
        else:
            logging.debug("Attention:{} n'est pas un mode reconnu".format(mode))

    def check_output(self):
        if self.mode == 'on':
            return 'open'
        if self.mode == 'off':
            return 'closed'
        if self.mode == 'prog':
            return 'undefined'

    def __str__(self):
        program=[]
        for elem in self.prog:
            program.append(self.prog[elem].nom)
        p_actif=[]
        for elem in self.actif:
            p_actif.append(elem)
        return "VANNE {}: mode = {} / sortie = {} // progs= {} / actif= {}".format(self.nom ,self.mode, self.sortie, program, p_actif)

    def add_p(self, prog):
        self.prog.setdefault(prog.nom, prog)

    def del_p(self, prog):
        if prog == 'all':
            self.prog.clear()
        else: 
            if prog in self.prog:
                del self.prog[prog]

    def active_p(self, prog):
        if prog == 'all':
            for elem in self.prog['nom']:
                self.actif.setdefault(elem, True)
        elif prog in self.prog.keys():
           
            self.actif.setdefault(prog, True)

class Program():
    week = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
    def __init__(self,nom):
        self.nom = nom
        self.start = d.time(0, 0)
        self.stop = d.time(0, 0)
        self.jours = {x: False for x in Program.week}
        self.valid = False
        self.v_message = 'pas configuré'
        
    def __str__(self):
        jours = [x for x in self.jours if self.jours[x] ]
        if self.valid == True:
            valide = 'programme valide'
        else:
            valide = 'programme non valide: {}'.format(self.v_message)
        return 'PROGRAM {} : start = {} / stop = {} / jours = {}\n             {}'.format(self.nom, self.start, self.stop, jours, valide)
    
    def validator(self):
        print('validator')
        liste_j = [j for j in self.jours.keys() if self.jours[j]]
        if self.stop < self.start:
            self.valid = False
            self.v_message = 'stop < start'
        elif len(liste_j) == 0:
            self.valid = False
            self.v_message = 'pas de jours sélectionés'
        else:
            self.v_message = 'prog valide'
            self.valid = True

    def modif(self, valeur, *args):
        if valeur == 'start':
            h,m = args
            self.start=d.time(h, m)
            self.validator()
        if valeur == 'stop':
            h,m = args
            self.stop=d.time(h, m)
            self.validator()
        if valeur == 'jours':
            op, l_jours = args
            if op == '+':
                value = True
            elif op == '-':
                value = False
            else:
                return
            for jour in l_jours:
                self.jours[jour] = value
            self.validator()
     
def v_survey(vanne):
    while True:
        print("{}:{}".format(vanne.nom, vanne.sortie))
        time.sleep(1)
def v_mod(vanne):
    while True:
        mode = input('mode ({})?'.format(vanne.nom))
        vanne.change_mode(mode) 


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s', level='DEBUG')
    v1 = Vanne('v1')
    v2 = Vanne('v2')
    p1 = Program('p1')
    p2 = Program('p2')
    p3 = Program('p3')
    v1.add_p(p1)
    v1.add_p(p2)
    v1.add_p(p3)
    print(v1)
    p1.modif('start',21,55)
    v1.active_p('p1')
    v1.active_p('p2')
    print(v1)
    """
    print(p1)
    p1.modif('stop',23,55)
    print(p1)
    p1.modif('jours','+',['lundi', 'mardi'])
    print(p1)
    p1.modif('jours','-',['lundi', 'mardi'])
    print(p1)
    print(v1)
    survey_v1 = threading.Thread(target=v_survey, args=(v1,))
    survey_v2 = threading.Thread(target=v_survey, args=(v2,))
    modif_v1 = threading.Thread(target=v_mod, args=(v1,))
    survey_v1.start()
    survey_v2.start()
    modif_v1.start()
    """
    print('fini...')

