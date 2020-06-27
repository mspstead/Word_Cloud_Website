from flask import Flask, render_template, redirect, request,jsonify
import os
from werkzeug.utils import secure_filename
import word_cloud as wc

app = Flask(__name__)

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

@app.route("/")
def home():

    silhouette_image = 'static/data/images/reddit_snoo.jpg'
    word_cloud = '/static/data/images/reddit_snoo_cloud.png'

    return render_template('index.html', silhouette_file=silhouette_image, cloud_file=word_cloud)

@app.route("/info")
def example():
    return render_template('info.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/upload", methods=["GET", "POST"])
def upload_image():

    silhouette_image = 'static/data/images/reddit_snoo.jpg'
    word_cloud = 'static/data/images/reddit_snoo_cloud.png'

    # Check if we have received a post request
    if request.method == "POST":

        if request.files:

            if "filesize" in request.cookies:

                if not allowed_image_filesize(request.cookies["filesize"]):
                    return jsonify(name='File size too large')

                image = request.files["image"]

                if image.filename == "":
                    return jsonify(name='No file selected')

                if allowed_image(image.filename):

                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    silhouette_image_path = "static/temp_data/uploads/" + filename

                    return jsonify(name=filename,path=silhouette_image_path)

                else:
                    return jsonify(name='That file type is not supported.')

    return render_template('index.html', silhouette_file=silhouette_image, cloud_file=word_cloud)

@app.route("/process", methods=["GET", "POST"])
def generate_word_cloud():

    silloutte_path = 'static/data/images/reddit_snoo.jpg'
    word_cloud_path = 'static/data/images/reddit_snoo_cloud.png'

    # Check if we have received a post request
    if request.method == "POST":

        silloutte_path = request.data.decode('utf-8')
        word_cloud_path = wc.generateWordCloud(silloutte_path,'https://www.reddit.com/r/dataisbeautiful/comments/gs4me1/oc_word_cloud_comparison_between_user_comments_on/')

        return jsonify(cloud_file_path=word_cloud_path)

    return render_template('index.html', silhouette_file=silloutte_path, cloud_file=word_cloud_path)

if __name__ == "__main__":
    app.run(debug=True)

