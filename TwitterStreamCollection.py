import MySQLdb
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

#Make sure that you install "tweepy" library before running this program.
#Replace all the below values with the respective fields.

conn = MySQLdb.connect("YOUR_SQL_SERVER", "YOUR_USERNAME", "YOUR_PASSWORD", "YOUR_DATABASE_NAME")

c = conn.cursor()

#Insert your consumer key, consumer secret key, access token, access token secret values in the following fields.
ckey = ''
csecret = ''
atoken = ''
asecret = ''

class listener(StreamListener):
    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        username = all_data["user"]["screen_name"]
        c.execute("INSERT INTO tweetAna (time, username, tweet) VALUES (%s,%s,%s)",
                   (time.time(), username, tweet))
        conn.commit()
        print((username, tweet))
        return True
        
    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

#The keyword which you want to use as the filter goes in the place of '?'
twitterStream.filter(track = ["?"])
