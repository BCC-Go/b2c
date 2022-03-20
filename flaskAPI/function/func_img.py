from config.config_flask import timedelta
from flask import Flask, send_from_directory, render_template
from s3_connection import s3_connection, s3_put_object
from config.config_s3 import AWS_S3_BUCKET_NAME, AWS_S3_BUCKET_REGION
from model import *
from os.path import splitext

ALLOWED_EXTENTIONS = ['png', 'jpg', 'jpeg']
s3 = s3_connection()

class Image():
    def upload(file):
        last = Event.query.order_by(Event.id.desc()).first()
        if last is None:
            num = 0
        else:
            num = last.id
        img = 'image/event/'+str(num+1)+splitext(file.filename)[1]
        file.save(img)
        ret = s3_put_object(s3, AWS_S3_BUCKET_NAME, img, img[6:])
        if ret :
            eve = Event(image = img[6:])
            db.session.add(eve)
            db.session.commit()
    
