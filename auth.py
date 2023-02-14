import tweepy
import json

twitter_api_data_path = "D:/TereBin/coding/TrB_AutoTweet/data/twitter_api_data.txt"
twitter_data_txt = open(twitter_api_data_path, 'r')
twitter_data = twitter_data_txt.read().splitlines()
api_key = twitter_data[0]
api_secret = twitter_data[1]
twitter_data_txt.close()

user_data_path = "D:/TereBin/coding/TrB_AutoTweet/data/user_data.json"
user_dict = json.load(
        open(user_data_path, 'r', encoding='utf-8'))  # readable dict

oauth1_user_handler = tweepy.OAuth1UserHandler(api_key, api_secret, callback='oob')
print(oauth1_user_handler.get_authorization_url(signin_with_twitter=True))

PIN = input("Input PIN: ")
access_token, access_secret = oauth1_user_handler.get_access_token(PIN)

twitter_id = input("트위터 아이디 : ")
tweet = input("문장 : ")
duration = input("시간 : ")
input_image = input("이미지를 넣으려면 Y : ")

num = str(len(user_dict))
user_dict[num] = {}
user_dict[num]["1_twitter_id"] = twitter_id
user_dict[num]["2_tweet"] = tweet
user_dict[num]["3_access_token"] = access_token
user_dict[num]["4_access_secret"] = access_secret
user_dict[num]["5_duration"] = duration
if input_image == "Y" or "y":
    user_dict[num]["6_img"] = ""
else:
    user_dict[num]["6_img"] = ""


with open(user_data_path, 'w', encoding='utf-8') as file:
    json.dump(user_dict, file, indent='\t')
