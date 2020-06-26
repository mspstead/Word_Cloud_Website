from flask import Flask, render_template, redirect, request, session
import os
from werkzeug.utils import secure_filename
import praw
import pandas as pd
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from hashlib import md5
from time import localtime

app = Flask(__name__)


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_2$c2M"p6&8z\n\xec]/'
app.config["IMAGE_UPLOADS"] = '/Users/mike/Documents/Word_Cloud_Website/static/temp_data/uploads'
app.config["IMAGE_EXPORTS"] = '/Users/mike/Documents/Word_Cloud_Website/static/temp_data/exports'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 5 * 1024 * 1024

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

@app.route("/", methods=["GET", "POST"])
def home():

    #Check to see if this is a fresh start and load default images otherwise use uploaded images.
    if 'silhouette_image' not in session.keys():
        session['silhouette_image'] = '/static/data/images/reddit_snoo.jpg'
        session['word_cloud'] = '/static/temp_data/exports/test.png'

    #Check if we have received a post request
    if request.method == "POST":

        if request.form['submit'] == 'Generate Word Cloud':
            word_cloud_path = generateWordCloud(session.get('silhouette_image'),'https://www.reddit.com/r/AskReddit/comments/hg5cqg/you_have_a_day_to_do_anything_without_any_moral/','')
            session['word_cloud'] = word_cloud_path
            print(session.get('word_cloud'))
            return render_template('index.html', silhouette_file=session.get('silhouette_image'),cloud_file=session.get('word_cloud'))

        elif request.form['submit'] == 'Upload':

            if request.files:

                if "filesize" in request.cookies:

                    if not allowed_image_filesize(request.cookies["filesize"]):
                        print("Filesize exceeded maximum limit")
                        return redirect(request.url)

                    image = request.files["image"]

                    if image.filename == "":
                        print("No filename")
                        return redirect(request.url)

                    if allowed_image(image.filename):
                        filename = secure_filename(image.filename)
                        image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                        session['silhouette_image'] = "/static/temp_data/uploads/"+filename
                        print("Image saved")

                        return render_template('index.html', silhouette_file=session.get('silhouette_image'),cloud_file=session.get('word_cloud'))

                    else:
                        print("That file extension is not allowed")
                        return redirect(request.url)

    return render_template('index.html', silhouette_file=session.get('silhouette_image'), cloud_file=session.get('word_cloud'))

@app.route("/info")
def example():
    return render_template('info.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')


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

    image_mask = np.array(Image.open(os.path.join(app.config["IMAGE_UPLOADS"],silloutte_image_path.split('/')[4])))

    wordcloud = WordCloud(width=400, height=400,
                          mask=image_mask,
                          background_color='white',
                          min_font_size=5).generate_from_frequencies(d)

    # plot the WordCloud image
    plt.figure(figsize=(6, 6), facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.savefig(os.path.join(app.config["IMAGE_EXPORTS"], 'test.png'))

    return '/static/temp_data/exports/test.png'


if __name__ == "__main__":
    app.run(debug=True)

