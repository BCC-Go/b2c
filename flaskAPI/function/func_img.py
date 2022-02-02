from config.config_flask import timedelta
from config.image_path import event
from model import *
from os.path import splitext

class Image():
    def upload(file):
        last = Event.query.order_by(Event.id.desc()).first()
        img = event+str(last.id+1)+splitext(file.filename)[1]
        eve = Event(image = img)
        db.session.add(eve)
        db.session.commit()
        file.save(img)
