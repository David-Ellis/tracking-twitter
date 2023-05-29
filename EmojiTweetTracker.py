import snscrape.modules.twitter as sntwitter
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import itertools

class TweetTracker:
    def __init__(self, querys, img_files, dy = 0.05):
        self.querys = querys
        self.main_query = ' OR '.join(querys)
        self.n_queries = len(querys)
        
        self.y_pos = [[] for i in range(self.n_queries)]
        self.phase = [[] for i in range(self.n_queries)]
        self.tweet_count = [[] for i in range(self.n_queries)]
        
        self.dy = dy
        self.x0 = np.arange(self.n_queries)
        self.images = [plt.imread(img_file_i) for img_file_i in img_files]
        self.phase0 = 2*np.pi*np.random.rand(self.n_queries)
        
        
        self.index = 0
        
        self.last_id = next(sntwitter.TwitterSearchScraper(self.main_query).get_items()).id
        
    def get_latest(self, check_last = 50):
        tweets = sntwitter.TwitterSearchScraper(self.main_query).get_items()
        tweet_contents = []
        
        next_id = ""
        
        count = 0
        while next_id != self.last_id and count < 10:
           # print("in this loop")
            tweet = next(tweets)
            next_id = tweet.id
            if count == 0:
                first_new_id = next_id
            count += 1
            tweet_contents.append(tweet.rawContent)
        self.last_id = first_new_id    

        #print(tweet_contents)
        for j, query in enumerate(self.querys):
            new_tweets = len(list(filter(lambda content: query in content, tweet_contents)))
            self.tweet_count[j].append(new_tweets)

                 
            self.y_pos[j].append(0.05)
            self.phase[j].append(self.index + self.phase0[j])
        self.index += 1
        # Reset time mark
        #self.t0 = datetime.datetime.now()
    def plot(self, ax):
        for j in range(self.n_queries):
            for i in range(len(self.y_pos[j])):
                if self.tweet_count[j][i] > 0 and self.y_pos[j][i] <= 1:
                    x = self.x0[j] + self.y_pos[j][i]/6 * np.sin(self.phase[j][i])
                    image_box = OffsetImage(self.images[j], 
                                            zoom=0.05*np.sqrt(self.tweet_count[j][i]),
                                            alpha = 1-self.y_pos[j][i])
                    
                    ab = AnnotationBbox(image_box, (x, self.y_pos[j][i]), 
                                        frameon=False, alpha=0.2)
                    ax.add_artist(ab)
    
            self.y_pos[j] = [y_i + self.dy for y_i in self.y_pos[j]]
        #self.y_pos = list(filter(lambda y_i: y_i <= 1, self.y_pos))
    
def reset_canvas(ax, x_pos, x_lab):
    ax.cla()
    ax.set_ylim([0, 1])
    ax.set_xlim([min(x_pos) - 1, max(x_pos) + 1])
    ax.set_yticks([])
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x_lab, fontsize=20)
    ax.set_title("Tweet Keyword Tracker", fontsize=20)
    
    return ax
    
query = "cat"

plt.close("all")

fig = plt.figure(figsize = (6, 5))
ax = fig.add_subplot(111)
ax.set_ylim([0, 1])

last_id = ""

tracker = TweetTracker(["cat", "dog", "python"], 
                   ["images/cat.png","images/dog.png","images/snake.png"])

while True: 
    reset_canvas(ax, 
                 [0, 1, 2], 
                 ["Cat", "Dog", "Python"])
    
    tracker.get_latest()    

    #print("looping")
    tracker.plot(ax)

    plt.pause(0.01)

    
    