def auth_twitter_api(key, key_secret, token, token_secret):
    import tweepy
    # 認証情報を設定
    auth = tweepy.OAuthHandler(key, key_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)
    return api

def alltweets_to_csv(api):
    import csv
    # 全ツイートを入れる空のリストを用意
    all_tweets    = []
    # 直近の200ツイート分を取得しておく
    latest_tweets = api.user_timeline(count=200)
    all_tweets.extend(latest_tweets)

    # 取得するツイートがなくなるまで続ける
    while len(latest_tweets)>0:
        latest_tweets = api.user_timeline(count=200, max_id=all_tweets[-1].id-1)
        all_tweets.extend(latest_tweets)

    with open('all_tweets.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['tweet_text', '#characters', '#favorited', '#retweeted', 'hasImage', 'hasBlogLink'])
        for tweet in all_tweets:
            if (tweet.text.startswith('RT')) or (tweet.text.startswith('@')):
                continue # RTとリプライはスキップ
            else:
                has_image        = 0 # 画像付きのツイートか
                has_bloglink     = 0 # ブログへのリンク付きのツイートか
                tweet_characters = tweet.text # ツイートの文字列
                if 'media' in tweet.entities:
                    has_image = 1
                if len(tweet.entities['urls']) > 0:
                    # urlは、文字数としてカウントしない
                    tweet_characters = tweet_characters.strip(tweet.entities['urls'][0]['url']).strip()
                    if 'nishipy.com' in tweet.entities['urls'][0]['display_url']:
                        has_bloglink   = 1
                writer.writerow([tweet.text, len(tweet_characters), tweet.favorite_count, tweet.retweet_count, has_image, has_bloglink])
    return all_tweets
