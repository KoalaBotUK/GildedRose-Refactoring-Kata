import requests
import json

class TwitterTools:

  def __init__(self, token, key, secret):
    self.twitter_token = token
    self.twitter_key = key
    self.twitter_secret = secret
    self.HEADERS = {
      "Authorization": f"Bearer {token}"
    }
    
  def get_twitter_id(self, name):
    """Gets the id of a twitter user
    :param name: username of twitter user
    :return: twitter id
    """
    r = requests.request("GET", f'https://api.twitter.com/2/users/by/username/{name}', headers = self.HEADERS)
    jsonvariables =json.loads(r.text)
    # print(jsonvariables["data"]["id"])
    # print(r.text)
    return jsonvariables["data"]["id"]

  def get_recent_tweet(self, name):
    """ Returns the latest tweet uploaded
    :param name: username of twitter user
    :return: text content of tweet
    """
    user_id = self.get_twitter_id(name)
    r = requests.request("GET", f'https://api.twitter.com/1.1/statuses/user_timeline.json?user_id={user_id}&count=1&tweet_mode=extended', headers = self.HEADERS)
    jsonvariables =json.loads(r.text)
    return jsonvariables[0]

  def get_profile_image(self, name):
    user_id = self.get_twitter_id(name)
    r = requests.request("GET", f"https://api.twitter.com/1.1/users/show.json?user_id={user_id}", headers = self.HEADERS)
    jsonvariables =json.loads(r.text)
    # print(jsonvariables["profile_image_url_https"])
    return(jsonvariables["profile_image_url_https"])

  def post_new_status(self, *text):
    status = ' '.join(text)
    r = requests.post("https://api.twitter.com/1.1/statuses/update.json", headers = self.HEADERS, params = {"status": str(status),})
    print(r)
    print(r.status_code)
    print(f"POSTED {status}")
    return r.status_code
