import time
from time import localtime
import json
import tweepy

twitter_api_data_path = "data/twitter_api_data.txt"
user_data_path = "data/user_data.json"
err_log_path = "data/err_log.txt"
current_time: time.struct_time = localtime(time.time())


def time_set():
    global current_time
    current_time = localtime(time.time())


def tweet(twitter_api_data_path, user_data):
    twitter_data_txt = open(twitter_api_data_path, 'r')
    twitter_data = twitter_data_txt.read().splitlines()
    api_key = twitter_data[0]
    api_secret = twitter_data[1]
    twitter_data_txt.close()
    tweet = user_data["2_tweet"]
    access_token = user_data["3_access_token"]
    access_secret = user_data["4_access_secret"]
    img_file = user_data["6_img"]

    def send_tweet(tweet, img_file, api_key, api_secret, access_token, access_secret):
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_secret)
        bot = tweepy.API(auth)
        if img_file != "":
            bot.update_status_with_media(status=tweet, filename=img_file)
        else:
            bot.update_status(status=tweet)

    print(user_data["1_twitter_id"])
    print(tweet)
    print()
    send_tweet(tweet, img_file, api_key, api_secret, access_token, access_secret)


if __name__ == "__main__":

    while True:
        try:
            time_set()  # 초기 시간 확인
            print(f"현재 시각은 {current_time.tm_hour}시 {current_time.tm_min}분입니다.\n{60 - current_time.tm_min}분 뒤 자동으로 트윗됩니다.")
            print("-" * 50)
            time.sleep(60 * (59 - current_time.tm_min))

            time_set()
            while current_time.tm_min != 0:  # 정각 확인
                time.sleep(10)
                time_set()
            print(f"{current_time.tm_hour}시 정각입니다. 자동으로 트윗합니다.\n")

            user_json = open(user_data_path, 'r', encoding='utf-8')  # open user_list.json as user_json
            user_dict = json.load(user_json)  # make user_json to user_dict
            user_json.close()

            i = 1
            user_list = []
            while i < len(user_dict):
                user_data = user_dict[str(i)]
                duration = list(map(int, user_data['5_duration'].split()))
                if current_time.tm_hour in duration:
                    try:
                        tweet(twitter_api_data_path, user_data)
                    except tweepy.errors.Forbidden as err:
                        err_str = str(err)
                        with open(err_log_path, 'a') as f:
                            err_code = "[" + str(time.strftime('%m/%d %H:%M', time.localtime(time.time()))) + "] " + "tweepy error : \n" + err_str + "\n\n"
                            f.write(err_code)
                        print("tweepy error")
                        print("사유 :", err, "\n")
                        pass
                i += 1

        except Exception as err:
            err_str = str(err)
            with open(err_log_path, 'a') as f:
                err_code = "[" + str(time.strftime('%m/%d %H:%M', time.localtime(time.time()))) + "] " + "new error : \n" + err_str + "\n\n"
                f.write(err_code)
            print("new error")
            print("사유 :", err, "\n")
            pass

        print("자동 트윗이 완료되었습니다.")
        print("-" * 50)
