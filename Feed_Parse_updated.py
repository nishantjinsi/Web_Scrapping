import feedparser
import pandas as pd
import time
import re

URL_list = list()
urls = list()
## Reading the values from the file and storing it into a list for parsing
with open ("/Users/nishantjinsiwale/Downloads/feed_list.tsv") as tsv:
    urls = [line.strip() for line in tsv]

def parse(urls ):
    feed_li = list()
    title_li = list()
    rss_li = list()
    dic = dict()
    d = {'RSS_Feed':[], 'Content':[]}

    ## Creating a Dataframe to store the URL, Feed_Title and the Content URL and its count
    columns = ['RSS Feed',  'Content URL', 'Count', 'Feed Title']
    Feed_Frame = pd.DataFrame(columns=columns)

    for i in urls:
        x = i.split()
        URL_list.append(x[1])
## Creating a variable for use

    ## For each URL in the list, parse through the content
    for l in URL_list:
        d = feedparser.parse(l)
        #for each post in the feed, store the values of the Title and the Content URL in particular lists
        for post in d.entries:
            # Append the values of Content URLS in the feed list
            feed_li.append(post.link)
            # Append the values of Title in the Title list
            title_li.append(post.title)
            # Append the value of Feed in the list
            rss_li.append(l)



    # Store these values we extracted into a dataframe
    feed_se = pd.Series(feed_li)
    title_se = pd.Series(title_li)
    rss_se = pd.Series(rss_li)

    Feed_Frame['Content_URL'] = feed_se.values
    Feed_Frame['Feed Title'] = title_se.values
    Feed_Frame['RSS Feed'] = rss_se

    return Feed_Frame

def count(df):
    dic = dict()
    list1 = list()
    x = df['Feed Title'].value_counts()
    # Store these values into a column in the dataframe named as Count
    df['Count'] =  x.values
    # Drop the duplicate URLs from the dataframe to get a list of unique feeds
    df = df.drop_duplicates(subset='Feed Title')
    # Strip the value of the head from the URl for comparision with the RSS Feed
    for i, j in df.iterrows():

            http1 =  re.split('://',j['Content_URL'])[1]


            list1.append(http1.split('/')[0])
    # Append that head in to the dataframe
    df['head'] = list1
    #Compare the values to check if the head is present in URL, the Content is generated from the original RSS Feed
    for i, j in df.iterrows():
        if j['head'] not in j['RSS Feed']:
            df['binary_count'] = 0
        else:
            df['binary_count'] = 1
    # Delete the Feeds that are not from the original RSS Feed
    df = df[df.binary_count!=0]

    return df

## Calling function parse to return the dataframe and storing it into an object --df
df = parse(urls)
## Calling function count to print out a CSV with expected output
print list(count(df))