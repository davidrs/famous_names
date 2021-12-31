

import pandas as pd
import json
from collections import Counter

import random
from time import sleep
from pywebio.input import *
from pywebio.output import *

from pywebio import start_server
import datetime

def load_data():
    credits = pd.read_csv('tmdb_5000_credits.csv')
    movies = pd.read_csv('tmdb_5000_movies.csv')
    
    actor_names = []
    actor_movies = {}
    for i, c in credits.iterrows():
        credit = json.loads(c['cast'])
        for p in credit:
            actor_names.append(p.get('name',None))
            if p.get('name',None) not in actor_movies:
                actor_movies[p.get('name',None)]=[]
            actor_movies[p.get('name',None)].append(c['title'])

    return actor_names, actor_movies




def shuffle_word(word):
    word=list(word.lower())
    # random.shuffle(word)
    word.sort()
    return ''.join([w for w in word if w != ' '])
    

def play_round(name, actor_movies, easy=False):
    points=0
    shfl = shuffle_word(name)
    if not easy:
        shfl=shfl.lower()

    put_text("Acronym: "+ shfl)
    put_text('In the movie:'+ random.sample(actor_movies[name],1)[0])
    ans = ""
    while True:
        ans = input('\nType "h" for a hint, "y" for the answer, or type a guess:')
        if ans.lower() in ['h','hint']:
            put_text('In the movie:', random.sample(actor_movies[name],1)[0])
            points-=1
        if ans.lower() in ['y','yes']:
            put_text(name)
            return 0
        if ans.lower()==name.lower():
            put_text('you won!')
            points+=5
            return points
        # clear_output(wait=True)
        
    
def play_game():
    actor_names, actor_movies = load_data()
    c = Counter(actor_names)
    print ("most common:",c.most_common(10))

    names = [x[0] for x in c.most_common(90)]


    now = datetime.datetime.now()
    random.seed(now.day*25*60 + now.hour*60 + int(now.minute/10))
    # print(now.year, now.month, now.day, now.hour, now.minute, now.second)
    random.shuffle(names)

    easy=False
    points=0
        
    for i,n in enumerate(names):
        points += play_round(n, actor_movies, easy)
        put_text('Score:', points)
        put_text('Round:', i)
        sleep(3)
        clear()
        # clear_output()

    # input("What's your name?")

if __name__ == '__main__':
    start_server(play_game, port=8000)