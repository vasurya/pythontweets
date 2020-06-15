import tweepy as tweepy
import pandas as pd
import preprocessor as p
from textblob import TextBlob
from gensim.parsing.preprocessing import remove_stopwords
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


app_name = '<YOUR APP NAME>'
consumer_key='<YOUR CONSUMER KEY'
consumer_secret='<YOUR CONSUMER SECRET KEY>'
access_token='<YOUR ACCESS TOKEN>'
access_secret='<YOUR SECRET ACCESS TOKEN>'


auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth,wait_on_rate_limit = False)#Changed from true

search = input("What does twitter think about #___")
search_term = "#{} -filter:retweets".format(search)
date_since = "2020-05-25"

tweets = tweepy.Cursor(api.search,q=search_term,lang="en",since = date_since).items()#removed items limit
tt = [[tweet.text] for tweet in tweets]
tweet_text = pd.DataFrame(data=tt, columns= ['text'])
print(tweet_text.info)

# tweet_text.to_csv(r'out.csv', index = True, header = True)


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
# data = pd.read_csv(r"C:\Users\Hp\Desktop\PYTHONTWEETS\PART2-ANALYZING DATABASE\trumptweets.csv")

tweet_text = tweet_text.drop_duplicates()
# data = data.drop("retweets", axis=1)
# data = data.drop("mentions", axis=1)
# data = data.drop("favorites", axis=1)
# data = data.drop("hashtags", axis=1)
# data = data.drop("geo", axis=1)
# data = data.drop("date", axis=1 )
# data = data.drop("link", axis=1)
def preprocess(row):
    text = row['text']
    text = p.clean(text)
    return text

def stopword(row):
    text = row['text']
    text = remove_stopwords(text)
    return text

neutral = 0
positive = 0
negative = 0
count = 0
total_p = 0
def sentiment_anal(row):
    text = row
    sent = TextBlob(text).sentiment

    global total_p
    global count
    global neutral
    global positive
    global negative

    total_p += sent.polarity

    if sent.polarity == 0:
        neutral += 1
    elif sent.polarity > 0:
        positive += 1
    elif sent.polarity < 0:
        negative += 1
    count += 1
    try:
        return sent
    except:
        return None

def percentage(item, total):
    val = float(item)/float(total)*100
    return format(val, '.2f')

def Piechart(positive,negative,neutral):
    labels = 'Positive','Neutral','Negative'
    sizes = [positive, neutral, negative]
    colors= ['yellowgreen','lightskyblue','lightcoral']
    explode = (0.1,0,0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels = sizes, explode = explode, colors = colors, shadow=True, startangle = 140)
    ax1.axis('equal')
    #plt.legend(labels, loc="best")
    plt.title('What do people think about # '+search)
    plt.legend(labels,loc=3)
    plt.axis('equal')
    # plt.tight_layout()




tweet_text['text'] = tweet_text.apply(preprocess,axis=1)
tweet_text['text'] = tweet_text.apply(stopword,axis=1)
tweet_text['text'] = tweet_text['text'].str.lower().str.replace('[^\w\s]',' ').str.replace('\s\s+', ' ')
#Error in below Line
tweet_text['sentiment'] = tweet_text['text'].apply(sentiment_anal)

tweet_text['sentiment'][0][0]

tweet_text['polarity'] = tweet_text['sentiment'].apply(lambda x:x[0])
tweet_text['subjectivity'] = tweet_text['sentiment'].apply(lambda x:x[1])

data_v = tweet_text.text.values
# print(data.head())
# print("Neutral ",neutral)
# print("Positive ", positive)
# print("Negative ", negative)

positive_per = percentage(positive,count)
negative_per = percentage(negative,count)
neutral_per = percentage(neutral,count)
print(positive_per)
print(negative_per)
print(neutral_per)
print(count)

avg_pol = total_p/count
print("Overall")
if avg_pol == 0:
    print('Neutral')
elif avg_pol < 0:
    print('Negative')
else:
    print('Positive')

Piechart(positive_per,negative_per,neutral_per)
wordcloud = WordCloud(
    width = 3000,
    height = 2000,
    background_color = 'black').generate(str(data_v))

fig = plt.figure(
    figsize = (40,30),
    facecolor = 'k',
    edgecolor = 'k')

plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()
