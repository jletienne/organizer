from flask import Flask, render_template,request, redirect, url_for
import os
import exifread
from datetime import datetime



app = Flask(__name__,static_url_path='/static')
app.config.from_object(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello_world():


    # get photo
    photo_list = [i for i in os.listdir('static/photos_to_review')]
    photos_left = len(photo_list)

    photo = photo_list[0]

    with open(f'static/photos_to_review/{photo}', 'rb') as fh:
        try:
            tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
            dateTaken = tags["EXIF DateTimeOriginal"]
            date_taken = str(datetime.strptime(str(dateTaken), '%Y:%m:%d %H:%M:%S').date())
        except:
            date_taken = str(datetime.fromtimestamp(os.stat(f'static/photos_to_review/{photo}').st_birthtime).date())

    if request.method == 'POST':
            result=int(request.form['result'])

            results_map = {'4': 'life', '8': 'food', '6': 'delete', '2': 'funny', '9': 'biz', '7': 'football', '1': 'dance'}
            os.rename(f'static/photos_to_review/{photo}', f'static/{results_map[str(result)]}/{date_taken}_{photo}')


            photo_list = [i for i in os.listdir('static/photos_to_review')]
            photos_left = len(photo_list)
            photo = photo_list[0]

            with open(f'static/photos_to_review/{photo}', 'rb') as fh:
                try:
                    tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
                    dateTaken = tags["EXIF DateTimeOriginal"]
                    date_taken = str(datetime.strptime(str(dateTaken), '%Y:%m:%d %H:%M:%S').date())
                except:
                    date_taken = str(datetime.fromtimestamp(os.stat(f'static/photos_to_review/{photo}').st_birthtime).date())


            return render_template('index.html', photo = f'static/photos_to_review/{photo}', date_taken = date_taken, photos_left = photos_left)

    return render_template('index.html', photo = f'static/photos_to_review/{photo}', date_taken = date_taken, photos_left = photos_left)



if __name__ == '__main__':
    app.debug = True
    app.run()
