from config.config_flask import timedelta
from flask import Flask, send_from_directory, render_template
#from werkzeug.utils import secure_filename
#from config.image_path import event
from model import *
from os.path import splitext

UPLOAD_FOLDER = '/images'
ALLOWED_EXTENTIONS = ['png', 'jpg', 'jpeg']

class Image():
    def upload(url, expire):
        #last = Event.query.order_by(Event.id.desc()).first()
        #img = event+str(last.id+1)+splitext(file.filename)[1]
        eve = Event(image = url)
        db.session.add(eve)
        db.session.commit()
        #file.save(secure_filename(img))

    def allowed_img(filename):
        return '.' in filename and \
            filename.rslit('.', 1)[1].lower() in ALLOWED_EXTENTIONS

    def upload_img(filename):
        return render_template(app.config['UPLOAD_FOLDER'], filename)

    def upload(filename):
        parser = reqparse.RequestParser()
        parser.add_argument('images', type=FileStorage, loaction='images/', action='appand')
        args = parser.parse_args()
        images = args['images']

        extension = images.filename.split('.')[-1]
        if extension in ALLOWED_EXTENSIONS:
            image.save('./images/{0}'.format(source_filename(image.filename)))
        else:
            return 0