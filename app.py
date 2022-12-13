from flask import Flask
import json
from database.db import initialize_db
from database.models import pitch,OfferMade
from flask import request

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost:27017/xharktank'
}
#app.config['MONGO_URI'] = "mongodb://localhost:27017/xharktank"
 
initialize_db(app)

pitch.objects().delete()

@app.route('/pitches',methods=['POST'])
def add_pitch():
    try:
        body = request.get_json()     
        #print(body)
        Pitch =  pitch(**body).save()
        #print(Pitch)
        #_id
        id1 = Pitch.id
        if Pitch.entrepreneur=='' or Pitch.entrepreneur is None or len(Pitch.entrepreneur)==0:
            return 'Bad Request #3',400
        if Pitch.equity>100:
            return 'Bad Request #3',400
        return {'id':str(id1)},200
    except :
        return 'Bad Request',400
    

@app.route('/pitches',methods=['GET'])
def printall():

    Pitch = pitch.objects().order_by('-id')
    temp=[]
    #{_id :ObjectId()}
    for elem in Pitch:
        elem=elem.to_mongo().to_dict()
        elem['id']=str(elem['_id'])
        temp_offer=[]
        
        if len(elem['offers'])!=0:
            for a in elem['offers']:
                a['id']=str(a['_id'])
                a.pop('_id')
                temp_offer.append(a)
        elem['offers']=temp_offer
        elem.pop('_id')
        temp.append(elem)
        
    return json.dumps(temp),200
    

@app.route('/pitches/<id>',methods=['GET'])
def printoffer(id):
    try:
        Pitch = pitch.objects.get(id=id)
        temp=Pitch
        temp=temp.to_mongo().to_dict()
        temp['id']=str(temp['_id'])
        temp.pop('_id')
        temp_offer=[]
        if len(temp['offers'])!=0:
            for offerVal in temp['offers']:
                offerVal['id']=str(offerVal['_id'])
                offerVal.pop('_id')
                temp_offer.append(offerVal)
        temp['offers']=temp_offer
        return json.dumps(temp),200
    except:
        return 'Not Found',404
           
@app.route('/pitches/<id>/makeOffer',methods=['POST'])
def makeoffer(id):
    try:
        body = request.get_json()
        
        try:
            value =  OfferMade(**body).save() 
        except:
            return 'Bad Request',400

        try:
            Pitch = pitch.objects.get(id=id)
        except:
            return 'Not Found',404

        id1 = value.id
        if value.investor=='' or value.investor is None or len(value.investor)==0:
            return 'Bad Request #3',400
        if value.equity>100:
            return 'Bad Request #3',400
        
        Pitch.offers.append(value.to_mongo().to_dict())
        Pitch.save()
        return {'id': str(id1)}, 200
    except:
        return 'Not Found',404
       
        
if __name__ == "__main__":
    app.run(debug=True,port=8081)
