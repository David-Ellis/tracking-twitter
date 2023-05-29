import snscrape.modules.twitter as sntwitter
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
import numpy as np

class TweetTracker:
    def __init__(self, query, img_file, x0 = 0, dy = 0.05):
        self.query = query
        self.y_pos = []
        self.tweet_count = []
        self.last_id = ""
        self.dy = dy
        self.x0 = x0
        self.image = plt.imread(img_file)
        self.phase0 = 2*np.pi*np.random.rand()
        self.phase = []
        
        self.index = 0
        
        scraper = sntwitter.TwitterSearchScraper(self.query)
        for tweet in scraper.get_items():
            self.last_id = tweet.id
            break
        
    def get_latest(self):
        scraper = sntwitter.TwitterSearchScraper(self.query)
        count = 0
        for i, tweet in enumerate(scraper.get_items()):
            if i == 0:
                first_id = tweet.id
                
            if tweet.id == self.last_id or count == 10:
                self.last_id = first_id
                break
            else:
                count += 1
                    
        #print(count)
        self.tweet_count.append(count)
        self.y_pos.append(0.05)
        self.phase.append(i + self.phase0)
    def plot(self, ax):
        for i in range(len(self.y_pos)):
            if self.tweet_count[i] > 0 and self.y_pos[i] <= 1:
                x = self.x0 + self.y_pos[i]/6 * np.sin(self.phase[i])
                
                image_box = OffsetImage(self.image, 
                                        zoom=0.05*np.sqrt(self.tweet_count[i]),
                                        alpha = 1-self.y_pos[i])
                ab = AnnotationBbox(image_box, (x, self.y_pos[i]), 
                                    frameon=False, alpha=0.2)
                ax.add_artist(ab)

        self.y_pos = [y_i + self.dy for y_i in self.y_pos]
        #self.y_pos = list(filter(lambda y_i: y_i <= 1, self.y_pos))
    
def reset_canvas(ax, x_pos, x_lab):
    ax.cla()
    ax.set_ylim([0, 1])
    ax.set_xlim([0, 1])
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

cat = TweetTracker("cat", "images/cat.png", x0 = 0.2)
dog = TweetTracker("dog", "images/dog.png", x0 = 0.5)
python = TweetTracker("snake", "images/snake.png", x0 = 0.8)

while True: 
    reset_canvas(ax, 
                 [0.2, 0.5, 0.8], 
                 ["Cat", "Dog", "Python"])
    
    cat.get_latest()    
    dog.get_latest()
    python.get_latest()
    #print("looping")
    cat.plot(ax)
    dog.plot(ax)
    python.plot(ax)
    
    plt.pause(0.01)

    
    