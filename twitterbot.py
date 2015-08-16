# -*- coding: utf-8 -*-
import ConfigParser
import json

from tweepy.streaming import StreamListener
from tweepy import *

config = ConfigParser.ConfigParser()
config.read('.twitter')

consumer_key = config.get('apikey', 'key')
consumer_secret = config.get('apikey', 'secret')
access_token = config.get('token', 'token')
access_token_secret = config.get('token', 'secret')
stream_rule = config.get('app', 'rule')
account_screen_name = config.get('app', 'account_screen_name').lower() 
account_user_id = config.get('app', 'account_user_id')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterApi = API(auth)
global  reply_language
class ReplyToTweet(StreamListener):

    def on_data(self, data):
        print data
        tweet = json.loads(data.strip())
        
        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == account_user_id

        if retweeted is not None and not retweeted and not from_self:

            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            language = tweet.get('user',{}).get('lang')
            tweetText = ReplyToTweet.reply_language(self,language)
            replyText = tweetText + ' ' + '@' + screenName

            #check if repsonse is over 140 char
            if len(replyText) > 140:
                replyText = replyText[0:137] + '...'

            print('Tweet ID: ' + tweetId)
            print('From: ' + screenName)
            print('Tweet Text: ' + tweetText)
            print('Reply Text: ' + replyText)

            # If rate limited, the status posts should be queued up and sent on an interval
            try:
                twitterApi.update_status(status=replyText)
            except TweepError as e:
                if e.message[0]['code'] != 187:
                    raise e
                else:
                    pass
                

    def on_error(self, status):
        print status
        
    def reply_language(self,lang):
         if lang == 'de':
            return u'Du weisst gar nichts,'
         elif lang == 'fr':
            return u'To ne sais rien,'
         elif lang == 'sp':
            return u'Tu no sabes nada,'
         elif lang == 'jp':
            return u'何も 知らない'
         else:
            return u'You know nothing,'


if __name__ == '__main__':
    streamListener = ReplyToTweet()
    twitterStream = Stream(auth, streamListener)
    twitterStream.userstream(_with='user')
