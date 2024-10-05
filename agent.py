import numpy as np
import random
from game import Game

ACTIONS = [0, 1, 2, 3, 4, 5]

def rnd_policy(s):
    actions = []
    for a in ACTIONS:
        if s[0, 1, a] != 0:
            actions.append(a)
            
    return random.choice(actions)

def max_play_policy(s):
    actions = []
    for a in ACTIONS:
        if s[0, 1, a] != 0 and s[0, 1, a] == (6-a):
            actions.append(a)
            
    if actions:
        return actions[-1]
    return rnd_policy(s)

def always_gain_policy(s):
    actions = []
    for a in ACTIONS:
        if s[0, 1, a] >= 6-a:
            actions.append(a)
            
    if actions:
        return random.choice(actions)
    return rnd_policy(s)

def capture_policy(s):
    actions = []
    for a in ACTIONS:
        if s[0, 1, a] != 0 and (s[0, 1, a] + a) % 12 < 6 and s[0, 1, (s[0, 1, a] + a)%12] == 0 and s[0, 0, 5-(s[0, 1, a] + a)%12] != 0:
            actions.append(a)
            
    if actions:
        actions.sort(key=lambda a: s[0, 0, 5-(s[0, 1, a] + a)%12])
        return actions[-1]
    return rnd_policy(s)

def united_policy(s):
    actions = []
    for a in ACTIONS:
        if s[0, 1, a] != 0 and s[0, 1, a] == (6-a):
            actions.append(a)
            
    if actions:
        return actions[-1]
    
    for a in ACTIONS:
        if s[0, 1, a] != 0 and (s[0, 1, a] + a) % 12 < 6 and s[0, 1, (s[0, 1, a] + a)%12] == 0 and s[0, 0, 5-(s[0, 1, a] + a)%12] != 0:
            actions.append(a)
            
    if actions:
        actions.sort(key=lambda a: s[0, 0, 5-(s[0, 1, a] + a)%12])
        return actions[-1]
    
    for a in ACTIONS:
        if s[0, 1, a] >= 6-a:
            actions.append(a)
            
    if actions:
        return random.choice(actions)
    return rnd_policy(s)
    
    
def united_policy_2(s):
    actions = []
    for a in ACTIONS:
        if s[0, 1, a] != 0 and (s[0, 1, a] + a) % 12 < 6 and s[0, 1, (s[0, 1, a] + a)%12] == 0 and s[0, 0, 5-(s[0, 1, a] + a)%12] != 0:
            actions.append(a)
            
    if actions:
        actions.sort(key=lambda a: s[0, 0, 5-(s[0, 1, a] + a)%12])
        return actions[-1]
    
    for a in ACTIONS:
        if s[0, 1, a] != 0 and s[0, 1, a] == (6-a):
            actions.append(a)
            
    if actions:
        return actions[-1]
    
    for a in ACTIONS:
        if s[0, 1, a] >= 6-a:
            actions.append(a)
            
    if actions:
        return random.choice(actions)
    return rnd_policy(s)
    
if __name__ == "__main__":
    game = Game()
    #game.play_ai(max_play_policy)
    #game.play_ai(always_gain_policy)
    #game.play_ai(capture_policy)
    game.play_agents(united_policy_2, united_policy)
    
    
            
    
        
        