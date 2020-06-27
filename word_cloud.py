import praw
import pandas as pd
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from hashlib import md5
from time import localtime
import os

def remove_common_words_symbols_and_nums(dataframe, column):
    """Removes common words and numbers from text strings in a dataframe column"""

    s = (stopwords.words('english')) #nltk stopwords dictionary
    dataframe.dropna(inplace=True)
    dataframe[column] = dataframe[column].astype('str')
    dataframe = dataframe[dataframe[column] != '[removed]']
    dataframe = dataframe[dataframe[column] != '[deleted]']
    dataframe[column] = dataframe[column].str.replace(r'(https?:\ / \ /)(\s)*(www\.)?(\s) * ((\w | \s) +\.) * ([\w\-\s]+\ /) * ([\w\-]+)((\?)?[\w\s] *= \s * [\w\ % &] * ) *', ' ')
    dataframe[column] = dataframe[column].str.replace(r'[^a-zA-Z]+', ' ')
    dataframe[column] = dataframe[column].str.replace('mr', '')
    dataframe[column] = dataframe[column].str.lower()
    dataframe[column] = dataframe[column].apply(lambda x: ' '.join([item for item in x.split() if item not in s]))

    return dataframe

def generateWordCloud(silloutte_image_path,reddit_url='', text_input=''):

    reddit = praw.Reddit(client_id="Y-KvkaV6mcCbiA",
                         client_secret="DZ0tBF1AlX6CJ5lEY8MF7S1gGMk",
                         password="01101991mS",
                         user_agent="testscript by /u/sugar-man",
                         username="sugar-man")

    urls = [reddit_url]
    comment_body_list = []
    for url in urls:
        print('done')
        submission = reddit.submission(url=url)
        submission.comments.replace_more(limit=0)
        all_comments = submission.comments.list()
        for comment in all_comments:
            comment_body_list.append(comment.body)

    comment_df = pd.DataFrame(data=comment_body_list, columns=['comment'])
    comment_df = remove_common_words_symbols_and_nums(comment_df, 'comment')

    words_comments = comment_df['comment'].str.split()
    flat_list = [item for sublist in list(words_comments) for item in sublist]
    words = pd.DataFrame({'word': flat_list})
    word_count_df = words['word'].value_counts().to_frame().reset_index()
    print(words.size)
    print(word_count_df.nlargest(100, 'word'))

    d = {}
    for a, x in word_count_df.values:
        d[a] = x

    image_mask = np.array(Image.open(os.path.join(silloutte_image_path)))

    wordcloud = WordCloud(width=400, height=400,
                          mask=image_mask,
                          background_color='white',
                          min_font_size=5).generate_from_frequencies(d)

    # plot the WordCloud image
    plt.figure(figsize=(6, 6), facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.savefig(os.path.join('static/temp_data/exports/', 'test.png'))

    return 'static/temp_data/exports/test.png'

