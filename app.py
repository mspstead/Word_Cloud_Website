from flask import Flask, render_template,request,jsonify, send_file
import os
from werkzeug.utils import secure_filename
import word_cloud as wc

app = Flask(__name__)

#ßapp.config["IMAGE_UPLOADS"] = '/home/ubuntu/Word_Cloud_Website/static/temp_data/uploads'
#app.config["IMAGE_EXPORTS"] = '/home/ubuntu/Word_Cloud_Website/static/temp_data/exports'
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

@app.route("/examples")
def example():
    return render_template('info.html')

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
                    filename_to_save = wc.add_prefix(filename)
                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename_to_save))
                    silhouette_image_path = "/static/temp_data/uploads/" + filename_to_save

                    return jsonify(name=filename_to_save,path=silhouette_image_path)

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

        if(data.get('stats_selection')=='checked'):
            stats_select = True
        else:
            stats_select = False

        silloutte_path = data.get('path') #Get the current silloutte image

        reddit_url = data.get('reddit_url') #Get the user entered reddit url
        username = data.get('user_name') #Get reddit username

        twitter = data.get('twitter') #Get twitter handle
        page_depth = data.get('page_depth') #Page search depth for twitter data retrieval

        text_input = data.get('text_input') #Get the text data
        background_colour = data.get('backgroundColour') #Get the background colour selection
        colour_scheme = data.get('colour_scheme') #Get selected colour scheme

        #If user has supplied a reddit comments url
        if reddit_url != '': #Check reddit url is not empty

            data = wc.generateRedditCommentsStats(silloutte_path, reddit_url, background_col=background_colour, colour_selection=colour_scheme, legend=stats_select)

            if(data.get('message')=='success'):

                return jsonify(message='success',cloud_file_path=data.get('img_path'),csv_file_path=data.get('csv_path'))

            else:

                return jsonify(message='No data',cloud_file_path=data.get('img_path'),csv_file_path=data.get('csv_path'))

        #If user has supplied a reddit username
        elif username != '':

            data = wc.generateRedditUserStats(silloutte_path, username, background_col=background_colour, colour_selection=colour_scheme,legend=stats_select)

            if(data.get('message')=='success'):

                return jsonify(message='success',cloud_file_path=data.get('img_path'),csv_file_path=data.get('csv_path'))

            else:

                return jsonify(message='No data',cloud_file_path=data.get('img_path'),csv_file_path=data.get('csv_path'))


        # If user has supplied a twitter username
        elif twitter != '':
            data = wc.generateTwitterUserStats(silloutte_path, twitter, background_col=background_colour,
                                                  colour_selection=colour_scheme,page_nr=int(page_depth),legend=stats_select)

            if (data.get('message') == 'success'):

                return jsonify(message='success', cloud_file_path=data.get('img_path'),
                                   csv_file_path=data.get('csv_path'))

            else:

                return jsonify(message='No data', cloud_file_path=data.get('img_path'),
                                   csv_file_path=data.get('csv_path'))

        #If user has supplied text
        elif text_input !='':

            data = wc.generateRawTextStats(silloutte_path,text_input, background_col=background_colour, colour_selection=colour_scheme,legend=stats_select)

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

@app.route("/imageMasks",methods=["GET"])
def imageMasks():

    if request.method=='GET':

        folder = 'static/data/imagemasks/'

        file_list = []
        for filename in os.listdir(folder):
            if filename.endswith(('.jpg', '.png','.gif','.jpeg')):
                file_list.append(folder+filename)
        return jsonify(image_paths=file_list)

if __name__ == "__main__":
    app.run(debug=True)

