#!/usr/bin/python3
# import modules
import praw
import numpy as np

# login
reddit = praw.Reddit(client_id='-iZuukmTrkqDfQ',
                     client_secret='UD-eEKKtmvpljRuxwrOy2gSwFUs',
                     password='0894975975',
                     user_agent='test-script by /u/Jacob975',
                     username='Jacob975')
# print my user name
print(reddit.user.me())
subreddit  = reddit.subreddit("showerthoughts")
top_submissions = subreddit.hot(limit=100)

upvotes = []
downvotes = []
contents = []
for sub in top_submissions:
    print(sub.permalink)
    ratio = reddit.submission(url = sub.permalink).upvote_ratio
    ups = int(round((ratio*sub.score)/(2*ratio - 1)) if ratio != 0.5 else round(sub.score/2))
    upvotes.append(ups)
    downvotes.append(ups - sub.score)
    contents.append(sub.title)
votes = np.array( [ upvotes, downvotes] ).T

# print some submissions as examples
print(upvotes)
print(downvotes)
print(contents)
'''
for i in range(5):
    print("### Comments ###\n{0}".format(contents[i]))
    print("upvote: {0}, downvote:{1}\n".format(upvotes[i], downvotes[i]))
'''
