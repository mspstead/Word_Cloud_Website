from flask import Flask, render_template,request,jsonify, send_file
import os
from werkzeug.utils import secure_filename
import word_cloud as wc

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = '/Users/mike/Documents/Word_Cloud_Website/static/temp_data/uploads'
app.config["IMAGE_EXPORTS"] = '/Users/mike/Documents/Word_Cloud_Website/static/temp_data/exports'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 5 * 1024 * 1024

def allowed_image(filename):
    """Function to check if file submitted is an image file"""
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):
    """Function to check if image file uploaded is within filesize."""
    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

@app.route("/")
def home():

    silhouette_image = 'static/data/images/reddit_snoo.jpg'
    word_cloud = 'static/data/images/reddit_snoo_cloud.png'
    csv_file_path = 'static/data/csvdata/example.csv'

    return render_template('index.html', silhouette_file=silhouette_image, cloud_file=word_cloud, csv_file=csv_file_path)

@app.route("/info")
def example():
    return render_template('info.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    """Function which handles the silloutte image upload by a user"""
    silhouette_image = 'static/data/images/reddit_snoo.jpg'
    word_cloud = 'static/data/images/reddit_snoo_cloud.png'
    csv_file_path = 'static/data/csvdata/example.csv'

    # Check if we have received a post request
    if request.method == "POST":

        if request.files:

            if "filesize" in request.cookies:

                if not allowed_image_filesize(request.cookies["filesize"]):
                    #If file to large let user know
                    return jsonify(name='File size too large')

                image = request.files["image"]

                if image.filename == "":
                    #If file not supplied let user know
                    return jsonify(name='No file selected')

                if allowed_image(image.filename):

                    #Save silloutte image template uploaded by user and update the silloutte image shown
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    silhouette_image_path = "static/temp_data/uploads/" + filename

                    return jsonify(name=filename,path=silhouette_image_path)

                else:
                    #User did not upload a supported image type.
                    return jsonify(name='That file type is not supported.')

    return render_template('index.html', silhouette_file=silhouette_image, cloud_file=word_cloud, csv_file=csv_file_path)

@app.route("/process", methods=["GET", "POST"])
def generate_word_cloud():
    """Function to generate a word cloud and display it to the user"""

    silloutte_path = 'static/data/images/reddit_snoo.jpg'
    word_cloud_path = 'static/data/images/reddit_snoo_cloud.png'
    csv_file_path = 'static/data/csvdata/example.csv'

    # Check if we have received a post request
    if request.method == "POST":

        data = request.get_json(force=True) #Get the data from the ajax

        silloutte_path = data.get('path') #Get the current silloutte image
        reddit_url = data.get('reddit_url') #Get the user entered reddit url
        text_input = data.get('text_input') #Get the text data

        if reddit_url != '': #Check reddit url is not empty

            data = wc.generateRedditWordCloud(silloutte_path, reddit_url)

            if(data.get('message')=='success'):

                return jsonify(message='success',cloud_file_path=data.get('img_path'),csv_file_path=data.get('csv_path'))

            else:

                return jsonify(message='No data',cloud_file_path=data.get('img_path'),csv_file_path=data.get('csv_path'))

        elif text_input !='':
            data = wc.generateWordCloud(silloutte_path,text_input)
            return jsonify(message='success',cloud_file_path=data.get('img_path'),csv_file_path=data.get('csv_path'))

        else:
            return jsonify(message='error',cloud_file_path=word_cloud_path,csv_file_path=data.get('csv_path'))

    return render_template('index.html', silhouette_file=silloutte_path, cloud_file=word_cloud_path, csv_file=csv_file_path)

@app.route("/downloadImage",methods=["POST"])
def downloadCloud():
    """Function to download word cloud image"""

    if request.method=='POST':
        word_cloud = request.form['download-image']
        return send_file(word_cloud,
                        mimetype='image/png',
                        attachment_filename='word_cloud_image.png',
                        as_attachment=True)

@app.route("/downloadFile",methods=["POST"])
def downloadFile():
    """Function to download word cloud stats csv file"""

    if request.method=='POST':
        word_cloud_csv = request.form['download-file']
        return send_file(word_cloud_csv,
                        mimetype='text/csv',
                        attachment_filename='word_cloud_stats.csv',
                        as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

