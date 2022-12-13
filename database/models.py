from .db import db

class pitch(db.Document):
    entrepreneur = db.StringField(required=True)
    pitchTitle = db.StringField(required=True)
    pitchIdea = db.StringField(required=True)
    askAmount = db.FloatField(required=True)
    equity = db.FloatField(required=True)
    offers = db.ListField(db.DictField(default=None),required=False)
    

class OfferMade(db.Document):
    investor = db.StringField(required=True)
    amount = db.FloatField(required=True)
    equity = db.FloatField(required=True)
    comment = db.StringField(required=True)
    
